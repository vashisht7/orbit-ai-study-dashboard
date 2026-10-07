/* Shared lesson selections and plain-language recall answers. */
window.DAILY_LESSON_CONTENT = (() => {
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
  return {topicIds, answers};
})();
