/* A single daily route over the existing foundation and interview material. */
window.DAILY_STUDY = (() => {
  const key = 'orbit-ai-daily-v1';
  const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const topicIds = ['ml-decisions','optimization','ml-decisions','classical-ranking','embeddings-ranking','optimization','evaluation-data','optimization','modern-transformers','modern-transformers','inference','inference','context','embeddings-ranking','retrieval-indexes','advanced-rag','durable-agents','durable-agents','ai-security','protocols','agent-evals','production','data-engineering','adaptation','posttraining','local-ai','interview-evidence','design-enterprise','evaluation-data','distributed-training'];
  const answers = [
    'The model proposes an interpretation. Your application validates the fields, checks permissions, and records whether the action actually succeeded.',
    'Each row produces one output by combining the two input values. Three rows therefore produce three numbers.',
    'Softmax compares the model’s scores. It does not check facts. High probability can accompany a wrong answer or unfamiliar input.',
    'An unseen pair has zero observed count. Smoothing or a fallback can avoid treating it as impossible; the tiny count model still has limited context.',
    'Compatible encoders place queries and documents in a shared space. Equal vector dimensions alone do not make two models’ coordinates comparable.',
    'A large step can overshoot a useful region or make the loss unstable. Compare the loss trajectory while changing only the learning rate.',
    'Choose the unit that would otherwise leak information across splits. Keep chunks of one document together, and use time splits when evaluating future events.',
    'Normalization controls numerical scales inside the computation. Regularization constrains learning to help generalization. They solve different problems.',
    'Attention scores say how much to use each item. Values contain the information to mix. Returning scores alone would not produce that information mixture.',
    'In [batch, sequence, vocabulary] logits, the middle axis is token position and the last axis contains candidate next-token scores.',
    'Query heads can share keys and values. Cache memory counts the K/V tensors actually stored, so it uses KV heads rather than query heads.',
    'FlashAttention reorganizes attention computation and memory access. Speculative decoding proposes multiple tokens and verifies them with a target model.',
    'A schema checks structure and types. It cannot prove that a value came from the right source, means what the user intended, or is authorized.',
    'Compare approximate retrieval with exact search using the same embeddings. If exact search is also poor, investigate representation, data, or relevance labels.',
    'Check whether the required evidence was retrieved and entered the context. The generator cannot reliably recover a missing source fact.',
    'Use a graph when explicit relationships or broad corpus structure improve measured answers enough to justify extraction, updates, and additional failure modes.',
    'Use a stable operation ID and a service-supported idempotency or reconciliation contract. A retry must not blindly repeat an uncertain side effect.',
    'The external action may finish just before the checkpoint is saved. On restart, reconcile the result or use idempotency instead of assuming it never happened.',
    'Application-enforced permissions, resource isolation, and constrained execution still protect the boundary even when the model proposes the wrong action.',
    'Verify identity, intended service audience, resource scope, current permissions, and result semantics. A well-shaped message can still request a forbidden action.',
    'Yes. Accuracy averages all cases. A model can miss rare important cases or make costly false positives while keeping the same overall accuracy.',
    'Time to first token includes waiting and prefill. Inter-token latency measures later generation; improving the queue need not change decoding speed.',
    'Keep the input/source versions, prompt, model, adapter, index, configuration, and relevant trace. Redact sensitive content while retaining reproducible identifiers.',
    'Merging, conversion, and quantization change the deployed computation. Test the actual artifact on the same held-out cases instead of assuming training gains survive.',
    'A system may exploit an incomplete reward, for example by being short but unhelpful. Evaluate independent user outcomes and search for reward shortcuts.',
    'Compare original audio, transcript, structured intent, and executed result. The first incorrect boundary identifies where investigation should begin.',
    'State the exact baseline, metric, denominator, data split, and your contribution. If evidence is missing, say so rather than inventing a result.',
    'Define release criteria first. Unsupported answers, forbidden actions, poor task success, or unacceptable latency can make a capstone unready.',
    'Keep evaluation inputs, model, prompt, data/index version, runtime conditions, and scoring policy fixed so the changed setting is the plausible cause.',
    'The repeated toy corpus tests mechanics and memorization. Independent data and broader tasks are needed to show general language quality.'
  ];
  let state = {};
  function clean(value) {
    const result = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) return result;
    for(let d=1;d<=30;d++) {
      const x=value[d];if(!x || typeof x!=='object')continue;
      result[d]={step:Number.isInteger(x.step)&&x.step>=0&&x.step<3?x.step:0,done:x.done===true,note:typeof x.note==='string'?x.note.slice(0,30000):''};
    }
    return result;
  }
  try{state=clean(JSON.parse(localStorage.getItem(key)||'{}'));}catch{}
  function save(){try{localStorage.setItem(key,JSON.stringify(state));return 'Saved in this browser.';}catch{return 'Browser saving is unavailable. Use Library → Export my notes before leaving.';}}
  function next(){return Array.from({length:30},(_,i)=>i+1).find(d=>!state[d]?.done)||30;}
  function md(text){
    const blocks=[];
    text=text.replace(/^```[^\n]*\n[\s\S]*?^```/gm,m=>{blocks.push(marked.parse(m));return '\n\nDAILYBLOCK'+(blocks.length-1)+'END\n\n';});
    text=text.replace(/^\$\$ (.+) \$\$$/gm,(_,m)=>{blocks.push('<div class="equation">'+katex.renderToString(m,{displayMode:true,throwOnError:false})+'</div>');return '\n\nDAILYBLOCK'+(blocks.length-1)+'END\n\n';});
    text=text.replace(/\$([^$\n]+)\$/g,(_,m)=>katex.renderToString(m,{throwOnError:false}));
    return marked.parse(text).replace(/<p>DAILYBLOCK(\d+)END<\/p>/g,(_,i)=>blocks[Number(i)]);
  }
  function render(day){
    const g=LESSON_GUIDES[day-1], foundation=BEGINNER[day-1], chapter=AI_DEPTH.chapters.find(c=>c.id===topicIds[day-1]);
    const entry=state[day] ||= {step:0,done:false,note:''};
    const parts=foundation.body.split(/(?=^### )/m).filter(x=>x.trim());
    const example=parts.find(x=>x.includes('```python')) || parts.find(x=>/example|walk|numbers/i.test(x.split('\n')[0])) || parts[1] || parts[0];
    const exampleHtml=example.length>5000 ? `<p>This workshop has a longer program. Start with the small example above, then open the full code when you are ready.</p><details><summary>Open the complete workshop example</summary><div class="prose">${md(example)}</div></details>` : `<div class="prose">${md(example)}</div>`;
    const questionBlock=chapter.body.split('## Interview rehearsal\n')[1].split('## Prove it yourself\n')[0].trim().split(/^### /m).filter(Boolean)[0];
    const qline=questionBlock.indexOf('\n');
    const practice=window.HELLO_PROBLEMS?.[g.problem] || `../practice.html#${g.problem}`;
    const completed=Object.values(state).filter(x=>x.done).length;
    const stage=['Learn the idea','See it work','Explain it yourself'];
    document.title=`Day ${day}: ${g.title} · Daily AI`;
    document.querySelector('#lesson').innerHTML=`
      <div class="daily-top"><a href="../index.html#day-${day}">← Day ${day} dashboard</a><span>${completed} of 30 days practiced</span></div>
      <div class="daily-progress" aria-label="${completed} of 30 days practiced"><span style="width:${completed/30*100}%"></span></div>
      <div class="daily-heading"><p class="kicker">DAY ${day} OF 30 · ABOUT 25–40 MINUTES · YOUR PACE</p><h1>${esc(g.title)}</h1><p class="lead">${esc(g.summary)}</p></div>
      <details class="day-picker"><summary>Choose another day</summary><div class="day-grid">${LESSON_GUIDES.map(x=>`<a href="#day-${x.day}" ${x.day===day?'aria-current="page"':''}><b>${state[x.day]?.done?'✓ ':''}Day ${x.day}</b><span>${esc(x.title)}</span></a>`).join('')}</div></details>
      <nav class="daily-steps" aria-label="Today's learning steps">${stage.map((s,i)=>`<button data-daily-step="${i}" aria-pressed="${entry.step===i}"><span>${i+1}</span>${s}</button>`).join('')}</nav>
      <section class="daily-panel" aria-label="${stage[entry.step]}">
      ${entry.step===0?`<p class="kicker">01 · UNDERSTAND ONE IDEA</p><h2>Start here</h2><div class="prose">${md(parts.slice(0,2).join('\n'))}</div><section class="diagram"><h2>Follow the steps</h2><ol class="flow">${g.steps.map(([name],i)=>`<li><button data-daily-flow="${i}" aria-pressed="${i===0}"><b>${i+1}</b>${esc(name)}</button></li>`).join('')}</ol><p class="flow-detail" aria-live="polite">${esc(g.steps[0][1])}</p></section>`:''}
      ${entry.step===1?`<p class="kicker">02 · MAKE IT CONCRETE</p><h2>A small example</h2><div class="simple-example">${esc(g.example)}</div><p>Predict what will happen before reading the explanation. Then change one input and explain the difference.</p>${exampleHtml}<div class="actions"><a class="button" href="${esc(practice)}" ${practice.startsWith('https:')?'target="_blank" rel="noopener noreferrer"':''}>Practice this idea ${practice.startsWith('https:')?'on Hello Interview ↗':'in Code Lab →'}</a><a href="../beginner/labs/${esc(foundation.lab)}" download>Download the lesson example</a></div>`:''}
      ${entry.step===2?`<p class="kicker">03 · SAY IT IN YOUR OWN WORDS</p><h2>${esc(g.check)}</h2><p>Try a short answer aloud. Include an example from your work if you can.</p><details class="daily-answer"><summary>Show a simple answer</summary><p>${esc(answers[day-1])}</p></details><details class="daily-answer"><summary>One interview follow-up: ${esc(questionBlock.slice(0,qline))}</summary><div class="prose">${md(questionBlock.slice(qline+1))}</div></details><label for="daily-note">My explanation, or what I want to revisit</label><textarea id="daily-note" maxlength="30000" placeholder="The idea is… For example… It can fail when…"></textarea><p id="daily-save" role="status">Your notes and daily progress stay in this browser.</p>`:''}
      </section>
      <div class="daily-controls">${entry.step>0?'<button id="daily-back">← Previous step</button>':'<span></span>'}${entry.step<2?`<button class="primary" id="daily-next">${stage[entry.step+1]} →</button>`:`<button class="primary" id="daily-done">${entry.done?'Practiced ✓ · Undo':'Mark this day practiced'}</button>`}</div>
      ${entry.done?`<div class="daily-finished"><p>You marked Day ${day} practiced. Revisit it whenever you need.</p>${day<30?`<a class="button primary" href="#day-${day+1}">Next: Day ${day+1} →</a>`:'<a href="#overview">Review your learning path →</a>'}</div>`:''}
      <section class="daily-extra"><h2>More detail, when you need it</h2><p>The full lessons are here. You do not have to finish every detail in one sitting.</p><details><summary>Read the complete foundation lesson</summary><div class="prose">${md(foundation.body)}</div></details><details><summary>Connect this to your AI interviews · ${esc(chapter.title)}</summary><div class="prose">${md(chapter.body)}</div><a href="#${chapter.id}">Open diagrams, calculators, and sources →</a></details><details><summary>Related topics and sources</summary><ul>${AI_DEPTH.chapters.filter(c=>c.days.includes(day)).map(c=>`<li><a href="#${c.id}">${esc(c.title)}</a></li>`).join('')}</ul><p><a href="../beginner/references.html">Foundation sources</a> · <a href="#${chapter.id}">Interview lesson sources</a></p><p class="muted">The example numbers are teaching examples, not measurements from your projects.</p></details></section>`;
    const rerender=()=>{save();render(day);document.querySelector('.daily-steps').scrollIntoView({block:'start'});};
    document.querySelectorAll('[data-daily-step]').forEach(b=>b.onclick=()=>{entry.step=Number(b.dataset.dailyStep);rerender();});
    document.querySelectorAll('[data-daily-flow]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-daily-flow]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelector('.flow-detail').textContent=g.steps[Number(b.dataset.dailyFlow)][1];});
    if(document.querySelector('#daily-next'))document.querySelector('#daily-next').onclick=()=>{entry.step++;rerender();};
    if(document.querySelector('#daily-back'))document.querySelector('#daily-back').onclick=()=>{entry.step--;rerender();};
    if(document.querySelector('#daily-done'))document.querySelector('#daily-done').onclick=()=>{entry.done=!entry.done;rerender();};
    const note=document.querySelector('#daily-note');
    if(note){note.value=entry.note;note.oninput=()=>{entry.note=note.value;document.querySelector('#daily-save').textContent=save();};}
    document.querySelectorAll('#lesson table').forEach(t=>{const wrap=document.createElement('div');wrap.className='table-wrap';t.replaceWith(wrap);wrap.append(t);});
  }
  return {render,next,export:()=>clean(state),import:value=>{state={...state,...clean(value)};save();}};
})();
