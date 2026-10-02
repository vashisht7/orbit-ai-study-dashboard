# AI Engineering Laboratory

This workbook accompanies the five concept volumes. It contains 20 CPU experiments, one actual tiny-transformer training exercise, and a local HTTP capstone. All documents and measurements in the core fixtures are fictional or synthetic. Real-model, GPU and protocol integrations are optional extensions and are not claimed to have run merely because the core checks pass.

## Start here

Use a fresh environment and Python 3.10 or newer. From this folder:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python labs.py 01
python labs.py all
```

On Windows, activate with `.venv\Scripts\activate` instead. For the tiny transformer:

```sh
python -m pip install -r requirements-optional.txt
python tiny_transformer.py
```

Read one experiment, write your prediction, run the reference, then make the requested change. Passing the supplied assertions shows the reference mechanics work; your learning comes from explaining and changing them. Keep a results notebook with configuration, observed output, explanation and one limitation. Package versions used for the delivered verification are recorded in VERIFICATION.json; the broad requirements permit compatible installations rather than promising bitwise identical results.

## 01. Gradients and stable probabilities

Read Volume 1, Chapter 1. Run `python labs.py 01`.

Predict the loss at x=2, y=5, w=1, b=0 and the result of a 0.1 update. The reference should show gradient -12 and near-zero new loss. Stable softmax must sum to one without exponentiating 1000 directly.

Change the learning rate to 1.0. Calculate the resulting prediction and loss first: w=13, b=6, prediction=32, loss=729. The larger step overshoots. Add a batch of noisy points and compare training/validation curves. Explain why the original one-point fit said nothing about generalization.

Complete `stable_softmax` in exercises.py without looking at labs.py. Run `python exercise_checks.py`. The checks intentionally fail until the three starter functions are implemented. The reference answers are named in that file's comments.

## 02. Tokenization as learned compression

Read Volume 1, Chapter 2. Run `python labs.py 02`.

List adjacent pairs in the input words and predict the first merge, including the stated deterministic tie rule. Verify that joining decoded pieces reconstructs every word. Change word frequencies and compare the merge sequence and total encoded length.

Try encoding an unseen word by applying learned merges in order. The character-level lab should preserve characters it knows without pretending to be byte BPE. Add an explicit end-of-word symbol and study whether merges change. Explain which production tokenizer concerns the toy omits: byte mapping, normalization, pre-tokenization and model-specific special tokens.

Optional real-tokenizer extension: download only a selected model's tokenizer and inspect English, code, Unicode and numerical strings. Record the exact model/tokenizer revision. Do not swap it into unrelated weights.

## 03. Causality is an invariant

Read Volume 1, Chapter 3. Run `python labs.py 03`.

Calculate the first attention row by hand. Because only the first position is allowed, its output equals the first value. Verify the masked triangle, row sums and future-perturbation check. Remove the causal mask and confirm the invariance test fails.

Add a batch/head dimension and compare your shapes with the book. Then consider a one-token query against a longer KV cache. Explain why simply making a one-by-one triangle is wrong. Build the mask using absolute query/key positions. Do not claim the square teaching function supports cached generation.

Complete `causal_mask` in exercises.py. The starter checks validate permitted positions, not model quality.

## 04. Decoding changes the distribution

Read Volume 1, Chapter 5. Run `python labs.py 04`.

Predict how temperature 0.5 differs from 1.0 before sampling. For top-p=0.8 and probabilities [0.6,0.25,0.1,0.05], the first two candidates remain and renormalize to about [0.706,0.294]. Change the threshold and observe discontinuities when another token enters the candidate set.

Sample 10,000 times and compare empirical frequencies with the filtered distribution. A single generated example is not enough to inspect a sampling algorithm. Test invalid p, zero mass and an already normalized input. Explain why a better sampling policy cannot recover missing evidence.

## 05. Structure, meaning and constrained choice

Read Volume 2, Chapters 1-2. Run `python labs.py 05`.

The record validator checks field sets, types, source membership, a missing/null relationship and real calendar dates. Add an impossible date and an invented source ID. Then add a record with a real source ID but a false value. Notice that source membership alone does not prove entailment; implement an appropriate evidence check for your task.

The enum mask demonstrates constrained selection, not a JSON grammar engine. To extend it, define a tiny grammar for a fixed enum string and track valid prefixes. For real JSON-schema decoding, use a supported runtime and test the documented schema subset, including refusal/empty-output handling. Save both validation failures and retries.

## 06. Similarity metrics and indexes

Read Volume 2, Chapter 3. Run `python labs.py 06`.

Predict why the large-norm vector wins dot product but loses cosine. Normalize the stored vectors and verify dot/cosine rankings align. Add zero vectors and mismatched dimensions and require explicit errors.

Optional database extension: select a local vector database, use the embedding dimension and distance the model expects, insert source IDs with tenant metadata, query with a filter, update a document and delete it. Verify deletion and scope before adding approximate-index tuning. Compare ANN neighbors to exact search on the same vectors; separately label relevance to the user task.

## 07. Chunking, BM25 and hybrid fusion

Read Volume 2, Chapter 4. Run `python labs.py 07`.

The integer-list chunk fixture uses length 4 and overlap 1. Predict [[0,1,2,3],[3,4,5,6],[6,7,8,9]]. Set overlap equal to length and verify rejection, preventing an infinite loop. Try a document shorter than one chunk and empty input.

The BM25 query should rank the annual-plan refund passage highest. Change it to an exact rare identifier, then to a paraphrase with no shared terms. Explain the lexical limitation. Fuse two deliberately different rank lists and calculate the top score by hand. Dense scores in a later live experiment must come from an actual embedding model, not a hand-authored ranking passed off as measured retrieval.

## 08. Graph paths with provenance

Read Volume 2, Chapter 5. Run `python labs.py 08`.

Find the three-edge path from Mira to Platform. Every edge retains its source. Restrict max_hops to two and verify no path is returned. Add a cycle and ensure traversal terminates.

Add a second Mira with a distinct entity ID, a relation with a different meaning and a time-limited ownership edge. Define resolution and temporal rules before traversal. A graph path without correct relation semantics can be a convincing error.

Optional GraphRAG extension: index a small public corpus using a pinned release, run entity-local and corpus-global questions, compare a vector baseline and record indexing cost. The provided BFS is not that full pipeline.

## 09. Tools and idempotency

Read Volume 3, Chapters 1-2. Run `python labs.py 09`.

The same operation key and unchanged payload must return one draft ID. A changed payload under that key must fail. Unknown tools must fail before execution. Add invalid types and an oversized body.

The store is in memory. Extend it to a transactional local database with a unique operation key and payload hash. Simulate a crash around execution and describe what the store can and cannot guarantee. Do not call in-memory deduplication exactly-once execution across service boundaries.

Replace the deterministic action selector with a model only after these executor checks pass. The model may propose actions; it never owns the authoritative principal.

## 10. Durable state and protocol boundaries

Read Volume 3, Chapters 2-4. Run `python labs.py 10`.

Follow accepted -> running -> awaiting_input -> running -> completed. Completion requires an artifact. A stale version and wrong owner must fail. Try a transition from completed back to running and explain why this particular state machine forbids it.

This simulation uses its own state names and is not protocol-conformant MCP/A2A code. For a real MCP extension, use the official SDK for a selected revision, expose one read-only search tool, discover it, invoke it and test an invalid argument. For A2A, expose a card and delayed task, then test polling/streaming as supported, cancellation and unauthorized task lookup. Record SDK and protocol revisions; follow their exact current method/state names.

## 11. Approval binds to an action

Read Volume 3, Chapter 5. Run `python labs.py 11`.

An unchanged action under the right user and unexpired approval passes. A modified body or expired approval fails. Add a different recipient, wrong user and stale resource version. Each material change should be evaluated under the product's authorization policy.

Build a review representation that shows the exact payload and relevant evidence. Do not let a model-controlled approval=true field authorize execution. Explain how you would store reviewer identity securely in a real application rather than in a demo dictionary.

## 12. Security at the capability boundary

Read Volume 3, Chapter 6. Run `python labs.py 12`.

Search for a deadline under the study tenant and confirm the private document is absent. An unknown tenant gets no results. Insert an instruction-bearing document and verify it cannot create an unknown tool capability.

Now test a stale cached result after access revocation. Add authorization scope and relevant versions to the cache policy, and revalidate when necessary. Report exactly which attacks you tested. A finite passing suite is evidence for those invariants, not proof of universal injection resistance.

## 13. Evals and uncertainty

Read Volume 4, Chapters 1-2. Run `python labs.py 13`.

The small classification fixture has precision and recall 0.5. The paired example has one improvement in five cases, producing wide uncertainty. Inspect changed cases rather than reporting a confident general gain.

Complete `recall_at_k` in exercises.py. Deduplicate retrieved IDs and return None when no relevant set is defined. Then implement grouped bootstrap: sample document IDs and include their associated questions. Duplicating rows must not be treated as creating new independent evidence.

## 14. Routing economics

Read Volume 4, Chapter 3. Run `python labs.py 14`.

With a small-call cost of 0.002, large-call cost 0.02 and one in four escalating, average model cost is 0.007 in the fixture. Escalated requests wait for both stages. Change the escalation rate and find where the cascade costs more than direct large-model calls.

Add a verifier cost and human-review cost for failures. Build an expected cost per successful task. These are hypothetical values; replace them with your measured workload and actual price schedule before making a deployment recommendation.

## 15. Quantization and memory

Read Volume 4, Chapter 4 and Volume 5, Chapter 3. Run `python labs.py 15`.

Inspect the scale, integer values, reconstruction and maximum error. Add a large outlier and observe how global scale changes errors for smaller values. Implement per-group scales and compare reconstruction error and metadata overhead.

Verify the 512-MiB KV estimate from the book. Change batch, sequence length and KV head count independently. The lab does not benchmark a GPU.

Real-serving extension: use a supported small model and runtime on suitable hardware, record the exact software/model/precision configuration, warm up, fix input/output lengths, then vary concurrency. Report p50/p95 end-to-end latency, first-token latency, throughput, errors and peak memory. TGI is covered for existing deployments; verify its maintenance status and evaluate an actively supported choice for a new setup.

## 16. Tracing and release consistency

Read Volume 4, Chapter 5. Run `python labs.py 16`.

Generation is the largest synthetic span. Change the index revision and require manifest validation to fail. Add a negative duration and reject invalid timing data.

Instrument the local capstone with real measured spans using a monotonic clock. Keep synthetic fixture timings separate from your observed results. Add request IDs, route/model/index versions and error categories, but avoid logging secrets or unnecessary private content.

## 17. SFT data and masks

Read Volume 5, Chapter 1. Run `python labs.py 17`.

The label array masks prompt positions with -100 and leaves answer targets. It is aligned for a trainer that performs the causal shift internally. Truncating away every predictable answer target must fail. If your training loop shifts externally, adapt the contract instead of shifting twice.

Add two paraphrases with the same group ID on opposite splits; the group check should reject them. Write a dataset card specifying task, provenance, label policy, missing/conflict examples, split unit, license/access constraints and exclusions. Do this before a paid or GPU training job.

## 18. Low-rank adaptation

Read Volume 5, Chapter 2. Run `python labs.py 18`.

The base remains unchanged while the synthetic rank-one residual is learned. Inspect both-zero initialization: both first-step factor gradients are zero. Make one factor random and the other zero, then trace which factor receives the first update.

Change the target update to rank two and compare rank-one and rank-two adapters on newly sampled held-out inputs. Record parameter count, loss and residual structure. This is real optimization of low-rank factors but not a QLoRA language-model run.

Optional QLoRA extension: pin a supported base/tokenizer, quantization method, compute dtype, adapter targets/rank and dataset. Smoke-test save/reload and masks, then compare quantized base against adapted output on held-out cases. Measure total peak training memory and re-evaluate exported artifacts.

## 19. Preferences and distillation

Read Volume 5, Chapter 4. Run `python labs.py 19`.

Positive preference advantage should reduce the DPO-form loss. The synthetic student should reduce KL to teacher probabilities. These are two separate objectives in one mechanics lab; the code does not claim to run an RLHF pipeline.

Replace some teacher targets with wrong distributions. Matching loss can improve while ground-truth accuracy worsens. Add independent labels and report both measures. For a real teacher-generated dataset, review examples, filter errors, document provenance and avoid contaminating evaluation cases.

## 20. Multimodal error propagation

Read Volume 5, Chapter 5. Run `python labs.py 20`.

Changing fifteen to fifty yields WER 0.25 in the four-word fixture, but can have much greater task impact than a harmless filler-word error. Add a negation error and label whether the answer's meaning reverses. The lab also checks overlap between time intervals.

Use a short recording or image you have permission to process. Create a manual reference, run a chosen perception model, and label names, numbers, negations, speaker/time alignment or table structure. Build three source-grounded questions and trace whether wrong answers originate in perception, retrieval or generation. This optional experiment requires a real perception tool; the edit-distance lab alone does not perform ASR or vision.

## 21. Tiny transformer: actual training

Run `python tiny_transformer.py`. Expected: decreasing loss, passing causal invariance and the repeating output ABCDABCDABCDABCD. This synthetic pattern tests the actual network and training loop, not natural-language ability.

Find each embedding, residual, normalization, mask, MLP and output head. Change the corpus to random tokens, disable training, remove the mask in a separate copy, or alter the target shift. Explain the outcome for each experiment. Keep the valid reference intact so you can compare against it.

## Local capstone: a real HTTP boundary

Run `python serve.py --port 8765`. In a second terminal:

```sh
curl -s http://127.0.0.1:8765/health
curl -s http://127.0.0.1:8765/ask \
  -H 'Content-Type: application/json' \
  -H 'X-Demo-Key: study-demo-key' \
  -d '{"query":"Atlas deadline"}'
```

The demo key maps to a tenant in server code. The server rejects a client-supplied tenant field. Omit the key to test 401, add an unknown field to test 400, and compare study/private keys without leaking d4 to study. The keys are public local-demo values, not a production authentication system.

The answer is an extracted source passage. To add generation, define a narrow model adapter that receives only authorized evidence and returns the documented response contract. Keep user identity, permission checks and action execution outside model control. Evaluate generated output against the extractive baseline, including missing and conflicting evidence.

## Completion standard

For each lab, keep one predicted result, one verified result, one modification and one failure explanation. For the capstone, keep a version manifest, dataset/rubric, baseline comparison, trace and limitations. Separate CPU-tested mechanisms from live-model experiments, simulated fixtures and unexecuted plans. That distinction is part of the skill you are learning.
