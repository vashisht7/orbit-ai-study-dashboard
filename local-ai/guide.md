# Local AI: understand your MLX projects

A companion to the 30 main lessons. New expanded track; earlier completion marks are preserved, not proof that you have read this new material. Illustrative project examples are not measured project claims.

## Day 1: What you actually download when you download a model

### Why this matters

You have run local models already. Understanding the package lets you tell which change could alter its behavior. A model is a numerical function; a runtime is the program that executes it.

### How it works

A checkpoint stores learned weights. Configuration describes how those numbers connect. A tokenizer maps text to token IDs; a chat template adds role and turn markers. MLX is an array-computation framework; MLX LM adds language-model loading, generation and adaptation. These pieces work together, but changing the runtime does not itself teach the weights anything.

### Rule, symbols and reasoning

output = decode(model(encode(formatted conversation))). Read this inside out: format messages, encode text as IDs, compute scores with weights, choose IDs, decode them as text. Application validation comes afterward.

### Worked example

For a NoteEchoes-style reminder, the model proposes text describing the action. Your application parses and checks it before creating a reminder. Downloading a different tokenizer can change the IDs even when the visible request stays the same.

### What changes and what it means

Changing the checkpoint changes learned numbers; changing the runtime changes how the computation is executed. Recording both makes failures reproducible.

### Try it in your own project

Inspect one existing model folder. Record the weight files, config, tokenizer, template, model revision and runtime version. Do not download another model for this exercise.

### Check your understanding

If your model generates text, has it automatically gained permission to create reminders?

Answer: No. Generation produces data. Application code and operating-system permission determine which actions can execute.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 2: Parameters, tensors and the memory budget

### Why this matters

A model name such as 7B tells you how many learned numbers it contains, not how much total RAM a running application will consume.

### How it works

A tensor is an array with a shape and a numeric representation. Parameter count counts stored learned values. Bit width measures storage per value. Eight bits make one byte, so multiplying parameters by bits and dividing by eight gives ideal weight bytes. Runtime memory also includes cache, intermediate results and overhead.

### Rule, symbols and reasoning

weight bytes ≈ P × b / 8; total live memory ≈ weights + KV cache + activations + runtime overhead. P is parameter count and b is average stored bits per parameter. GB here means 1,000,000,000 bytes; GiB means 1,073,741,824 bytes.

### Worked example

For an illustrative 1-billion-parameter model, ideal weights need 2 GB at 16 bits, 1 GB at 8 bits, or 0.5 GB at 4 bits. Real files include metadata and may leave some layers at higher precision.

### What changes and what it means

Reducing stored bits reduces the ideal weight component. Increasing context or batch size can still raise total runtime memory.

### Try it in your own project

Estimate the three sizes for your model, then compare with actual file size. List possible reasons for the difference before measuring process memory.

### Check your understanding

Does a 4 GB model file guarantee it can run in 4 GB of free RAM?

Answer: No. File size is only part of the live memory budget, and context and temporary allocations can increase the peak.

Further reading: [MLX quantization API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html)

## Day 3: Storage precision is different from sampling temperature

### Why this matters

Both quantization and temperature can change the words you see. They act at different stages, so confusing them makes experiments hard to interpret.

### How it works

Quantization changes the representation of weights used to compute scores. Temperature changes how existing scores become a sampling distribution. Greedy selection chooses the largest score directly. A sampled token probability is not a calibrated probability that an action is correct.

### Rule, symbols and reasoning

p_i = exp(z_i/T) / sum_j exp(z_j/T), for T > 0. z_i is the score for token i. Dividing by a smaller positive T increases score differences before normalization; the weights themselves remain unchanged.

### Worked example

Two next-token scores 2 and 1 produce probabilities about 0.73 and 0.27 at T=1; at T=0.5 they become about 0.88 and 0.12. A 4-bit conversion may change the scores before either calculation.

### What changes and what it means

Changing temperature changes selection probabilities while keeping weights fixed. Changing precision can change the scores themselves.

### Try it in your own project

Compare two temperatures on one fixed model. Then compare 8-bit and 4-bit with the same prompt and greedy decoding. Record these as two separate experiments.

### Check your understanding

Does lowering temperature recover information lost during weight quantization?

Answer: No. It changes token selection from the scores available; it does not restore the original weights.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 4: What 4-bit and 8-bit quantization really mean

### Why this matters

Quantization lets you store weights with fewer bits. To understand its tradeoff, follow one weight through compression and reconstruction.

### How it works

In a simple uniform scheme, choose a minimum a and maximum c, divide that interval into representable levels, and store the nearest level index. With b bits there are 2^b possible indices. Reconstruction maps the index back to an approximate weight. This is a teaching scheme; real formats may use groups, nonuniform levels or different scaling conventions.

### Rule, symbols and reasoning

s = (c − a)/(2^b − 1); q = clip(round((w − a)/s), 0, 2^b − 1); reconstructed w = a + s q. Here s is level spacing, w the original weight, and q the stored integer index. Without clipping, rounding error is at most s/2.

### Worked example

On [−1,1], 4-bit has 16 levels and s=2/15≈0.1333. Weight 0.30 becomes index 10 and reconstructs as 0.3333. With 8-bit, s=2/255≈0.00784; index 166 reconstructs as 0.30196. More levels reduce this particular rounding error.

### What changes and what it means

Fewer bits mean fewer representable levels within a chosen range. Storage falls, but rounding can change predictions.

### Try it in your own project

Calculate both reconstructions for −0.42. Explain why a smaller weight error does not automatically imply a proportionate improvement in application accuracy.

### Check your understanding

Does 4-bit mean a model has only four possible weights?

Answer: No. Four bits encode 16 indices per quantization group; group scales and offsets map those indices to reconstructed values.

Further reading: [MLX quantization API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html)

## Day 5: Group size, scales and quantization overhead

### Why this matters

A single unusually large weight can force a coarse scale for many small weights. Grouping lets different portions of a matrix use different ranges.

### How it works

A group is a set of weights sharing quantization metadata. Smaller groups can fit local ranges more closely, but need more metadata. Storage precision and computation precision are separate: packed weights can be reconstructed and used in higher-precision arithmetic. A label such as 4-bit does not specify the whole format.

### Rule, symbols and reasoning

ideal storage bits ≈ P b + ceil(P/g) m. P is weight count, b bits per packed weight, g weights per group, and m metadata bits per group. This estimate ignores padding and unquantized tensors.

### Worked example

For 1,024 weights at 4 bits with a 16-bit scale and a 16-bit offset per group, g=64 needs 512+64=576 bytes. At g=32 it needs 512+128=640 bytes. The second layout spends more space on local scales.

### What changes and what it means

Smaller groups spend more bytes on metadata and can represent local ranges more closely. Quality and speed still require measurement.

### Try it in your own project

Read your converted model's quantization configuration: bits, group size, mode and any layer exceptions. Compare two versions only after recording all four.

### Check your understanding

Are two models labeled 4-bit necessarily numerically identical?

Answer: No. Group size, scaling method, calibration, original checkpoint and layer choices can all differ.

Further reading: [MLX quantization API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html)

## Day 6: What changes when you fine-tune a local model

### Why this matters

Inference uses learned weights to make a prediction. Fine-tuning uses examples and an error signal to change selected learned values. This connects your local projects to today's gradient lesson.

### How it works

Run a forward pass, compare the prediction with the desired target, differentiate that loss with respect to trainable parameters, then apply an optimizer update. A frozen parameter still participates in prediction but receives no update. Changing temperature is inference configuration; it is not fine-tuning.

### Rule, symbols and reasoning

For plain gradient descent: w_new = w_old − η × ∂L/∂w. η is the chosen learning rate; the derivative tells how loss changes locally as w changes. Real optimizers such as Adam also use accumulated state, so this is the simplest update rule, not their complete formula.

### Worked example

With prediction 2w, target 6 and loss (2w−6)^2, the gradient is 4(2w−6). At w=1 it is −16. With η=0.1 the update is +1.6, so w becomes 2.6 and loss falls from 16 to 0.64. A NoteEchoes adapter applies the same principle to many trainable values and language-model loss.

### What changes and what it means

Training changes selected parameters and therefore future predictions. A learning-rate change affects the next training update, not the weights of an already frozen inference run.

### Try it in your own project

For one of your fine-tuning configurations, identify what is trainable, what is frozen, which loss is minimized and which optimizer is used. Explain each before running training.

### Check your understanding

Does a negative gradient mean the weight should decrease?

Answer: For a positive learning rate in gradient descent, subtracting a negative gradient increases the weight. The gradient describes the uphill direction.

Further reading: [MLX quick start](https://ml-explore.github.io/mlx/build/html/usage/quick_start.html)

## Day 7: Fine-tuning examples, targets and validation splits

### Why this matters

A training run can learn formatting mistakes or memorize examples. Good data defines the behavior you want and gives you an honest way to check improvement.

### How it works

Supervised language-model fine-tuning predicts target tokens from preceding tokens. A loss mask selects which positions contribute to the objective; assistant-only loss focuses on response tokens. Train examples drive updates, validation selects settings, and a held-out test set assesses the final choice. Near-duplicate conversations crossing splits can overstate generalization.

### Rule, symbols and reasoning

L = −(1/N) sum_t m_t log p(target_t | earlier tokens), where m_t is 1 for a scored target position and 0 otherwise, and N=sum_t m_t. The minus sign turns low target probability into a large penalty.

### Worked example

For a reminder project, pair a user request with the desired structured proposal. If 'remind me tomorrow' appears in training and almost the same wording appears in testing, passing it gives weak evidence for unseen phrasing.

### What changes and what it means

Changing which tokens are scored changes the training objective. A better split changes how trustworthy your evaluation is, not the model directly.

### Try it in your own project

Inspect ten of your training conversations after template formatting. Mark the target tokens. Split by source or conversation family where appropriate, then look for duplicates across splits.

### Check your understanding

Can a falling training loss establish that unseen requests improved?

Answer: No. Check held-out examples, including ambiguous requests and failure cases, with application-level metrics.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 8: MLX lazy evaluation and automatic differentiation

### Why this matters

MLX code can describe calculations before executing them. This affects both how gradients are produced and how you time a computation.

### How it works

Lazy operations build a dependency graph. Evaluation materializes needed results. Automatic differentiation follows the computation to calculate derivatives; it does not select your learning rate or decide whether your data is good. MLX exposes function transformations such as grad and explicit evaluation through eval.

### Rule, symbols and reasoning

If f(w)=(2w−6)^2, grad(f)(w)=4(2w−6). This is the chain rule applied by software: outer square contributes 2(2w−6), inner expression contributes 2. Evaluating f and its gradient produces numbers for a particular w.

### Worked example

On a supported MLX installation, define f=lambda w:(2*w-6)**2, set w=mx.array(1.0), and compute g=mx.grad(f)(w). After mx.eval(g), g.item() is −16. This is a tiny numeric check, not a model training run.

### What changes and what it means

Explicit evaluation moves deferred numerical work into the measured region. Automatic differentiation supplies derivatives rather than choosing the training policy.

### Try it in your own project

Run that calculation in your existing MLX environment with import mlx.core as mx. When benchmarking larger operations, include evaluation inside the measured region, warm up first, and ensure the relevant work completes.

### Check your understanding

Why can timing only the creation of a lazy expression look unrealistically fast?

Answer: It may mostly time graph construction while the actual numerical work happens later when a result is evaluated.

Further reading: [MLX quick start](https://ml-explore.github.io/mlx/build/html/usage/quick_start.html)

## Day 9: Apple Silicon unified memory and device execution

### Why this matters

A local model must fit alongside your other applications. Shared physical memory reduces some transfers, but it does not remove the need to budget allocations.

### How it works

MLX arrays can be used by its CPU and GPU execution paths on Apple Silicon within unified memory. Computation still requires scheduling and synchronization. Unified memory does not mean every operation is free of temporary copies, nor does it mean MLX automatically executes on the Apple Neural Engine. Hardware support depends on the runtime and operation.

### Rule, symbols and reasoning

available budget = physical memory − operating-system use − other applications − safety headroom. This is a planning estimate; actual peak memory must be measured during your workload.

### Worked example

On an illustrative 16 GB machine, reserving 6 GB for the system, other apps and headroom leaves about 10 GB for the experiment. A 7B model's ideal 4-bit weights are 3.5 GB, but cache and temporary allocations still consume the remainder.

### What changes and what it means

Increasing workload consumes shared capacity. Moving work between supported devices changes scheduling and performance, not the mathematical goal.

### Try it in your own project

Record idle memory and peak memory for one existing model at two context lengths. Keep other applications and model settings stable. Compare results with your weight-only estimate from Day 2.

### Check your understanding

Does shared CPU/GPU memory make a 16 GB Mac equivalent to a machine with unlimited model memory?

Answer: No. CPU, GPU, applications and caches compete for the same finite physical capacity.

Further reading: [MLX unified memory](https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html)

## Day 10: Read the model configuration before guessing its shape

### Why this matters

A model's parameter count does not tell you its layer count, hidden width or number of cache heads. Those determine different costs.

### How it works

Hidden width is the length of each token representation. Layers repeat transformations. Attention query heads ask for information; key/value heads supply cached information. Grouped-query attention shares fewer key/value heads among more query heads. Exact dimensions belong to the checkpoint configuration, not to a generic family name.

### Rule, symbols and reasoning

A dense matrix with O output coordinates and I input coordinates has O×I weights, plus O biases if present. For standard attention, query projection width is H_q×d and key/value projection width is H_kv×d; H denotes head count and d head width.

### Worked example

An illustrative layer with I=1,024, H_q=16 and d=64 has 1,048,576 query-projection weights. If H_kv=4, its key projection has 262,144 weights. Fewer KV heads also reduce cache storage.

### What changes and what it means

Changing architecture changes the shapes and computation. Reading the configuration lets you calculate costs rather than borrow numbers from another model.

### Try it in your own project

Read your config and record hidden size, layers, query heads, KV heads and head dimension. Distinguish explicitly stored fields from values you derive under an architectural assumption.

### Check your understanding

Should you always use query-head count in a KV-cache memory calculation?

Answer: No. Use the number of key/value heads; in grouped-query attention it is smaller than query-head count.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 11: KV cache: why long conversations consume more memory

### Why this matters

During generation, the model repeatedly consults earlier tokens. Caching their keys and values avoids recomputing them, but memory grows with the stored context.

### How it works

Each attention layer saves a key vector and a value vector for each cached token and KV head. These are computed activations, separate from learned weights. Quantizing weights to 4 bits does not automatically quantize the cache to 4 bits.

### Rule, symbols and reasoning

KV bytes ≈ 2×L×B×T×H_kv×d×s. The 2 counts keys and values; L is layers, B batch size, T cached tokens, H_kv KV heads, d head width, and s bytes per cache number. This assumes a full dense cache without sliding windows, packing overhead or sharing.

### Worked example

For L=16, B=1, T=2,048, H_kv=4, d=64 and s=2, cache size is 33,554,432 bytes, or 32 MiB. Doubling T doubles this estimate, although total process memory need not double.

### What changes and what it means

Longer retained context increases cache storage. Fewer KV heads or fewer bytes per cache value reduce that component, with their own implementation and quality tradeoffs.

### Try it in your own project

Calculate your model's expected cache growth per additional 1,000 tokens. Compare two runs with fixed output length and different prompt lengths.

### Check your understanding

Why can a small quantized model still run out of memory on a long prompt?

Answer: Its weights may fit while the growing cache and temporary activations exceed remaining memory.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 12: Prefill, decode and useful latency measurements

### Why this matters

The delay before the first token and the speed of later tokens feel different to the user. One tokens-per-second number can hide that distinction.

### How it works

Prefill processes the prompt and prepares its cached representations. Decode produces successive output tokens, reusing the cache. Loading the model is another cost. Small-batch decode can be limited by moving weights through memory; prompt processing may use parallel computation more effectively. Neither bottleneck is universal.

### Rule, symbols and reasoning

total time ≈ load time + time to first token + (N−1)×mean later-token time, for N emitted tokens, with time to first token measured after loading. The definition of each timing boundary must stay consistent.

### Worked example

After a model is loaded, first token at 0.4 s plus 19 more tokens at 0.05 s each gives 1.35 s for 20 tokens. Reporting only 20 tokens/s hides the initial wait. These are illustrative numbers, not NoteEchoes measurements.

### What changes and what it means

A longer prompt mainly increases prompt processing and cache work; more output tokens extend decoding. Track both to explain perceived delay.

### Try it in your own project

Measure a short and a long prompt with the same model and output budget. Record cold load separately from warmed prefill and decode.

### Check your understanding

Will halving weight storage necessarily double generation speed?

Answer: No. Kernels, reconstruction work, cache traffic and other bottlenecks can change the result. Measure on your hardware.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 13: Chat templates, special tokens and structured output

### Why this matters

A fine-tuned model learned from a particular input format. A template mismatch can look like a weak model or a failed quantization even when neither is the cause.

### How it works

A chat template converts role-labeled messages into the exact text and special-token structure expected by the model. Tokenization then turns it into IDs. Stop tokens indicate completion. JSON instructions influence generation; a parser checks syntax and a schema checks required fields and types. Valid JSON alone does not establish a correct action.

### Rule, symbols and reasoning

messages → chat template → token IDs → model scores → generated IDs → decoded text → parse → schema and semantic checks. Each arrow has its own possible failure.

### Worked example

If your adapter saw assistant-start markers during training but inference omits them, it may continue the user text instead of answering. A proposal with valid JSON but tomorrow's wrong date is still an application failure.

### What changes and what it means

Correcting a template changes the sequence the model receives. Adding validation changes which generated proposals the application accepts.

### Try it in your own project

Compare the rendered training prompt and inference prompt for one identical conversation. Check role markers, stop IDs, added system text and whether a generation prompt is expected.

### Check your understanding

If a 4-bit model emits invalid JSON, what should you check before blaming bit width?

Answer: Check the same input/template, tokenizer, stop settings and output limit, then compare against the unconverted baseline on the same cases.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 14: Choose prompting, retrieval or fine-tuning by the failure

### Why this matters

You have several ways to improve a local application. Each changes a different part of the system and solves a different kind of problem.

### How it works

Prompting supplies instructions at inference. Retrieval supplies selected external information. Fine-tuning changes learned behavior through weight updates. New personal notes usually belong in a searchable store; a consistent output format may benefit from supervised examples. None of these makes application validation unnecessary.

### Rule, symbols and reasoning

prediction = f_weights(instructions, retrieved evidence, request). Prompting changes instructions, retrieval changes evidence, and fine-tuning changes weights. This expression is a dependency map rather than an arithmetic formula.

### Worked example

If NoteEchoes cannot find yesterday's note, updating its adapter is an indirect way to repair a missing retrieval result. If it finds the correct note but repeatedly produces the wrong field names, examine instructions, constraints or fine-tuning.

### What changes and what it means

Adding evidence changes what information is available now; adaptation changes learned behavior. Choosing the matching intervention avoids ineffective training.

### Try it in your own project

Sort ten real failures into missing knowledge, wrong behavior, inference configuration or application bug. Choose one intervention per group and state what would count as improvement.

### Check your understanding

Does fine-tuning on today's notes keep the model automatically synchronized with notes added tomorrow?

Answer: No. Training updates a particular snapshot. Retrieval can fetch newly indexed information without repeating that training.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 15: Local embeddings: index memory and compatibility

### Why this matters

A local retrieval system often needs an embedding model in addition to a generator. Its vectors and index consume memory and must remain compatible.

### How it works

An embedding maps text to a numeric vector for similarity search. Documents and queries must use compatible encoders and preprocessing. Changing the embedding model can change the coordinate system, so old document vectors often need recomputing. Generator quantization and embedding precision are separate settings.

### Rule, symbols and reasoning

raw vector bytes = N×D×s. N is number of document vectors, D their dimension, and s bytes per stored coordinate. This excludes index structures, document text and embedding-model weights.

### Worked example

10,000 note chunks with 384 float32 coordinates each require 10,000×384×4=15,360,000 bytes, about 15.36 MB before index overhead. Halving storage bytes per coordinate halves this component, but similarity quality needs checking.

### What changes and what it means

Changing vector dimensions or storage changes index memory. Changing encoders can require re-embedding every stored document.

### Try it in your own project

Record your encoder, vector dimension, normalization rule, chunking method and index format. Retrieve a fixed set of questions before and after any index change.

### Check your understanding

Can you swap the query embedding model while keeping unrelated old document vectors?

Answer: Their coordinates may no longer mean the same things. Rebuild or explicitly verify compatibility instead of assuming equal dimensions are sufficient.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 16: Build a fair 16-bit, 8-bit and 4-bit comparison

### Why this matters

A convincing comparison isolates precision. Otherwise a different prompt, model revision or generation limit may explain the outcome.

### How it works

Start from the same source checkpoint and keep tokenizer, template, task set and decoding settings fixed. Record quantization method and group size. Compare task quality, memory, first-token delay and generation speed. A smaller file can be useful even when speed barely changes, provided quality remains acceptable.

### Rule, symbols and reasoning

quality difference = converted pass rate − baseline pass rate. Memory saving fraction = 1 − converted peak memory / baseline peak memory. Compute both on matching workloads; distinguish total process memory from weight-file storage.

### Worked example

In an illustrative 100-case test, baseline passes 94, 8-bit passes 94 and 4-bit passes 91. Inspect which three cases changed; three date-extraction errors may matter more than three harmless wording differences.

### What changes and what it means

A controlled comparison exposes the benefit and regressions of conversion. It gives evidence for a deployment decision rather than relying on file names.

### Try it in your own project

Prepare a comparison table for your existing versions. Fill unknown measurements with 'not measured', not estimates. Include model revision, bits, groups, prompt settings, pass count, peak memory and timing.

### Check your understanding

Can a single pleasant answer prove the 4-bit version matches the baseline?

Answer: No. Use a fixed representative set and examine regressions by failure type, ideally with repeated timing runs.

Further reading: [MLX quantization API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html)

## Day 17: Full fine-tuning versus LoRA

### Why this matters

Updating every weight can require substantial memory. LoRA restricts the trainable change to a smaller factorized matrix while retaining the base model.

### How it works

For a linear layer, full fine-tuning learns changes to every element of W. LoRA freezes W and learns two smaller matrices whose product adds an adjustment. Rank r limits the factorization size. It is capacity you choose, not a direct quality score.

### Rule, symbols and reasoning

y=(W+sBA)x. W has shape [O,I], A [r,I], B [O,r]; s is an adapter scaling factor. Full weight count is OI; LoRA adds rI+Or=r(I+O) trainable values. The factorization is why fewer values can express a structured update.

### Worked example

For I=O=1,024 and r=8, full W has 1,048,576 values; A and B together have 16,384, or 1/64 as many. Across a whole model, the saving depends on which layers receive adapters.

### What changes and what it means

Increasing rank increases trainable adapter values and possible update capacity. It does not guarantee improved validation quality.

### Try it in your own project

Read your adapter configuration. List rank, scale, target modules and number of adapted layers. Calculate one layer's trainable parameter count.

### Check your understanding

Does LoRA's smaller parameter count mean its training is guaranteed to match full fine-tuning?

Answer: No. It constrains the available update. Data, target modules, rank, optimization and the task determine the result.

Further reading: [Original LoRA paper](https://arxiv.org/abs/2106.09685) · [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 18: QLoRA and the frozen quantized base

### Why this matters

LoRA reduces trainable state, but its frozen base can still be large. Quantizing that base reduces another major memory component.

### How it works

Quantized-base adapter training uses an approximate frozen base alongside trainable adapter values. Computation can use higher-precision reconstructed values. Original QLoRA's NF4 and double-quantization choices are specific methods; an MLX quantized adapter run does not automatically use the same format. Read the actual configuration.

### Rule, symbols and reasoning

y≈(W_reconstructed+sBA)x. W_reconstructed comes from the packed frozen base. Gradients update selected adapter parameters A and B. Quantized storage does not imply directly applying ordinary floating-point gradient updates to every packed integer code.

### Worked example

An illustrative 7B base has ideal 4-bit weight storage of 3.5 GB instead of 14 GB at 16 bits. Adapter parameters, gradients, optimizer state and activations still require extra memory; 3.5 GB is not the training budget.

### What changes and what it means

Quantizing the frozen base reduces its storage. Training adapters changes behavior while the packed base remains fixed.

### Try it in your own project

For your MLX fine-tune, identify the frozen-base quantization mode and the adapter dtype. Compare this with the settings of the model you actually serve.

### Check your understanding

Are all four-bit adapter runs numerically interchangeable with an NF4 QLoRA run?

Answer: No. Bit width alone does not identify the codebook, grouping, computation or original base. Match and test the actual artifacts.

Further reading: [Original QLoRA paper](https://arxiv.org/abs/2305.14314) · [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 19: Why training can run out of memory when inference fits

### Why this matters

Training must preserve information for backward computation and optimizer updates. A model that generates successfully may still exceed memory during fine-tuning.

### How it works

Weights, trainable gradients, optimizer state and saved activations contribute to memory. Sequence length and microbatch size affect activations. Gradient accumulation combines several smaller microbatches before an update. Checkpointing trades recomputation for fewer saved intermediate values. Neither technique removes every memory cost.

### Rule, symbols and reasoning

effective examples per update = microbatch size × accumulation steps × worker count, assuming equally sized batches. This is an example count; token-based loss normalization also matters when sequence lengths differ.

### Worked example

On one device, microbatch 1 with accumulation 8 collects eight examples before an update. It can lower the peak compared with processing all eight simultaneously, but takes multiple forward/backward passes and keeps accumulated gradients.

### What changes and what it means

Smaller microbatches usually reduce activation peaks. Accumulation changes how many examples contribute before an update; checkpointing adds recomputation.

### Try it in your own project

If an existing run fails, reduce sequence length or microbatch size one at a time and record peak memory. Consider accumulation to preserve examples per update; recheck optimization behavior.

### Check your understanding

Does accumulation by eight mean eight full activation graphs must stay in memory at once?

Answer: Normally no. Each microbatch can complete backward computation before the next; its gradients accumulate while most of its graph can be released.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 20: Learning rate, rank, epochs and overfitting

### Why this matters

Fine-tuning settings control different mechanisms. Raising all of them after a poor result gives you little explanation for what helped or harmed.

### How it works

Learning rate controls optimizer update scale. Rank controls adapter capacity. An epoch is one pass through the training examples. More passes can improve training fit while worsening unseen behavior. Compare training and validation trends, then inspect application failures.

### Rule, symbols and reasoning

updates per epoch ≈ ceil(N/E), where N is training examples and E effective examples per optimizer update, assuming batches are handled as stated. Standard LoRA often uses s=alpha/r; rank-stabilized LoRA uses alpha/sqrt(r). Changing rank without considering scaling changes more than capacity.

### Worked example

With 800 examples and 8 effective examples per update, one epoch is about 100 updates. Three epochs are about 300. If validation deteriorates after epoch one while training loss improves, more training is not automatically beneficial.

### What changes and what it means

More epochs mean more opportunities to fit the training data. Validation tells you whether this also helps unseen inputs.

### Try it in your own project

Write one hypothesis for your next run: learning rate too high, data too narrow or insufficient capacity. Change only the setting that tests it; save the validation outcome and checkpoint identity.

### Check your understanding

If a larger rank performs worse, does that prove LoRA is unsuitable?

Answer: No. Scaling, learning rate, data size, target layers and overfitting may explain it. Compare controlled runs.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 21: Evaluate adaptation on tasks you actually care about

### Why this matters

Loss measures token prediction, while your application needs usable outcomes. Evaluation connects training changes to user value.

### How it works

Define a pass condition before examining results. For structured actions, check parsing, required fields, intended action and argument correctness separately. Include ambiguous requests that should produce clarification. Keep your final test set out of training and repeated model selection.

### Rule, symbols and reasoning

pass rate = passed cases / tested cases. A paired comparison uses the same cases for both models: count newly passed cases and newly failed cases, rather than looking only at the total.

### Worked example

An adapter can improve JSON validity from 90/100 to 99/100 while reducing correct dates from 95/100 to 92/100. Better formatting does not erase the new date failures. These counts are an illustration, not your recorded project result.

### What changes and what it means

Separating failure types reveals whether an improvement is useful or merely cosmetic. A single average can hide a critical regression.

### Try it in your own project

Build a small labeled set from your project's actual failure categories. Run base and adapter under matching decoding settings; inspect disagreements before expanding the set.

### Check your understanding

Can a lower validation loss guarantee safer reminder creation?

Answer: No. Loss averages token prediction penalties. Application tests must check whether the proposed reminder matches the user's intent and whether approval rules hold.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 22: MLX model loading, generation and benchmarking

### Why this matters

A usable local workflow needs reproducible loading and inference before you add training. This becomes the baseline for every later comparison.

### How it works

MLX LM provides model and tokenizer loading plus text generation. Pin the package version and checkpoint revision, apply the checkpoint's expected chat template, and record generation settings. Separate model download, initial loading, warm-up and steady-state execution when measuring performance.

### Rule, symbols and reasoning

reproducible run = model revision + tokenizer/template + runtime version + generation settings + input set + device conditions. This is an experiment checklist: leaving one part unknown weakens a before/after comparison.

### Worked example

Two runs called 'Qwen 4-bit' can differ in checkpoint, group size, prompt markers and output limit. A faster run with half the output limit does not demonstrate a faster runtime.

### What changes and what it means

Pinning configurations makes later comparisons interpretable. Warming a model changes timing conditions and must be reported.

### Try it in your own project

In your installed environment, inspect python -m mlx_lm.generate --help. Use an already downloaded compatible model and one short request. Save the exact invocation and output; consult your installed version's help for supported flags.

### Check your understanding

Should download time be included in a warmed generation-throughput number?

Answer: No. Report download and load costs separately, while also reporting cold-start time when that is relevant to the user's experience.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 23: Merge, requantize and verify the served artifact

### Why this matters

The artifact you deploy can differ numerically from the one you evaluated during training. A successful merge command is not proof of unchanged behavior.

### How it works

An adapter may remain separate or be fused into a base weight matrix. If training used a quantized base, reconstructing that base differs from using the original higher-precision checkpoint. Requantizing a merged result adds rounding again. Supported merge paths depend on the runtime and model.

### Rule, symbols and reasoning

merged W = base W + sBA. In general, Q(W+sBA) ≠ Q(W)+sBA, because quantization Q rounds values. Likewise, reconstructed Q(W) need not equal the original W.

### Worked example

A toy base weight 0.30 reconstructed as 0.3333 plus an adapter change 0.02 gives 0.3533. Applying the same change to the original 0.30 gives 0.32 before any later rounding. Neither path can be assumed equivalent.

### What changes and what it means

Merging changes the stored artifact; requantizing can change its numerical behavior again. Re-evaluation tests what users will actually run.

### Try it in your own project

Record the exact base, adapter and merge settings. Evaluate the separate-adapter version, merged version and final quantized version on the same cases. Keep the last working artifact available.

### Check your understanding

Does dequantization recover the original high-precision weights exactly?

Answer: No. It reconstructs the quantized approximation. Information discarded by rounding is generally lost.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 24: An MLX adapter training workflow you can explain

### Why this matters

The main lesson derives LoRA. This companion turns that mechanism into a reproducible local experiment using your existing MLX experience.

### How it works

First evaluate the base. Prepare training and validation examples in a supported format. Inspect the installed MLX LM training options, select the trainable layers and settings, run a small experiment, then load its adapter with the matching base. An adapter file is not a standalone full language model.

### Rule, symbols and reasoning

baseline → formatted data → loss and gradients → adapter update → validation → saved adapter + matching base → held-out task test. Each stage has an artifact or measurement you can inspect.

### Worked example

For a reminder project, teach a consistent proposal format using varied requests and correct responses. Keep unseen names, dates and clarification cases for evaluation. A formatting gain accompanied by invented dates is not an acceptable overall improvement.

### What changes and what it means

A saved adapter carries learned adjustments. Serving it with the right base applies those adjustments; removing it returns to base behavior under the same settings.

### Try it in your own project

Inspect python -m mlx_lm.lora --help and the official MLX LM LoRA guide for your version. Write a run sheet containing base revision, data split, template, rank, target layers, learning rate, batch/accumulation, iteration budget and adapter output folder. Run a small local trial only when those choices are clear.

### Check your understanding

What must accompany the adapter when you reproduce an inference result?

Answer: The matching base and tokenizer/template, adapter configuration, runtime and decoding settings, plus the same input. The adapter alone does not define the full computation.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 25: Distillation and preference learning for smaller models

### Why this matters

After supervised fine-tuning, a model may still choose poor responses or be too expensive. Preference learning and distillation address different aspects of that problem.

### How it works

Preference data compares a preferred and a dispreferred response to the same prompt. Distillation trains a student using a teacher's outputs or probability distribution. A teacher can be wrong; generated data needs checking. Smaller student size and lower storage precision are separate ways to reduce resources.

### Rule, symbols and reasoning

For soft-target distillation, L = −sum_i q_i log p_i. q_i is the teacher's target probability for token i and p_i the student's prediction. Minimizing this encourages agreement with the teacher distribution, not automatic agreement with truth.

### Worked example

A larger model may draft reminder proposals for training a smaller local model. Validate dates and intent before accepting those examples. Separately, preference pairs can favor asking a necessary clarification over guessing.

### What changes and what it means

Distillation changes a student through teacher supervision. Preference learning changes which responses are favored. Both depend on the quality of their training signals.

### Try it in your own project

Create five preferred/dispreferred pairs and state a concrete reason for each. Review five teacher-generated examples for factual and format errors before adding any to a dataset.

### Check your understanding

Is a 4-bit version of a model automatically a distilled model?

Answer: No. Quantization changes numerical representation; distillation trains a student to imitate a teacher. They can be used together.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

## Day 26: Audio pipelines: find which model made the mistake

### Why this matters

A voice application includes several transformations. Fine-tuning the language model cannot reliably repair a fact that was lost before it received the transcript.

### How it works

Audio recognition produces text, the language model interprets it, and the application validates the proposed action. Each stage can introduce errors. The device used for each model depends on its runtime and conversion; do not assume every speech model runs on the Neural Engine.

### Rule, symbols and reasoning

end-to-end latency ≈ capture/endpointing + transcription + interpretation + validation/action, for sequential stages. Overlapped streaming changes the timing model. End-to-end accuracy cannot generally be found by multiplying unrelated benchmark accuracies.

### Worked example

If 'do not remind me today' becomes 'remind me today', a correctly functioning intent model may still propose the wrong action. Compare original audio, transcript and proposal to locate the failure.

### What changes and what it means

Repairing transcription changes the information reaching the language model. Repairing validation changes which actions are allowed after generation.

### Try it in your own project

Run the same intent request once from a verified text transcript and once through audio. If only the audio path fails, inspect recognition and endpointing before changing the adapter.

### Check your understanding

Why is word error rate alone insufficient for a reminder application?

Answer: One incorrect negation, name or date can change the action, while several harmless filler-word errors may not. Measure downstream intent and argument correctness too.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 27: Benchmark local models without misleading yourself

### Why this matters

Short tests can miss loading costs, thermal changes and variance. A useful report explains the workload and conditions behind each number.

### How it works

Use repeated runs with fixed prompts and output lengths. Report memory, quality, time to first token and later-token speed separately. Record device, power mode, runtime, context and concurrent workload. Compare warm runs fairly and keep cold-start measurements distinct.

### Rule, symbols and reasoning

mean latency = sum of run times / number of runs. Median is the middle sorted observation; p95 is a high percentile of the measured distribution. A p95 from very few runs is unstable and should not be presented as a production guarantee.

### Worked example

A 4-bit model may start faster because fewer bytes are loaded, yet decode at a similar speed because a different cost dominates. A long session may slow as thermal conditions change. Both observations can be real.

### What changes and what it means

Repeated measurements expose variability. Stable workload definitions help distinguish a model improvement from a favorable run.

### Try it in your own project

Repeat one representative request at least several times for each artifact. Save individual observations, not only their average. Explain the sample size and avoid claiming a precise tail latency from a tiny sample.

### Check your understanding

Can an isolated best-case timing defend a latency guarantee?

Answer: No. It demonstrates one run under one condition. Guarantees need representative workloads, enough observations and clearly defined boundaries.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 28: Choose a model by its quality–memory–latency tradeoff

### Why this matters

The smallest artifact is not always the best application choice, and the largest model is not always worth its cost. Selection needs explicit constraints.

### How it works

Set minimum task quality and maximum memory/latency budgets, then compare candidates that meet them. A larger 4-bit model and a smaller 8-bit model differ in both learned capacity and precision. Changing both is a product comparison, not an isolated quantization experiment.

### Rule, symbols and reasoning

candidate is feasible when quality ≥ required quality, peak memory ≤ memory budget, and measured latency ≤ latency budget. These conditions express your requirements; their thresholds must come from the application.

### Worked example

Suppose one candidate uses 3 GB with 92/100 task passes and another uses 5 GB with 97/100. If your device budget is 4 GB, the second cannot be selected unchanged. If the five failures are critical, the first may also be unacceptable.

### What changes and what it means

Explicit constraints can change the chosen model even when another has a better headline score. The decision is tied to your actual device and task.

### Try it in your own project

Build a decision table for your actual MLX artifacts. Explain one rejected candidate and one unresolved measurement. Consider routing or a simpler non-model solution when no candidate meets requirements.

### Check your understanding

Can you infer whether a 7B 4-bit model beats a 3B 8-bit model just from their names?

Answer: No. Architecture, training and task fit differ. Evaluate both under your application's constraints.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 29: Debug local inference one stage at a time

### Why this matters

A changed output has many possible causes. A controlled diagnosis prevents unnecessary retraining and helps you learn what each component does.

### How it works

Start from a saved working input and artifact. Check input formatting, tokenizer and stop settings, then base/adapter identity, conversion settings and runtime. For slowdowns, separate loading, prompt length, decode, memory pressure and thermal conditions. Change one suspected cause at a time.

### Rule, symbols and reasoning

observed difference = new run − baseline run, with all unrelated conditions held fixed where possible. This is an experimental comparison, not a claim that all effects add linearly.

### Worked example

If only the merged 4-bit version fails a date test while the separate adapter passes, inspect merge and conversion before collecting more training data. If both fail on the same audio transcript, check the transcript and task examples.

### What changes and what it means

Isolating one stage narrows the possible cause. A reproducible failing example makes a fix testable.

### Try it in your own project

Write a failure report with one minimal input, expected result, actual result, artifact versions and the first experiment that distinguishes two plausible causes.

### Check your understanding

What does 'try a lower learning rate' fail to explain when only inference is slow?

Answer: Learning rate controls training updates. Inference latency is more directly connected to workload, model size, kernels, memory and hardware conditions.

Further reading: [MLX LM generation and conversion](https://github.com/ml-explore/mlx-lm)

## Day 30: Capstone: defend your own local model release

### Why this matters

The goal is to explain the model you have used, not merely recognize terms. A small reproducible comparison makes the concepts concrete.

### How it works

Choose an existing project and follow one input through formatting, model computation, token selection and application validation. Compare a baseline with one adaptation or precision change. Preserve the artifact identities and test results needed to reproduce the conclusion.

### Rule, symbols and reasoning

release evidence = reproducible configuration + held-out task results + resource measurements + failure analysis + rollback artifact. This is a reasoning checklist, not a numerical quality score.

### Worked example

For a NoteEchoes-style project, explain why you selected a particular base and 4-bit or 8-bit representation, what the adapter learned, what stays outside the model, which cases still fail and what memory/latency you actually measured.

### What changes and what it means

Your final report turns tool familiarity into an explanation supported by measurements. Missing evidence becomes a clear next experiment.

### Try it in your own project

Produce a one-page report with your model/config inventory, three worked calculations from this track, a controlled comparison table, two inspected failures and your selection decision. Mark missing evidence explicitly. No new download or expensive training run is required to begin.

### Check your understanding

What distinguishes 'I used MLX and QLoRA' from understanding the system?

Answer: You can explain what the runtime executes, what is frozen or trained, how numbers are represented, why memory changes, how you verified quality and where your evidence stops.

Further reading: [MLX LM adapter training guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

