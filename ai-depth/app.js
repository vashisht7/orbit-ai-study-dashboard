/* Original static reader. All lesson HTML comes from repository-authored Markdown. */
(() => {
  'use strict';
  const chapters = window.AI_DEPTH.chapters;
  const byId = new Map(chapters.map(c => [c.id, c]));
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const storageKey = 'orbit-ai-depth-v1';
  const levels = ['Not yet checked', 'Can explain', 'Can work the example', 'Can defend with evidence'];
  let state = {}, current = null;
  function validState(value) {
    const clean = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw Error('Expected a notes object.');
    for (const [id, entry] of Object.entries(value)) {
      if (!byId.has(id) || !entry || typeof entry !== 'object') continue;
      clean[id] = {level: Number.isInteger(entry.level) && entry.level >= 0 && entry.level <= 3 ? entry.level : 0,
        note: typeof entry.note === 'string' ? entry.note.slice(0, 30000) : ''};
    }
    return clean;
  }
  try { state = validState(JSON.parse(localStorage.getItem(storageKey) || '{}')); } catch { state = {}; }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); $('#save-status').textContent = 'Saved in this browser.'; }
    catch { $('#save-status').textContent = 'Browser storage is unavailable. Export your notes before leaving.'; }
  }
  function download(name, text, type) {
    const url = URL.createObjectURL(new Blob([text], {type}));
    const link = document.createElement('a'); link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  for (const [selector, values] of [['#project', [...new Set(chapters.flatMap(c => c.projects))]], ['#track', [...new Set(chapters.map(c => c.track))]]]) {
    values.forEach(v => { const o = document.createElement('option'); o.value = o.textContent = v; $(selector).append(o); });
  }
  for (let day = 1; day <= 30; day++) { const option = document.createElement('option'); option.value = String(day); option.textContent = `Day ${day}`; $('#day').append(option); }
  const requestedDay = Number(new URLSearchParams(location.search).get('day'));
  if (Number.isInteger(requestedDay) && requestedDay >= 1 && requestedDay <= 30) $('#day').value = String(requestedDay);
  function library() {
    const query = $('#search').value.toLowerCase().trim(), project = $('#project').value, track = $('#track').value;
    const day = Number($('#day').value);
    const visible = chapters.filter(c => (!day || c.days.includes(day)) && (!project || c.projects.includes(project)) && (!track || c.track === track)
      && (!query || [c.title, c.body, c.projects.join(' ')].join(' ').toLowerCase().includes(query)));
    let group = '';
    $('#chapters').innerHTML = visible.map(c => {
      const heading = group !== c.track ? `<h3>${esc(c.track)}</h3>` : ''; group = c.track;
      return `${heading}<a href="#${c.id}" ${c.id === current?.id ? 'class="active" aria-current="page"' : ''}>${state[c.id]?.level === 3 ? '✓ ' : ''}${c.number}. ${esc(c.title)}</a>`;
    }).join('') || '<p class="empty">No matching topics. Clear the search or filters.</p>';
    const defended = chapters.filter(c => state[c.id]?.level === 3).length;
    $('#progress').textContent = `${visible.length} topics shown · ${defended}/${chapters.length} self-rated “Can defend”`;
  }
  function link(id) { const c = byId.get(id); return `<a href="#${c.id}">${esc(c.title)}</a>`; }
  function overview() {
    const tracks = [...new Set(chapters.map(c => c.track))];
    const sources = new Set(chapters.flatMap(c => c.sources.map(s => s.url))).size;
    $('#lesson').innerHTML = `<p class="kicker">YOUR AI ENGINEERING FIELD GUIDE · REVIEWED OCTOBER 6, 2026</p>
      <h1>Your AI reference library.</h1>
      <p class="lead">Use these longer lessons when you want more detail about a topic. For everyday learning, follow one lesson at a time in Daily AI.</p>
      <div class="stat-row"><div class="stat"><b>${chapters.length}</b><span>personalized chapters</span></div><div class="stat"><b>27</b><span>tested Python examples</span></div><div class="stat"><b>${sources}</b><span>primary references</span></div><div class="stat"><b>4</b><span>system-design rehearsals</span></div></div>
      <div class="notice"><b>You do not need to choose another course.</b> Daily AI brings the foundation, example, and interview material together in the same 30-day order as your dashboard. This library keeps the complete explanations available for review.</div>
      <div class="actions"><a class="button" href="#overview">Back to my daily lesson →</a><a href="#interview-evidence">Review your résumé evidence checklist</a><a href="../reader/index.html">Open the detailed reference</a></div>
      ${$('#day').value ? `<section class="audit"><h2>Your Day ${Number($('#day').value)} deep dives</h2><ul>${chapters.filter(c => c.days.includes(Number($('#day').value))).map(c => `<li>${link(c.id)}</li>`).join('')}</ul><p>Use the day filter in Topics to return to all chapters.</p></section>` : ''}
      <h2>What needed more depth</h2>
      <div class="table-wrap"><table><thead><tr><th>Area</th><th>Existing foundation</th><th>Added interview depth</th></tr></thead><tbody>
      <tr><td>Classical ML and evaluation</td><td>Basic metrics and five bridge notes</td><td>${link('ml-decisions')}; ${link('evaluation-data')}</td></tr>
      <tr><td>Your classifier and ranker</td><td>General embeddings and model mechanics</td><td>${link('embeddings-ranking')}; ${link('design-mflash')}</td></tr>
      <tr><td>RAG and agents</td><td>Core pipelines and durability concepts</td><td>${link('advanced-rag')}; ${link('agent-evals')}; ${link('protocols')}</td></tr>
      <tr><td>Fine-tuning and modern reasoning</td><td>LoRA, QLoRA, and preference foundations</td><td>${link('adaptation')}; ${link('posttraining')}</td></tr>
      <tr><td>Production, data, and devices</td><td>Broad introductions</td><td>${link('data-engineering')}; ${link('distributed-training')}; ${link('local-ai')}</td></tr>
      <tr><td>Résumé defense</td><td>Daily interview prompts</td><td>Four worked system designs, failure scenarios, and evidence cards</td></tr>
      <tr><td>Specialist roles</td><td>Selected introductions</td><td>Speech, recommendation, vision, diffusion, time-series, and GNN orientation; specialized roles still need dedicated implementation and research practice</td></tr>
      </tbody></table></div>
      <h2>Reference areas</h2><p>Browse by subject when you want to revisit a concept. Your daily lesson already selects a relevant topic for you.</p>
      <ol class="roadmap">${tracks.map(t => { const items = chapters.filter(c => c.track === t); return `<li><a href="#${items[0].id}">${esc(t)}</a><small>${items.length} chapters · ${items.map(c => c.number).join(', ')}</small></li>`; }).join('')}</ol>
      <h2>Choose a topic</h2><div class="cards">${chapters.map(c => `<section class="card"><p class="kicker">${esc(c.track)} · ${c.number}</p><a href="#${c.id}">${esc(c.title)}</a><p>${esc(c.projects.join(' · '))}</p><p>${c.minutes} min reading + practice · Days ${c.days.join(', ')}</p></section>`).join('')}</div>
      <div class="audit"><h2>Scope, sources, and your résumé</h2><p>This is original teaching material researched on October 6, 2026. References distinguish published research, vendor guidance, and living implementation documentation. It is a dated snapshot; API details and checkpoint capabilities should be checked again when implementing.</p><p>All numerical examples are synthetic teaching cases unless explicitly identified otherwise. Project connections come from your résumé and the existing dashboard; the proposed designs are not claims about your shipped implementations. No résumé metrics have been invented or changed.</p><p>The original downloadable PDFs contain their earlier editions. This new material is available here and in the <a href="content.md">complete Markdown edition</a>; use “Print / save PDF” inside a chapter for an offline copy.</p></div>`;
  }
  function prepareBody(c) {
    const [before, after] = c.body.split('## Interview rehearsal\n');
    const [qa, exercise] = after.split('## Prove it yourself\n');
    const questions = qa.trim().split(/^### /m).filter(Boolean).map(text => {
      const split = text.indexOf('\n');
      return `<details class="interview"><summary>${esc(text.slice(0, split).trim())}</summary>${marked.parse(text.slice(split + 1))}</details>`;
    }).join('');
    return `${marked.parse(before)}<h2>Interview rehearsal</h2><p class="muted">Answer aloud before revealing the explanation. These are original practice prompts, not verified company interview questions.</p>${questions}<h2>Prove it yourself</h2>${marked.parse(exercise)}`;
  }
  function showChapter(c) {
    const saved = state[c.id] || {level:0, note:''};
    const index = chapters.indexOf(c);
    $('#lesson').innerHTML = `<p class="kicker">${esc(c.track)} · CHAPTER ${c.number} / ${chapters.length}</p><h1>${esc(c.title)}</h1>
      <div>${c.projects.map(p => `<span class="chip">${esc(p)}</span>`).join('')}<span class="chip">${c.minutes} min reading + practice</span></div>
      <div class="actions"><a href="#day-${c.foundation}">Learn this step by step · Day ${c.foundation}</a><a href="../practice.html#${c.practice}">Related Code Lab →</a><button id="print">Print / save PDF</button>${/```python/.test(c.body) ? '<button id="code-download">Download Python example</button>' : ''}</div>
      <p class="muted">Prerequisites: ${c.prereq.length ? c.prereq.map(link).join(' · ') : 'Start here; use the foundation link if a term is unfamiliar.'}</p>
      <section class="diagram" aria-label="Interactive concept diagram"><h2>Follow the mechanism</h2><p>Select a step. Explain what crosses each arrow before moving on.</p><ol class="flow">${c.flow.map(([label],i) => `<li><button data-step="${i}" aria-pressed="${i===0}"><b>0${i+1}</b>${esc(label)}</button></li>`).join('')}</ol><div class="flow-detail" aria-live="polite">${esc(c.flow[0][1])}</div></section>
      ${c.sim ? '<section class="simulator" id="simulator" aria-label="Interactive worked example"></section>' : ''}
      <nav class="outline" aria-label="In this chapter"></nav><div class="prose">${prepareBody(c)}</div>
      <details class="sources"><summary>Primary sources & implementation notes · checked October 6, 2026</summary><p>Use these references to verify mechanisms and implementation-specific details. Vendor results are not your project results; “latest” documentation can change after this review.</p><ul>${c.sources.map(s => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a></li>`).join('')}</ul></details>
      <section class="evidence"><h2>Make this yours</h2><p class="muted">A self-check, not an exam score. Save your mechanism, a failure case, and evidence from your actual work. Notes stay on this browser.</p><label for="rating">What can you do without notes?</label><select id="rating">${levels.map((l,i)=>`<option value="${i}" ${i===saved.level?'selected':''}>${l}</option>`).join('')}</select><label for="evidence-note">Your explanation or evidence card</label><textarea id="evidence-note" placeholder="Problem → my contribution → baseline → data/split → change → result → limitation → artifact" maxlength="30000"></textarea><p id="note-status" role="status"></p></section>
      <div class="pager">${index ? `<a href="#${chapters[index-1].id}">← ${esc(chapters[index-1].title)}</a>` : '<a href="#overview">← Coverage guide</a>'}${index < chapters.length-1 ? `<a href="#${chapters[index+1].id}">${esc(chapters[index+1].title)} →</a>` : '<a href="#overview">Return to coverage guide →</a>'}</div>`;
    $('#evidence-note').value = saved.note;
    document.querySelectorAll('[data-step]').forEach(b => b.onclick = () => {
      document.querySelectorAll('[data-step]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      $('.flow-detail').textContent = c.flow[Number(b.dataset.step)][1];
    });
    document.querySelectorAll('.prose h2').forEach((h,i) => {
      h.id = `section-${i}`; const b = document.createElement('button'); b.textContent = h.textContent;
      b.onclick = () => h.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
      $('.outline').append(b);
    });
    const update = () => {
      state[c.id] = {level: Number($('#rating').value), note: $('#evidence-note').value}; save(); library();
      $('#note-status').textContent = $('#save-status').textContent;
    };
    $('#rating').onchange = update; $('#evidence-note').oninput = update;
    $('#print').onclick = () => {
      const closed = [...document.querySelectorAll('details:not([open])')]; closed.forEach(d => d.open = true);
      window.print(); closed.forEach(d => d.open = false);
    };
    if ($('#code-download')) $('#code-download').onclick = () => {
      const blocks = [...c.body.matchAll(/```python\n([\s\S]*?)\n```/g)].map(m => m[1]);
      download(`${c.id}.py`, `# ${c.title}\n# Synthetic teaching example; not a production system.\n\n${blocks.join('\n\n')}\nprint('Example checks passed.')\n`, 'text/x-python');
    };
    if (c.sim) simulator(c.sim);
  }
  const controls = {
    threshold: ['Abstention: coverage versus error', [['threshold','Confidence threshold',50,100,85,1]], 'Predicted confidences and correctness are a fixed synthetic set. Move the threshold; no model is running.'],
    interval: ['Uncertainty around a pass rate', [['n','Independent trials',20,1000,100,10],['rate','Observed pass rate (%)',0,100,80,1]], 'A 95% Wilson interval for an illustrative binomial rate. The calculator rounds successes to a whole case; dependence or sampling bias invalidates this simple interpretation.'],
    kv: ['See KV memory grow', [['tokens','Cached tokens',512,32768,4096,512],['batch','Concurrent sequences',1,16,1,1],['bytes','Bytes per KV element',1,4,2,1]], 'Hypothetical full-attention model: 24 layers, 8 KV heads, head width 64. Cache only; excludes weights, activations, buffers, and allocator overhead.'],
    lora: ['Count a low-rank update', [['rank','Adapter rank',1,128,8,1],['width','Input and output width',128,4096,1024,128]], 'One square matrix; adapter parameters = rank × (input width + output width). Excludes bias, optimizer states, and other adapted matrices.'],
    routing: ['Budget a two-stage model cascade', [['escalation','Requests escalated (%)',0,100,25,1],['requests','Requests per day',100,100000,10000,100]], 'Hypothetical costs: 0.002 per small-model call and 0.020 per large-model call, in the same currency. Every request first pays for the small call. Not current vendor pricing.'],
    ranking: ['Move the most relevant result', [['position','Rank of the grade-2 result',1,3,2,1]], 'Three candidates have relevance grades 2, 1, and 0. The remaining candidates retain grade order. The example isolates rank position; it does not evaluate missing candidates.']
  };
  function simulator(kind) {
    const [title, fields, note] = controls[kind], box = $('#simulator');
    box.innerHTML = `<h2>${title}</h2><p>Predict the result, then change one setting.</p><div class="sim-controls">${fields.map(([id,label,min,max,value,step]) => `<label for="sim-${id}">${label} <b data-value="${id}">${value}</b><input id="sim-${id}" type="range" min="${min}" max="${max}" value="${value}" step="${step}"></label>`).join('')}</div><output class="sim-result" aria-live="polite"></output><div class="bar-track" aria-hidden="true"><div class="bar-fill"></div></div><p class="sim-note">${note}</p>`;
    const update = () => {
      const v = Object.fromEntries(fields.map(([id]) => [id, Number($(`#sim-${id}`).value)]));
      fields.forEach(([id]) => box.querySelector(`[data-value="${id}"]`).textContent = v[id]);
      let result, proportion;
      if (kind === 'kv') {
        const mib = 2*24*8*64*v.tokens*v.batch*v.bytes/2**20;
        result = `${mib.toLocaleString()} MiB of KV cache (${(mib/1024).toFixed(2)} GiB)`; proportion = mib / (2*24*8*64*32768*16*4/2**20);
      } else if (kind === 'lora') {
        const count = v.rank*2*v.width, fraction = count/(v.width*v.width);
        result = `${count.toLocaleString()} adapter parameters · ${(fraction*100).toFixed(2)}% of base matrix`; proportion = fraction;
      } else if (kind === 'routing') {
        const cost = .002 + v.escalation/100*.02;
        result = `${cost.toFixed(4)} per request · ${(cost*v.requests).toFixed(2)} per day`; proportion = cost/.022;
      } else if (kind === 'threshold') {
        const data = [[.99,1],[.97,1],[.95,0],[.92,1],[.89,1],[.85,0],[.8,1],[.75,0],[.65,1],[.55,0]];
        const accepted = data.filter(([p]) => p >= v.threshold/100), errors = accepted.filter(([,ok]) => !ok).length;
        result = `${accepted.length}/10 accepted · ${accepted.length ? (100*errors/accepted.length).toFixed(1)+'% error among accepted' : 'error undefined (no accepted cases)'}`; proportion = accepted.length/10;
      } else if (kind === 'interval') {
        const successes = Math.round(v.n*v.rate/100), p = successes/v.n, z = 1.96, d = 1+z*z/v.n;
        const center = (p+z*z/(2*v.n))/d, half = z*Math.sqrt(p*(1-p)/v.n+z*z/(4*v.n*v.n))/d;
        result = `${successes}/${v.n} passed · 95% interval: ${(100*(center-half)).toFixed(1)}%–${(100*(center+half)).toFixed(1)}%`; proportion = p;
      } else {
        const rel = [1,0]; rel.splice(v.position-1,0,2);
        const dcg = a => a.reduce((s,r,i)=>s+(2**r-1)/Math.log2(i+2),0);
        const ndcg = dcg(rel)/dcg([2,1,0]);
        result = `Grades [${rel.join(', ')}] · NDCG@3 = ${ndcg.toFixed(3)}`; proportion = ndcg;
      }
      box.querySelector('output').textContent = result;
      box.querySelector('.bar-fill').style.width = `${Math.max(0, Math.min(100, proportion*100))}%`;
    };
    box.querySelectorAll('input').forEach(x => x.oninput = update); update();
  }
  function show() {
    const id = location.hash.slice(1); current = byId.get(id) || null;
    const dayMatch = /^day-(\d+)$/.exec(id);
    const validDay = dayMatch && Number(dayMatch[1]) >= 1 && Number(dayMatch[1]) <= 30;
    const daily = !id || id === 'overview' || validDay;
    document.body.classList.toggle('daily-view', Boolean(daily));
    document.title = `${current?.title || 'Daily AI'} · Orbit`;
    if(daily) DAILY_STUDY.render(validDay ? Number(dayMatch[1]) : !id && Number.isInteger(requestedDay) && requestedDay >= 1 && requestedDay <= 30 ? requestedDay : DAILY_STUDY.next());
    else current ? showChapter(current) : overview();
    if (id && !['overview','library'].includes(id) && !current && !validDay) {
      const p = document.createElement('p'); p.className = 'notice'; p.textContent = 'That topic was not found. Choose a chapter below.'; $('#lesson').prepend(p);
    }
    document.querySelectorAll('#lesson table').forEach(t => {
      if (t.parentElement.classList.contains('table-wrap')) return;
      const wrap = document.createElement('div'); wrap.className = 'table-wrap'; t.replaceWith(wrap); wrap.append(t);
    });
    library(); $('#library').classList.remove('open'); $('#menu').setAttribute('aria-expanded','false'); window.scrollTo(0,0);
  }
  $('#search').oninput = library; $('#project').onchange = library; $('#track').onchange = library;
  $('.skip').onclick = e => { e.preventDefault(); $('#content').focus(); $('#content').scrollIntoView(); };
  $('#day').onchange = () => { library(); if (location.hash === '#library') overview(); };
  $('#menu').onclick = () => $('#menu').setAttribute('aria-expanded', String($('#library').classList.toggle('open')));
  $('#export').onclick = () => download('orbit-ai-evidence.json', JSON.stringify({version:1, exported:new Date().toISOString(), notes:state, daily:DAILY_STUDY.export()},null,2), 'application/json');
  $('#import').onchange = async e => {
    const file = e.target.files[0]; if (!file) return;
    try {
      if (file.size > 2_000_000) throw Error('File is too large. Choose an exported notes file under 2 MB.');
      const data = JSON.parse(await file.text());
      if (data.version !== 1) throw Error('This is not a supported Orbit notes export.');
      state = {...state, ...validState(data.notes)}; if(data.daily) DAILY_STUDY.import(data.daily); save(); show(); $('#save-status').textContent = 'Notes imported; matching topics replaced by your saved copy.';
    } catch (err) { $('#save-status').textContent = `Import failed: ${err.message}`; }
    e.target.value = '';
  };
  window.addEventListener('hashchange', show); show();
  document.addEventListener('click', e => { if(e.target.closest('a[href="#overview"]') && location.hash === '#overview') { e.preventDefault(); show(); } });
})();
