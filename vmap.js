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
    ['Foundations', ['Vectors, matrices, dot products', 'Loss, gradients, learning rate', 'Softmax & temperature'], dl(1, 3), 'Your NoteEchoes confidence threshold (0.75) is a softmax cutoff.'],
    ['Transformers', ['Tokens → embeddings', 'Self-attention (Q,K,V) + causal mask', 'RoPE position, KV cache, GQA'], dl(4, 7), 'Qwen 0.6B: 28 layers, 16 Q-heads / 8 KV-heads.'],
    ['Prompting & structure', ['In-context learning', 'Constrained / JSON decoding', 'Context engineering'], dl(8, 8), 'CoreV5 schema masks invalid tokens while decoding.'],
    ['Retrieval & RAG', ['Embeddings & vector search', 'BM25 + dense hybrid, RRF', 'Recall@k vs faithfulness'], dl(9, 14), 'SQLite FTS5 + E5 on device; Ragas/TruLens at BofA.'],
    ['Agents & safety', ['Tool calling = contract', 'Human-in-the-loop, guardrails', 'Durable state, prompt injection'], dl(15, 18), 'Model proposes, Swift gate + EventKit executes.'],
    ['Adaptation', ['LoRA / QLoRA / rsLoRA', 'DPO & preference learning', 'Eval-gated merging'], dl(19, 21), 'rsLoRA r=32 α=64 → scale 11.31; NF4 dequantized merge.'],
    ['Serving & quantization', ['vLLM, PagedAttention, batching', 'INT8 / INT4 (AWQ) / FP8', 'TTFT vs TPOT, capacity planning'], dl(22, 23), 'vLLM on Azure at BofA; INT8 649 MB on iPhone.'],
    ['On-device AI', ['Unified memory (UMA) zero-copy', 'MLX GPU + ANE for Whisper', 'Bandwidth-bound decoding'], dl(24, 26), 'tokens/s ≈ 50 GB/s ÷ 0.65 GB ≈ 77.'],
    ['Evaluation & ops', ['Operational vs strict metrics', 'LLMOps, tracing, monitoring', 'Statistics you can defend'], dl(21, 23), '1,200 challenge rows; 100% operational pass.'],
    ['Interview ready', ['System-design mocks', 'Resume defense drills', 'Coding rounds (Code Lab)'], dl(27, 30), 'Defend the 40% extraction-efficiency claim.']
  ];
  $('#concept-map').innerHTML = C.map((c, i) => `<div class="cnode" style="--nc:${WC[i % 5]}"><h4>${esc(c[0])}</h4>
    <ul>${c[1].map(x => `<li>${esc(x)}</li>`).join('')}</ul>${c[2]}<div class="you">🎯 ${esc(c[3])}</div></div>`).join('');

  /* 3 · pipelines */
  const D = [
    ['How a token is generated', 'Transformer inference loop', [
      ['📝', 'Text', 'raw input', 'Your prompt as characters.'],
      ['🔢', 'Tokenizer', 'ids', 'BPE splits text into token ids. Qwen vocab = 151,936 → embedding table ≈ 155 MB at INT8.'],
      ['📍', 'Embed + RoPE', 'vectors', 'Each id becomes a vector (d=1024). RoPE rotates Q/K so attention knows relative position.'],
      ['🔍', 'Attention', 'Q·Kᵀ', 'Each token scores every earlier token: <span class="formula">softmax(QKᵀ/√d)·V</span>. Causal mask hides the future. K,V are cached.'],
      ['🧮', 'MLP ×28', 'layers', 'Per-token feed-forward. Attention + MLP repeat once per layer (28 in Qwen 0.6B).'],
      ['🎲', 'Logits → sample', 'softmax', 'Final vector → vocab scores → softmax(temperature) → pick next token, append, and loop.'],
      ['🔁', 'KV cache', 'reuse', 'Only the new token is computed; old K,V are read from cache. <span class="formula">2·L·H_kv·D_h·T·2 bytes</span> = 112 KB/token for NoteEchoes.']]],
    ['RAG end to end', 'Retrieve, then answer with evidence', [
      ['📄', 'Documents', 'source', 'PDFs, notes, filings.'],
      ['✂️', 'Chunk', '200-500 tok', 'Split with overlap. Bad chunking is the #1 hidden cause of "hallucination".'],
      ['🧬', 'Embed + index', 'dense + BM25', 'E5 vectors for meaning, BM25/FTS5 for exact names. Keep both.'],
      ['❓', 'Query', 'user ask', 'Optionally rewrite the query.'],
      ['🔀', 'Hybrid + RRF', 'fuse ranks', '<span class="formula">score = Σ 1/(60 + rank)</span>. No score normalization needed.'],
      ['🏅', 'Rerank', 'cross-encoder', 'Re-score top-25 jointly with the query (+35% on messy tables at BofA).'],
      ['🤖', 'LLM answers', 'grounded', 'Prompt holds only retrieved evidence. Instruct: say "not found" if absent.'],
      ['📏', 'Evaluate', 'Recall@k · Faithfulness', 'Recall@k=0 → retrieval bug. Evidence present but wrong answer → generation bug (TruLens groundedness).']]],
    ['Fine-tuning with LoRA / QLoRA', 'What you did for NoteEchoes & BofA', [
      ['🧊', 'Frozen base', 'NF4 4-bit', 'QLoRA stores base weights in 4-bit NormalFloat + double quantization; they are never updated.'],
      ['➕', 'Add A·B', 'rank r=32', 'Train two small matrices: ΔW = B·A. Params drop by ~100×.'],
      ['⚖️', 'Scale', 'α/√r', 'LoRA scales by α/r; <b>rsLoRA</b> by α/√r so high ranks stay stable: 64/√32 = 11.31.'],
      ['🏋️', 'Train', 'off-device', 'Backprop stores activations ≈ 3× inference RAM, so train on Mac/cloud, never on iPhone.'],
      ['🔗', 'Merge', 'dequantized base', 'Merge onto the <b>dequantized NF4</b> base (not plain FP16) → matches training behaviour; eval gates pass.'],
      ['📦', 'Quantize + ship', 'INT8 MLX', 'group-64 INT8 → 649 MB package, pinned commit + SHA-256.']]],
    ['Cloud serving with vLLM', 'Bank of America stack', [
      ['📥', 'Requests', 'many users', 'Prompts arrive at random times and lengths.'],
      ['🗓️', 'Scheduler', 'continuous batching', 'Each step it re-forms the batch: finished requests leave, new ones join (iteration-level).'],
      ['⚙️', 'Prefill', 'compute-bound', 'Process the whole prompt in parallel. Chunked prefill (512 tok) stops one big prompt from stalling others.'],
      ['📖', 'Decode', 'memory-bound', 'One token per step; reads all weights + KV. Batching raises arithmetic intensity.'],
      ['🧱', 'PagedAttention', 'KV blocks', 'KV cache split into fixed blocks like OS pages → no fragmentation, prefix sharing, 2-4× throughput.'],
      ['📡', 'Stream out', 'TTFT · TPOT', 'TTFT = wait to first token; TPOT = gap between tokens. Optimize both under load.']]],
    ['NoteEchoes on-device pipeline', 'Voice → approved reminder', [
      ['🎙️', 'Microphone', '16 kHz PCM', 'Audio stays on device (privacy).'],
      ['🧠', 'Whisper', 'Apple Neural Engine', 'Fixed-shape encoder-decoder → ANE at ~1-2 W.'],
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
      <div class="tps">${fit ? '≈ <b>' + (tps >= 10 ? Math.round(tps) : tps.toFixed(1)) + '</b> tokens/s' : '✗ does not fit'}</div></div>`;
    }).join('')}</div></div>`).join('');
    $('#qnote').textContent = ` · white line = usable memory (~${usable.toFixed(0)} GB); bars use a log scale.`;
  }
  $('#bw').addEventListener('input', drawQ); drawQ();

  /* 5 · coding map */
  const byTopic = {};
  PROBLEMS.forEach(p => (byTopic[p.topic] = byTopic[p.topic] || []).push(p));
  $('#coding-map').innerHTML = Object.keys(byTopic).sort().map(t => `<div class="pcard"><h4>${esc(t)}</h4>${byTopic[t].map(p =>
    `<a class="pl" href="practice.html#${p.id}"><span>${esc(p.title)}</span><span class="d-${p.diff}">${p.diff}</span></a>`).join('')}</div>`).join('');

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
