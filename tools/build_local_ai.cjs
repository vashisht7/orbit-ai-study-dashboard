const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const lessons = JSON.parse(fs.readFileSync(path.join(root, 'local-ai/lessons.json'), 'utf8'));
const changes = [
'Changing the checkpoint changes learned numbers; changing the runtime changes how the computation is executed. Recording both makes failures reproducible.',
'Reducing stored bits reduces the ideal weight component. Increasing context or batch size can still raise total runtime memory.',
'Changing temperature changes selection probabilities while keeping weights fixed. Changing precision can change the scores themselves.',
'Fewer bits mean fewer representable levels within a chosen range. Storage falls, but rounding can change predictions.',
'Smaller groups spend more bytes on metadata and can represent local ranges more closely. Quality and speed still require measurement.',
'Training changes selected parameters and therefore future predictions. A learning-rate change affects the next training update, not the weights of an already frozen inference run.',
'Changing which tokens are scored changes the training objective. A better split changes how trustworthy your evaluation is, not the model directly.',
'Explicit evaluation moves deferred numerical work into the measured region. Automatic differentiation supplies derivatives rather than choosing the training policy.',
'Increasing workload consumes shared capacity. Moving work between supported devices changes scheduling and performance, not the mathematical goal.',
'Changing architecture changes the shapes and computation. Reading the configuration lets you calculate costs rather than borrow numbers from another model.',
'Longer retained context increases cache storage. Fewer KV heads or fewer bytes per cache value reduce that component, with their own implementation and quality tradeoffs.',
'A longer prompt mainly increases prompt processing and cache work; more output tokens extend decoding. Track both to explain perceived delay.',
'Correcting a template changes the sequence the model receives. Adding validation changes which generated proposals the application accepts.',
'Adding evidence changes what information is available now; adaptation changes learned behavior. Choosing the matching intervention avoids ineffective training.',
'Changing vector dimensions or storage changes index memory. Changing encoders can require re-embedding every stored document.',
'A controlled comparison exposes the benefit and regressions of conversion. It gives evidence for a deployment decision rather than relying on file names.',
'Increasing rank increases trainable adapter values and possible update capacity. It does not guarantee improved validation quality.',
'Quantizing the frozen base reduces its storage. Training adapters changes behavior while the packed base remains fixed.',
'Smaller microbatches usually reduce activation peaks. Accumulation changes how many examples contribute before an update; checkpointing adds recomputation.',
'More epochs mean more opportunities to fit the training data. Validation tells you whether this also helps unseen inputs.',
'Separating failure types reveals whether an improvement is useful or merely cosmetic. A single average can hide a critical regression.',
'Pinning configurations makes later comparisons interpretable. Warming a model changes timing conditions and must be reported.',
'Merging changes the stored artifact; requantizing can change its numerical behavior again. Re-evaluation tests what users will actually run.',
'A saved adapter carries learned adjustments. Serving it with the right base applies those adjustments; removing it returns to base behavior under the same settings.',
'Distillation changes a student through teacher supervision. Preference learning changes which responses are favored. Both depend on the quality of their training signals.',
'Repairing transcription changes the information reaching the language model. Repairing validation changes which actions are allowed after generation.',
'Repeated measurements expose variability. Stable workload definitions help distinguish a model improvement from a favorable run.',
'Explicit constraints can change the chosen model even when another has a better headline score. The decision is tied to your actual device and task.',
'Isolating one stage narrows the possible cause. A reproducible failing example makes a fix testable.',
'Your final report turns tool familiarity into an explanation supported by measurements. Missing evidence becomes a clear next experiment.'
];
const sources = {
 mlx: ['MLX quick start', 'https://ml-explore.github.io/mlx/build/html/usage/quick_start.html'],
 memory: ['MLX unified memory', 'https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html'],
 quant: ['MLX quantization API', 'https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html'],
 lm: ['MLX LM generation and conversion', 'https://github.com/ml-explore/mlx-lm'],
 tune: ['MLX LM adapter training guide', 'https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md'],
 lora: ['Original LoRA paper', 'https://arxiv.org/abs/2106.09685'],
 qlora: ['Original QLoRA paper', 'https://arxiv.org/abs/2305.14314']
};
const refs = ['lm','quant','lm','quant','quant','mlx','tune','mlx','memory','lm','lm','lm','lm','tune','lm','quant','lora','qlora','tune','tune','tune','lm','tune','tune','tune','lm','lm','lm','lm','tune'];
if (lessons.length !== 30 || new Set(lessons.map(x=>x.title)).size!==30) throw Error('Need 30 distinct Local AI lessons');
let book = '# Local AI: understand your MLX projects\n\nA companion to the 30 main lessons. New expanded track; earlier completion marks are preserved, not proof that you have read this new material. Illustrative project examples are not measured project claims.\n\n';
lessons.forEach((l,i)=>{
 for(const key of ['title','why','how','formula','example','experiment','question','answer']) if(!l[key]) throw Error(`Day ${i+1} missing ${key}`);
 l.day=i+1;l.change=changes[i];l.sources=[sources[refs[i]]];
 if([17,18,23,24].includes(l.day)) l.sources.push(sources.tune);
 l.sources=l.sources.filter((s,j,a)=>a.findIndex(t=>t[1]===s[1])===j);
 l.body=`### Why this matters\n\n${l.why}\n\n### How it works\n\n${l.how}\n\n### Rule, symbols and reasoning\n\n${l.formula}\n\n### Worked example\n\n${l.example}\n\n### What changes and what it means\n\n${l.change}\n\n### Try it in your own project\n\n${l.experiment}\n`;
 book+=`## Day ${l.day}: ${l.title}\n\n${l.body}\n### Check your understanding\n\n${l.question}\n\nAnswer: ${l.answer}\n\nFurther reading: ${l.sources.map(([t,u])=>`[${t}](${u})`).join(' · ')}\n\n`;
});
fs.writeFileSync(path.join(root,'local-ai/course.js'),'// Generated by tools/build_local_ai.cjs from lessons.json.\nwindow.LOCAL_AI_LESSONS = '+JSON.stringify(lessons,null,2)+';\n');
fs.writeFileSync(path.join(root,'local-ai/guide.md'),book);
console.log('Built 30 distinct Local AI lessons and downloadable guide.');
