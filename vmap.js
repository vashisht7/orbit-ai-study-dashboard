/* Visual Map: renders journey, concept map, interactive pipelines, quantization chart, coding + site maps. */
(() => {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const WC = ['#38bdf8', '#34d399', '#a78bfa', '#fbbf24', '#f472b6'];

  /* 1 · journey */
  const weeks = (typeof WEEKS !== 'undefined' ? WEEKS : []);
  $('#journey-grid').innerHTML = [0, 1, 2, 3, 4].map(w => {
    const ds = DAYS.filter(d => d.week === w); if (!ds.length) return '';
    const meta = weeks[w] || ['Final stretch', '', '', ''];
    return `<div class="week" style="--wc:${WC[w]}"><h3>Stage ${w + 1} · ${esc(meta[0])} <small style="color:var(--dim);font-weight:400">${esc(meta[1])}</small></h3><p>${esc(meta[2])}</p>
      <div class="days">${ds.map(d => `<a class="day" href="index.html#day-${d.day}"><b>Day ${d.day}</b>
        <span>🧠 ${esc(((d.beginner && d.beginner[0] && d.beginner[0].title) || '').slice(0, 52))}</span>
        <em>💻 ${esc(d.coding)}</em></a>`).join('')}</div></div>`;
  }).join('');

  /* 2 · concept map */
  const dl = (a, b) => { const o = []; for (let i = a; i <= b; i++) o.push(`<a class="chip" href="index.html#day-${i}">D${i}</a>`); return o.join(''); };
  const C = [
    ['Foundations', ['Vectors and matrices', 'Softmax and gradients', 'Training and autograd'], dl(1, 8), 'Understand the small calculations before scaling up.'],
    ['Transformers', ['Attention and residual paths', 'Position and KV cache', 'Decoding and execution'], dl(9, 12), 'Check the actual model configuration for head counts.'],
    ['Prompting and structure', ['Task instructions and context', 'Schema and semantic validation'], dl(13, 13), 'Valid JSON can still describe a wrong action.'],
    ['Retrieval and RAG', ['Embeddings and access filters', 'Chunking, hybrid retrieval, RRF', 'Graph relationships'], dl(14, 16), 'Measure retrieval and answer quality separately.'],
    ['Agents and safety', ['Tool contracts and authorization', 'Durable state and retries', 'Prompt injection and protocols'], dl(17, 20), 'The application enforces permission to execute.'],
    ['Evaluation', ['Task success and classification', 'Retrieval metrics', 'Uncertainty and evaluation slices'], dl(21, 21), 'Always state the denominator and test population.'],
    ['Serving and operations', ['Latency, batching, quantization', 'Versioning and observability', 'Data lifecycle'], dl(22, 23), 'Toy memory estimates are not device benchmarks.'],
    ['Adaptation', ['LoRA, QLoRA, rsLoRA', 'Preferences and rewards', 'Distillation'], dl(24, 25), 'Re-evaluate the actual deployment artifact.'],
    ['Multimodal and on-device', ['Audio to text to structured intent', 'Provenance and validation'], dl(26, 26), 'Locate errors at representation boundaries.'],
    ['Interview and capstone', ['Coding and system design', 'Project evidence', 'Controlled experiments and decoder lab'], dl(27, 30), 'Use readiness checks instead of calendar completion.']
  ];
  $('#concept-map').innerHTML = C.map((c, i) => `<div class="cnode" style="--nc:${WC[i % 5]}"><h4>${esc(c[0])}</h4>
    <ul>${c[1].map(x => `<li>${esc(x)}</li>`).join('')}</ul>${c[2]}<div class="you">🎯 ${esc(c[3])}</div></div>`).join('');

  const guideSelect = $('#guide-select');
  guideSelect.innerHTML = window.LESSON_GUIDES.map(g => `<option value="${g.day}">Lesson ${g.day} · ${esc(g.title)}</option>`).join('');
  const showGuide = () => {
    $('#guide-card').innerHTML = window.renderLessonGuide(Number(guideSelect.value));
    $('#guide-lesson').href = `index.html#day-${guideSelect.value}`;
  };
  guideSelect.addEventListener('change', showGuide);
  const requestedDay = Number(new URLSearchParams(location.search).get('lesson'));
  if (requestedDay >= 1 && requestedDay <= 30) guideSelect.value = requestedDay;
  showGuide();
  const coverage = [
    ['Core model mechanics', 'Covered in depth', 2, 12, 'Vectors, losses, training, attention, transformers, and decoding.'],
    ['RAG and retrieval', 'Covered', 14, 16, 'Embeddings, chunking, fusion, source evidence, and graph trade-offs.'],
    ['Agents and safety', 'Covered', 17, 20, 'Tool boundaries, retries, state, prompt injection, and interfaces.'],
    ['Evaluation and statistics', 'Personalized deep dives added', 21, 21, 'Calibration, selective error, grouped splits, uncertainty, agent judges, and evidence cards.'],
    ['Serving and operations', 'Personalized deep dives added', 22, 23, 'Memory budgets, routing, sharding, Spark lineage, rollout, and recovery. Hands-on infrastructure practice still matters.'],
    ['Fine-tuning and alignment', 'Covered', 24, 25, 'Adapter mechanics, preference signals, and deployment evaluation.'],
    ['Multimodal and on-device', 'Personalized deep dives added', 26, 26, 'OCR field/document quality, voice error boundaries, SQLite recovery, and mobile design. Specialist research needs further practice.'],
    ['Classical ML, SQL, and Spark', 'Focused second pass added', 27, 27, 'Model baselines, classifier/ranker design, TF-IDF/PageRank, shuffles, temporal joins, and streaming correctness.'],
    ['Project and interview readiness', 'Covered as practice', 27, 30, 'Demonstrate tested behavior and measured results; no automatic readiness guarantee.']
  ];
  $('#coverage-grid').innerHTML = coverage.map(([title,status,a,b,note]) => `<article class="pcard"><h4>${esc(title)}</h4><b>${esc(status)}</b><p>${esc(note)}</p>${dl(a,b)}<p><a href="index.html#day-${a}">Open the full daily lesson →</a></p></article>`).join('');

  /* 3 · pipelines */
  const D = [
    ['How a token is generated', 'Transformer inference loop', [
      ['📝', 'Text', 'raw input', 'Your prompt as characters.'],
      ['🔢', 'Tokenizer', 'ids', 'The tokenizer maps text to vocabulary IDs. Vocabulary size and embedding storage depend on the exact checkpoint and representation.'],
      ['📍', 'Embed + RoPE', 'vectors', 'Each ID becomes a learned vector. RoPE modifies queries and keys inside attention to represent position.'],
      ['🔍', 'Attention', 'Q·Kᵀ', 'Each token scores every earlier token: <span class="formula">softmax(QKᵀ/√d)·V</span>. Causal mask hides the future. K,V are cached.'],
      ['🧮', 'MLP ×28', 'layers', 'Per-token feed-forward. Attention + MLP repeat once per layer (28 in Qwen 0.6B).'],
      ['🎲', 'Logits → sample', 'softmax', 'Final vector → vocab scores → softmax(temperature) → pick next token, append, and loop.'],
      ['🔁', 'KV cache', 'reuse', 'Only the new token is computed; old K,V are read from cache. <span class="formula">2·L·H_kv·D_h·T·2 bytes</span> is a generic estimate. Read layer count, KV heads, head dimension, and precision from your checkpoint.']]],
    ['RAG end to end', 'Retrieve, then answer with evidence', [
      ['📄', 'Documents', 'source', 'PDFs, notes, filings.'],
      ['✂️', 'Chunk', '200-500 tok', 'Split with overlap. Poor chunk boundaries can hide relevant evidence; diagnose retrieval before choosing a fix.'],
      ['🧬', 'Embed + index', 'dense + BM25', 'E5 vectors for meaning, BM25/FTS5 for exact names. Keep both.'],
      ['❓', 'Query', 'user ask', 'Optionally rewrite the query.'],
      ['🔀', 'Hybrid + RRF', 'fuse ranks', '<span class="formula">score = Σ 1/(60 + rank)</span>. No score normalization needed.'],
      ['🏅', 'Rerank', 'cross-encoder', 'Re-score candidate documents jointly with the query. Measure the quality gain and added latency on your dataset.'],
      ['🤖', 'LLM answers', 'grounded', 'Prompt holds only retrieved evidence. Instruct: say "not found" if absent.'],
      ['📏', 'Evaluate', 'Recall@k · Faithfulness', 'Low recall suggests inspecting retrieval and ground truth. If useful evidence is present, inspect context packing and generation next.']]],
    ['Fine-tuning with LoRA / QLoRA', 'What you did for NoteEchoes & BofA', [
      ['🧊', 'Frozen base', 'NF4 4-bit', 'QLoRA stores base weights in 4-bit NormalFloat + double quantization; they are never updated.'],
      ['➕', 'Add A·B', 'rank r=32', 'Train two small matrices: ΔW = B·A. Parameter savings depend on matrix dimensions and the chosen rank.'],
      ['⚖️', 'Scale', 'α/√r', 'LoRA scales by α/r; <b>rsLoRA</b> by α/√r so high ranks stay stable: 64/√32 = 11.31.'],
      ['🏋️', 'Train', 'off-device', 'Training needs gradients, optimizer state, and saved activations. Its memory budget depends on the training method and model.'],
      ['🔗', 'Merge', 'dequantized base', 'Merge onto the <b>dequantized NF4</b> base (not plain FP16) → matches training behaviour; eval gates pass.'],
      ['📦', 'Quantize + ship', 'INT8 MLX', 'group-64 INT8 → 649 MB package, pinned commit + SHA-256.']]],
    ['Cloud serving with vLLM', 'Bank of America stack', [
      ['📥', 'Requests', 'many users', 'Prompts arrive at random times and lengths.'],
      ['🗓️', 'Scheduler', 'continuous batching', 'Each step it re-forms the batch: finished requests leave, new ones join (iteration-level).'],
      ['⚙️', 'Prefill', 'compute-bound', 'Process the whole prompt in parallel. Chunked prefill splits prompt processing into scheduler-sized pieces to balance waiting and ongoing generation.'],
      ['📖', 'Decode', 'memory-bound', 'One token per step; reads all weights + KV. Batching raises arithmetic intensity.'],
      ['🧱', 'PagedAttention', 'KV blocks', 'KV cache split into fixed blocks like OS pages → less wasted allocation and possible prefix sharing; performance gains depend on workload.'],
      ['📡', 'Stream out', 'TTFT · TPOT', 'TTFT = wait to first token; TPOT = gap between tokens. Optimize both under load.']]],
    ['NoteEchoes on-device pipeline', 'Voice → approved reminder', [
      ['🎙️', 'Microphone', '16 kHz PCM', 'Audio stays on device (privacy).'],
      ['🧠', 'Whisper', 'Apple Neural Engine', 'Speech-to-text execution and power depend on the actual model, runtime, and hardware; measure the deployed build.'],
      ['🔤', 'Tokenizer', 'unified RAM', 'Text → ids; shared buffers (UMA, zero copy).'],
      ['🍎', 'Qwen 0.6B', 'MLX · GPU · INT8', 'Autoregressive decode on GPU. <span class="formula">tokens/s ≈ 50 GB/s ÷ 0.65 GB ≈ 77</span>.'],
      ['✅', 'CoreV5 validator', 'schema', 'Strict JSON envelope: intent, ISO time, confidence. Below 0.75 → ask to clarify.'],
      ['🛡️', 'Swift gate', 'permissions', 'App checks permission + date sanity; destructive actions need user confirm.'],
      ['📅', 'EventKit', 'sandbox', 'Only the app executes the action. The model never touches calendar APIs.']]],
    ['Agent loop (safe tool use)', 'Model proposes, system disposes', [
      ['👀', 'Observe', 'state', 'Read input + current persisted state.'],
      ['🗺️', 'Plan', 'LLM', 'Decide the next step.'],
      ['📨', 'Propose tool call', 'envelope', 'Name + args + confidence. It is data, not an action.'],
      ['🔒', 'Validate', 'deterministic', 'Type-check args, authorization, policy; untrusted text can never raise privileges.'],
      ['🙋', 'Human approval', 'if risky', 'Deleting / paying / sending → explicit confirmation.'],
      ['⚡', 'Execute', 'sandbox', 'Least-privilege executor.'],
      ['💾', 'Persist', 'durable', 'Write state after each phase so a crash or app suspend can resume without double-acting.']]]
  ];
  $('#dgrid').innerHTML = D.map((d, di) => `<div class="dcard" data-d="${di}"><h3>${esc(d[0])}</h3><div class="tag">${esc(d[1])}</div>
    <div class="flow">${d[2].map((s, i) => `${i ? '<span class="arrow">➜</span>' : ''}<button class="step${i ? '' : ' on'}" data-i="${i}" style="--sc:${WC[(di + i) % 5]}"><span class="i">${s[0]}</span><b>${esc(s[1])}</b><small>${esc(s[2])}</small></button>`).join('')}</div>
    <div class="detail"><b>${esc(d[2][0][1])}:</b> ${d[2][0][3]}</div></div>`).join('');
  $('#dgrid').addEventListener('click', e => {
    const b = e.target.closest('.step'); if (!b) return;
    const card = b.closest('.dcard'), s = D[+card.dataset.d][2][+b.dataset.i];
    card.querySelectorAll('.step').forEach(x => x.classList.remove('on')); b.classList.add('on');
    card.querySelector('.detail').innerHTML = `<b>${esc(s[1])}:</b> ${s[3]}`;
  });

  /* 4 · quantization chart */
  const MODELS = [['NoteEchoes · Qwen 0.6B', 0.6], ['3B small model', 3], ['LLaMA-3 8B (BofA)', 8], ['70B', 70]];
  const BITS = [['FP16', 16], ['INT8', 8], ['INT4', 4]];
  function drawQ() {
    const sel = $('#bw'), bw = +sel.value, ram = +sel.selectedOptions[0].dataset.ram;
    const cloud = /Cloud/.test(sel.selectedOptions[0].text), usable = ram * (cloud ? 0.9 : 0.65);
    const scale = v => 100 * Math.log10(v * 50 + 1) / Math.log10(140 * 50 + 1);
    $('#qchart').innerHTML = MODELS.map(([name, p]) => `<div class="qrow"><b>${esc(name)}</b><div class="bars">${BITS.map(([bn, b]) => {
      const gb = p * b / 8, fit = gb * 1.1 <= usable, tps = bw / gb;
      return `<div class="bar-line"><div class="track"><div class="fill ${fit ? 'fit' : 'nofit'}" style="width:${scale(gb)}%">${bn} · ${gb < 10 ? gb.toFixed(2) : gb.toFixed(1)} GB</div><div class="ram" style="left:${scale(usable)}%" title="usable memory"></div></div>
      <div class="tps">${fit ? 'Ideal ceiling ≈ <b>' + (tps >= 10 ? Math.round(tps) : tps.toFixed(1)) + '</b> tokens/s' : '✗ does not fit'}</div></div>`;
    }).join('')}</div></div>`).join('');
    $('#qnote').textContent = ` · white line = assumed usable memory (~${usable.toFixed(0)} GB); log-scale weight bars. KV cache, runtime, and real device limits require measurement.`;
  }
  $('#bw').addEventListener('input', drawQ); drawQ();

  /* 5 · coding map */
  const byTopic = {};
  PROBLEMS.forEach(p => (byTopic[p.topic] = byTopic[p.topic] || []).push(p));
  $('#coding-map').innerHTML = Object.keys(byTopic).sort().map(t => `<div class="pcard"><h4>${esc(t)}</h4>${byTopic[t].map(p =>
    `<a class="pl" href="${window.HELLO_PROBLEMS[p.id] || 'practice.html#' + p.id}" ${window.HELLO_PROBLEMS[p.id] ? 'target="_blank" rel="noopener"' : ''}><span>${esc(p.title)} · ${window.HELLO_PROBLEMS[p.id] ? 'Hello Interview ↗' : 'Code Lab'}</span><span class="d-${p.diff}">${p.diff}</span></a>`).join('')}</div>`).join('');

  /* 6 · site map */
  const S = [
    ['🎯 Dashboard', 'index.html', '30 levels, XP, streaks. Daily reading, local-AI card, resume drill, labs.'],
    ['⌨️ Code Lab', 'practice.html', `${PROBLEMS.length} problems with Python editor + test cases + reference solutions.`],
    ['🖥️ Python terminal', 'practice.html?tab=terminal', 'A real Python REPL in the browser; state persists.'],
    ['📚 Cheat sheet', 'cheatsheet.html', '28 topics incl. on-device AI, quantization, serving.'],
    ['🍎 Inside NoteEchoes', 'model-process.html', 'Model, training pipeline, eval and metrics.'],
    ['🎤 Interview bank', 'interviews.html', 'Explain, diagnose and defend questions.'],
    ['📖 Beginner book', 'beginner/index.html', 'Plain-language lessons, math and labs.'],
    ['🔬 Advanced reference', 'reader/index.html', 'Deeper chapters and laboratories.']
  ];
  $('#site-map').innerHTML = S.map(s => `<a class="pcard sitecard" href="${s[1]}"><h4>${s[0]}</h4><p>${esc(s[2])}</p></a>`).join('');
})();
