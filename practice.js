/* Code Lab: runs real Python (Pyodide) in a Web Worker so infinite loops can be killed safely. */
(() => {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const KEY = 'orbit.practice.v1';
  const store = Object.assign({ solved: {}, code: {} }, JSON.parse(localStorage.getItem(KEY) || '{}'));
  const save = () => localStorage.setItem(KEY, JSON.stringify(store));
  const MOCK_DAYS = [7, 14, 21];
  let cur = null;

  /* ---------------- Python harness (runs inside the worker) ---------------- */
  const HARNESS = `
import json, math, traceback, inspect
def _canon(x, cmp):
    if cmp == 'sorted2':
        return sorted([sorted(i) if isinstance(i, list) else i for i in x], key=lambda v: json.dumps(v))
    if cmp == 'sorted':
        return sorted(x)
    return x
def _approx(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_approx(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_approx(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) < 1e-6
    return a == b
def _eq(a, b, cmp):
    if cmp == 'approx':
        return _approx(a, b)
    try:
        return _canon(a, cmp) == _canon(b, cmp)
    except Exception:
        return False
async def _run_one(t_json, fn, kind, cmp, tree):
    t = json.loads(t_json)
    g = globals()
    try:
        if kind == 'class':
            obj = g[fn](*t['init']); out = []
            for op in t['ops']:
                out.append(getattr(obj, op[0])(*op[1:]))
            actual = out
        else:
            args = t['args']
            if tree:
                args = [build_tree(args[0])] + args[1:]
            actual = g[fn](*args)
            if inspect.isawaitable(actual):
                actual = await actual
        try:
            actual = json.loads(json.dumps(actual))
        except TypeError:
            return json.dumps(dict(ok=False, actual=repr(actual), note='return value is not JSON-serialisable'))
        return json.dumps(dict(ok=_eq(actual, t['expected'], cmp), actual=actual))
    except Exception:
        return json.dumps(dict(ok=False, error=traceback.format_exc(limit=4)))
`;

  const WORKER_SRC = `
importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js');
const PRELUDE=${JSON.stringify(PRELUDE_PY)}, HARNESS=${JSON.stringify(HARNESS)};
let py, replNs, buf=[];
const ready=(async()=>{
  py=await loadPyodide();
  py.setStdout({batched:s=>buf.push(s)}); py.setStderr({batched:s=>buf.push(s)});
  replNs=py.globals.get('dict')(); py.runPython(PRELUDE,{globals:replNs});
  postMessage({type:'ready'});
})();
const clean=e=>{const m=String(e.message||e).trim().split('\\n'); const i=m.findIndex(l=>l.startsWith('  File "<exec>"')); return (i>0?m.slice(i):m).join('\\n');};
const show=r=>{if(r===undefined||r===null)return null; const s=String(r); if(r&&r.destroy)r.destroy(); return s;};
onmessage=async ev=>{
  const m=ev.data; await ready; postMessage({type:'started',id:m.id}); buf=[];
  try{
    if(m.type==='repl'){
      let res=null,error=null; try{res=show(await py.runPythonAsync(m.code,{globals:replNs}));}catch(e){error=clean(e);}
      postMessage({type:'done',id:m.id,out:buf.join('\\n'),result:res,error});
    } else {
      const ns=py.globals.get('dict')(); py.runPython(PRELUDE+HARNESS,{globals:ns});
      try{ await py.runPythonAsync(m.code,{globals:ns}); }catch(e){ postMessage({type:'done',id:m.id,out:buf.join('\\n'),error:clean(e)}); return; }
      if(m.type==='run'){ postMessage({type:'done',id:m.id,out:buf.join('\\n')}); return; }
      const p=m.problem;
      ns.set('_fn',p.fn); ns.set('_kind',p.kind); ns.set('_cmp',p.cmp); ns.set('_tree',!!p.tree);
      if(!ns.get(p.fn)){ postMessage({type:'done',id:m.id,out:'',error:'Could not find "'+p.fn+'" - keep the function/class name from the starter code.'}); return; }
      for(let i=0;i<p.tests.length;i++){
        buf=[]; ns.set('_test_json',JSON.stringify(p.tests[i]));
        const r=JSON.parse(await py.runPythonAsync('await _run_one(_test_json, _fn, _kind, _cmp, _tree)',{globals:ns}));
        postMessage({type:'progress',id:m.id,i,res:r,out:buf.join('\\n')});
      }
      postMessage({type:'done',id:m.id});
    }
  }catch(e){ postMessage({type:'done',id:m.id,error:clean(e)}); }
};`;

  /* ---------------- worker management ---------------- */
  let worker = null, ready = false, nextId = 1, job = null, timer = null;
  const status = (t, cls) => { const el = $('#py-status'); el.textContent = t; el.className = 'pill ' + (cls || ''); };
  function spawn() {
    ready = false; status('Python: loading… (first time ~10 MB)', 'busy');
    worker = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: 'text/javascript' })));
    worker.onerror = e => { status('Python failed to load (offline?)', ''); if (job) job.onFail('Could not load Python. Check your internet connection (needed once to fetch the Python runtime).'); job = null; };
    worker.onmessage = ev => {
      const m = ev.data;
      if (m.type === 'ready') { ready = true; status('Python: ready ✓', 'ready'); return; }
      if (!job || m.id !== job.id) return;
      if (m.type === 'started') { arm(); return; }
      arm();
      if (m.type === 'progress') job.onProgress(m);
      if (m.type === 'done') { clearTimeout(timer); const j = job; job = null; j.onDone(m); }
    };
  }
  function arm() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      worker.terminate(); worker = null;
      const j = job; job = null;
      status('Python: stopped a stuck run', 'busy');
      if (j) j.onFail('⏱ Time limit exceeded (no result for 8 s). Likely an infinite loop or an exponential-time solution. Python was restarted.');
    }, 8000);
  }
  function submit(msg, handlers) {
    if (job) { handlers.onFail('Another run is still in progress…'); return; }
    if (!worker) spawn();
    job = Object.assign({ id: nextId++ }, handlers);
    worker.postMessage(Object.assign({ id: job.id }, msg));
  }

  /* ---------------- problem list ---------------- */
  const fmt = (v, n = 220) => { let s; try { s = JSON.stringify(v); } catch (e) { s = String(v); } if (s === undefined) s = 'None'; return s.length > n ? s.slice(0, n) + '…' : s; };
  const matchDay = (p, d) => !d || (d >= 28) || (MOCK_DAYS.includes(d) ? p.days.some(x => x <= d) : p.days.includes(d));

  function buildFilters() {
    const days = $('#f-day');
    for (let d = 1; d <= 30; d++) {
      const o = document.createElement('option'); o.value = d;
      o.textContent = `Day ${d} · ${(typeof DAYS !== 'undefined' && DAYS[d - 1] ? DAYS[d - 1].coding : '')}`.slice(0, 48);
      days.appendChild(o);
    }
    const topics = [...new Set(PROBLEMS.map(p => p.topic))].sort();
    const ts = $('#f-topic');
    topics.forEach(t => { const o = document.createElement('option'); o.textContent = t; ts.appendChild(o); });
    for (const [selector, values] of [
      ['#f-company', PROBLEMS.flatMap(p => p.sources.map(s => s.company))],
      ['#f-track', PROBLEMS.map(p => p.track)]
    ]) {
      [...new Set(values)].sort().forEach(value => {
        const option = document.createElement('option'); option.textContent = value; $(selector).appendChild(option);
      });
    }
  }
  function filtered() {
    const q = $('#q').value.trim().toLowerCase(), df = $('#f-diff').value, d = +$('#f-day').value, t = $('#f-topic').value;
    const company = $('#f-company').value, track = $('#f-track').value, evidence = $('#f-evidence').value;
    return PROBLEMS.filter(p => (!q || [p.title, p.topic, p.track, ...p.sources.map(s => s.company)].join(' ').toLowerCase().includes(q))
      && (!df || p.diff === df) && (!t || p.topic === t) && matchDay(p, d)
      && (!company || p.sources.some(s => s.company === company))
      && (!track || p.track === track) && (!evidence || p.evidence === evidence));
  }
  function renderList() {
    const list = filtered();
    $('#plist').innerHTML = list.map(p => `<li><button data-id="${p.id}" class="${cur && cur.id === p.id ? 'active' : ''}">
      <span class="t"><span>${store.solved[p.id] ? '✅ ' : ''}${esc(p.title)}</span><span class="d-${p.diff}">${p.diff}</span></span>
      <span class="m">${esc(p.topic)} · ${p.tests.length} tests</span><span class="m">${esc([...new Set(p.sources.map(s => s.company))].join(', ') || 'Profile practice')}</span></button></li>`).join('') || '<li class="quiet" style="padding:10px">No problems match.</li>';
    $('#match-count').textContent = `${list.length} of ${PROBLEMS.length} problems shown`;
    const solved = PROBLEMS.filter(p => store.solved[p.id]).length;
    $('#solved-count').textContent = `${solved} / ${PROBLEMS.length} solved`;
    $('#solved-fill').style.width = (100 * solved / PROBLEMS.length) + '%';
  }
  function open(id, pushHash = true) {
    cur = PROBLEMS.find(p => p.id === id) || PROBLEMS[0];
    $('#p-title').textContent = cur.title;
    $('#p-context').innerHTML = `<span class="pill">${esc(cur.track)}</span> <span class="pill">${esc(cur.evidence)}</span>
      <p>${esc(cur.relevance)}</p>
      ${window.HELLO_PROBLEMS[cur.id] ? `<p><a href="${esc(window.HELLO_PROBLEMS[cur.id])}" target="_blank" rel="noopener noreferrer">Open this exercise in Hello Interview ↗</a></p>` : ''}
      ${cur.sources.length ? `<details><summary>Company evidence · ${esc([...new Set(cur.sources.map(s => s.company))].join(', '))}</summary>
      ${cur.sources.map(s => `<p><b>${esc(s.company)} · ${esc(s.relation)}</b><br><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a><br>${esc(s.note)} <span class="quiet">Checked ${esc(s.checked)}.</span></p>`).join('')}
      <p class="quiet">Self-reported historical experience; local wording, examples, and contracts may differ.</p></details>` : '<p class="quiet">Original role-focused practice. No verified company attribution.</p>'}`;
    $('#p-examples').innerHTML = cur.tests.slice(0, 2).map((t, i) => `<div class="case"><b>Example ${i+1}</b><div>Input: ${esc(fmt(cur.kind === 'class' ? {init:t.init, ops:t.ops} : t.args, 1200))}</div><div>Expected: ${esc(fmt(t.expected, 1200))}</div></div>`).join('');
    $('#sol-explanation').innerHTML = marked.parse(cur.explanation);
    $('#sol-code').textContent = cur.solution;
    window.mountSolutionWalkthrough(cur);
    $('#show-sol').setAttribute('aria-expanded', 'false');
    $('#show-sol').textContent = '💡 Reference solution & explanation';
    $('#p-meta').innerHTML = `${esc(cur.topic)} · <span class="d-${cur.diff}">${cur.diff}</span> · ${cur.tests.length} test cases`;
    const html = (window.marked && (marked.parse ? marked.parse(cur.statement) : marked(cur.statement))) || esc(cur.statement);
    $('#p-statement').innerHTML = html;
    $('#code').value = store.code[cur.id] || cur.starter;
    $('#results').innerHTML = ''; $('#sol').hidden = true;
    $('#p-solved').hidden = !store.solved[cur.id];
    $('#side').classList.remove('open');
    if (pushHash) history.replaceState(null, '', '#' + cur.id);
    renderList();
  }

  /* ---------------- running ---------------- */
  const setBusy = b => { ['#run-tests', '#run-code', '#term-run'].forEach(s => $(s).disabled = b); };
  function runTests() {
    if (!cur) return;
    const code = $('#code').value; store.code[cur.id] = code; save();
    const box = $('#results'); box.innerHTML = '<div class="out">Running… ' + (ready ? '' : '(loading Python the first time takes a few seconds)') + '</div>';
    setBusy(true);
    const rows = []; let passed = 0;
    const p = cur;
    submit({ type: 'test', code, problem: { fn: p.fn, kind: p.kind, cmp: p.cmp, tree: p.tree, tests: p.tests } }, {
      onProgress(m) {
        const t = p.tests[m.i], r = m.res; if (r.ok) passed++;
        const input = p.kind === 'class' ? `ops: ${fmt(t.ops, 160)}` : `input: ${t.args.map(a => fmt(a, 120)).join(', ')}`;
        rows.push(`<div class="case ${r.ok ? 'ok' : 'no'}"><div class="h" style="color:${r.ok ? 'var(--ok)' : 'var(--bad)'}">${r.ok ? '✓' : '✗'} Test ${m.i + 1}</div>
          <div>${esc(input)}</div>${r.ok ? '' : `<div>expected: <b>${esc(fmt(t.expected))}</b></div><div>got: <b>${esc(r.error ? '' : fmt(r.actual))}</b></div>`}
          ${r.error ? `<div class="err">${esc(r.error)}</div>` : ''}${m.out ? `<div>stdout: ${esc(m.out)}</div>` : ''}</div>`);
      },
      onDone(m) {
        setBusy(false);
        if (m.error) { box.innerHTML = `<div class="err">${esc(m.error)}</div>`; return; }
        const all = passed === p.tests.length;
        if (all) { store.solved[p.id] = true; save(); $('#p-solved').hidden = false; renderList(); }
        box.innerHTML = `<div class="sum ${all ? 'pass' : 'fail'}">${all ? '🎉 All ' + p.tests.length + ' tests passed!' : passed + ' / ' + p.tests.length + ' tests passed'}</div>` + rows.join('');
      },
      onFail(msg) { setBusy(false); box.innerHTML = `<div class="err">${esc(msg)}</div>`; }
    });
  }
  function runCode() {
    const code = $('#code').value; if (cur) { store.code[cur.id] = code; save(); }
    const box = $('#results'); box.innerHTML = '<div class="out">Running…</div>'; setBusy(true);
    submit({ type: 'run', code }, {
      onProgress() { },
      onDone(m) { setBusy(false); box.innerHTML = (m.error ? `<div class="err">${esc(m.error)}</div>` : '') + `<div class="out">${esc(m.out || '(no output — use print() to see values)')}</div>`; },
      onFail(msg) { setBusy(false); box.innerHTML = `<div class="err">${esc(msg)}</div>`; }
    });
  }

  /* ---------------- terminal ---------------- */
  const log = (cls, txt) => { const l = $('#term-log'); const s = document.createElement('span'); s.className = cls; s.textContent = txt + '\n'; l.appendChild(s); l.scrollTop = l.scrollHeight; };
  function termRun() {
    const inp = $('#term-in'), code = inp.value; if (!code.trim()) return;
    inp.value = ''; log('cmd', '>>> ' + code.split('\n').join('\n... ')); setBusy(true);
    submit({ type: 'repl', code }, {
      onProgress() { },
      onDone(m) { setBusy(false); if (m.out) log('', m.out); if (m.result !== null && m.result !== undefined) log('res', m.result); if (m.error) log('er', m.error); },
      onFail(msg) { setBusy(false); log('er', msg); }
    });
  }

  /* ---------------- editor niceties ---------------- */
  $('#code').addEventListener('keydown', e => {
    const t = e.target;
    if (e.key === 'Tab') { e.preventDefault(); const s = t.selectionStart; t.setRangeText('    ', s, t.selectionEnd, 'end'); }
    else if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); runTests(); }
    else if (e.key === 'Enter') {
      const s = t.selectionStart, before = t.value.slice(0, s), line = before.slice(before.lastIndexOf('\n') + 1);
      const indent = (line.match(/^\s*/) || [''])[0] + (line.trimEnd().endsWith(':') ? '    ' : '');
      e.preventDefault(); t.setRangeText('\n' + indent, s, t.selectionEnd, 'end');
    }
  });
  $('#code').addEventListener('input', () => { if (cur) { store.code[cur.id] = $('#code').value; save(); } });
  $('#term-in').addEventListener('keydown', e => {
    if (e.key === 'Tab') { e.preventDefault(); e.target.setRangeText('    ', e.target.selectionStart, e.target.selectionEnd, 'end'); }
    else if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); termRun(); }
    else if (e.key === 'Enter' && !e.shiftKey && !e.target.value.includes('\n') && !e.target.value.trimEnd().endsWith(':')) { e.preventDefault(); termRun(); }
  });

  /* ---------------- wiring ---------------- */
  buildFilters();
  ['#q', '#f-diff', '#f-day', '#f-topic', '#f-company', '#f-track', '#f-evidence'].forEach(s => $(s).addEventListener('input', renderList));
  $('#plist').addEventListener('click', e => { const b = e.target.closest('button[data-id]'); if (b) open(b.dataset.id); });
  $('#run-tests').onclick = runTests; $('#run-code').onclick = runCode; $('#term-run').onclick = termRun;
  $('#term-clear').onclick = () => { $('#term-log').textContent = ''; };
  $('#reset').onclick = () => { if (cur && confirm('Reset to the starter code?')) { delete store.code[cur.id]; save(); $('#code').value = cur.starter; } };
  $('#show-sol').onclick = () => {
    const s = $('#sol'); s.hidden = !s.hidden;
    if (s.hidden) window.pauseSolutionWalkthrough();
    else window.mountSolutionWalkthrough(cur);
    $('#show-sol').setAttribute('aria-expanded', String(!s.hidden));
    $('#show-sol').textContent = s.hidden ? '💡 Reference solution & explanation' : 'Hide reference solution';
  };
  $('#clear-filters').onclick = () => {
    ['#q','#f-diff','#f-day','#f-topic','#f-company','#f-track','#f-evidence'].forEach(s => $(s).value = '');
    renderList();
  };
  window.addEventListener('hashchange', () => open(location.hash.slice(1), false));
  $('#toggle-side').onclick = () => $('#side').classList.toggle('open');
  const tab = which => {
    const t = which === 'terminal';
    $('#problems-view').hidden = t; $('#terminal-view').hidden = !t;
    $('#tab-problems').setAttribute('aria-selected', !t); $('#tab-terminal').setAttribute('aria-selected', t);
    if (t && !worker) spawn();
    if (t && !$('#term-log').textContent) log('res', 'Python terminal ready. Try:  [x*x for x in range(5)]');
  };
  $('#tab-problems').onclick = () => tab('problems'); $('#tab-terminal').onclick = () => tab('terminal');

  const qs = new URLSearchParams(location.search);
  if (qs.get('day')) { $('#f-day').value = qs.get('day'); }
  const start = location.hash.slice(1) || (filtered()[0] || PROBLEMS[0]).id;
  open(PROBLEMS.some(p => p.id === start) ? start : PROBLEMS[0].id, false);
  if (qs.get('tab') === 'terminal') tab('terminal');
  setTimeout(() => { if (!worker) spawn(); }, 600); // warm up Python in the background
})();
