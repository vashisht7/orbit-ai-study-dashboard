"""Generate paired write-by-hand and reference notebooks from the same exercises."""
import json
import textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'learning/model-workshop'
SAMPLE=(DEST/'sample.txt').read_text()
metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.10'},'colab':{'provenance':[]}}

def cell(kind,source,tags=None):
    data={'cell_type':kind,'metadata':{'tags':tags or []},'source':textwrap.dedent(source).strip().splitlines(keepends=True)}
    if kind=='code':data.update(execution_count=None,outputs=[])
    return data

intro='''
# Write your first Transformer, one piece at a time

Keep the dashboard's **Inside the model** lab open beside this notebook. Watch attention and the feed-forward layer, then write their calculations here.

You will build a small, CPU-friendly character-level language model. It is randomly initialized: no pretrained weights or API are involved. Short teaching stories make it runnable; expect imperfect generated text.

**How to learn:** predict a shape or output → replace one TODO → run the cell and its check → explain why it worked. A failed assertion is a clue, not a reason to paste the whole answer. `Transformer_Reference.ipynb` contains the matching completed implementation.

**Where to run:** JupyterLab on your computer, a VS Code Python notebook, or Google Colab. A GPU is unnecessary for these defaults. AI autocomplete is optional; turn it off while working through a derivation if it gives away the answer.

Local setup (in the workshop folder):
```sh
python -m pip install -r requirements-notebook.txt
python -m jupyterlab Write_Your_Transformer.ipynb
```

In Colab, upload this notebook. The included text is embedded, so no extra file is required. To use your own permitted text later, upload it to the session and change `TEXT_PATH`. Keep an independent final test set before making claims about quality.
'''
setup='''
# Run only if imports in the next cell fail (for example, in a new Colab runtime).
# In a notebook, uncomment this line and run it, then restart the kernel if asked.
# %pip install torch matplotlib
'''
imports='''
import math
import json
import hashlib
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F
import matplotlib.pyplot as plt

torch.set_num_threads(1)
SEED = 7
CONFIG = dict(width=32, heads=4, layers=2, context=32)
BATCH_SIZE = 8
STEPS = 160
print('PyTorch:', torch.__version__)
print('CPU training; configuration:', CONFIG)
'''
exercises=[]
def exercise(title,explanation,starter,solution,check):
    exercises.append((title,explanation,starter,solution,check))

exercise('1 · Turn text into IDs', '''
A character-level tokenizer assigns an integer to every character. The network receives IDs, not raw strings. Reserve the final 10% of characters **before sampling training windows**. Build the vocabulary from the training portion; ID 0 represents characters not seen there.

Write `encode_text`. It should return a 1-D `torch.long` tensor. Then print the first 20 IDs and decode them. The supplied corpus is tiny and contains related stories: a separate region is useful for this exercise but is not a robust independent benchmark. For real evaluation, split by source/document and inspect duplicates.
''',
'''def encode_text(text, lookup):
    # TODO: look up each character; use 0 for unknown characters.
    raise NotImplementedError('Write encode_text with dtype=torch.long')
''',
'''def encode_text(text, lookup):
    return torch.tensor([lookup.get(char, 0) for char in text], dtype=torch.long)
''',
'''data = encode_text(text, lookup)
train_data, val_data = data[:split], data[split:]
assert data.ndim == 1 and data.dtype == torch.long
assert encode_text('a?', {'a': 1}).tolist() == [1, 0]
assert min(len(train_data), len(val_data)) > CONFIG['context']
print('Training characters:', len(train_data), '| validation:', len(val_data))
print('First 20 IDs:', data[:20].tolist())
print('Decoded:', ''.join(vocab[i] for i in data[:20].tolist()))
''')
exercise('2 · Build x and the shifted target y', '''
For the sequence `c a t`, input `c a` has target `a t`. Every position predicts the **next** character. A batch has shape `[batch, context]`; targets have the same shape.

Write `make_batch`. Sample valid starting offsets. Return an input window and the window shifted one character to the right. Use the optional generator for repeatable evaluation without consuming training randomness.
''',
'''def make_batch(data, context, batch_size, generator=None):
    # TODO: sample starts, stack x windows, and stack y windows shifted by one.
    raise NotImplementedError('Write make_batch')
''',
'''def make_batch(data, context, batch_size, generator=None):
    starts = torch.randint(len(data) - context, (batch_size,), generator=generator)
    x = torch.stack([data[i:i+context] for i in starts])
    y = torch.stack([data[i+1:i+context+1] for i in starts])
    return x, y
''',
'''x, y = make_batch(torch.arange(100), 8, 3)
assert x.shape == y.shape == (3, 8)
assert torch.equal(y, x + 1), 'Every target should be shifted one position'
print('Input row:', x[0].tolist())
print('Target row:', y[0].tolist())
''')
exercise('3 · Write causal multi-head attention', '''
Open **Inside the model → Attention** in the dashboard.

`qkv(x)` returns `[batch, time, 3 × width]`. Split the last dimension into query, key, and value tensors. Reshape each to `[batch, heads, time, head_width]`. Compute `q @ k.transpose(-2,-1) / sqrt(head_width)`.

Set scores above the diagonal to negative infinity **before** softmax. Softmax runs over keys (the last axis). Multiply those weights by values. Rejoin the heads and apply the output projection. `.contiguous()` makes the transposed layout compatible with `.view()`.

**Prediction:** changing the last input must leave all earlier outputs unchanged. This checks causal isolation, not language quality.
''',
'''class CausalAttention(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        assert width % heads == 0
        self.heads, self.head_width = heads, width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.output = nn.Linear(width, width)

    def forward(self, x):
        batch, time, width = x.shape
        # TODO: project, split heads, score, mask, softmax, mix values, rejoin.
        raise NotImplementedError('Write the attention forward pass')
''',
'''class CausalAttention(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        assert width % heads == 0
        self.heads, self.head_width = heads, width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.output = nn.Linear(width, width)

    def forward(self, x):
        batch, time, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        def split_heads(t):
            return t.view(batch, time, self.heads, self.head_width).transpose(1, 2)
        q, k, v = map(split_heads, (q, k, v))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_width)
        future = torch.ones(time, time, device=x.device, dtype=torch.bool).triu(1)
        weights = scores.masked_fill(future, float('-inf')).softmax(dim=-1)
        mixed = (weights @ v).transpose(1, 2).contiguous()
        return self.output(mixed.view(batch, time, width))
''',
'''attention = CausalAttention(8, 2).eval()
x = torch.randn(2, 5, 8)
altered = x.clone(); altered[:, -1] += 10
assert attention(x).shape == x.shape
torch.testing.assert_close(attention(x)[:, :-1], attention(altered)[:, :-1])
print('Attention shape and causal isolation passed.')
''')
exercise('4 · Write the feed-forward layer', '''
Open **Inside the model → Feed-forward**. The dashboard uses 4 → 8 → 4 for readability; here use width → 4×width → width.

Write an expansion `nn.Linear`, GELU, and contraction `nn.Linear`. Each token uses the **same learned matrices independently**. Attention mixes token positions; this layer transforms features at one position. A nonlinear activation is essential: two affine layers alone are equivalent to one affine layer.

`nn.Linear(in_features,out_features)` computes `x @ weight.T + bias` for row-oriented batches. It operates on the last axis. Do not flatten time into the feature dimension.
''',
'''class FeedForward(nn.Module):
    def __init__(self, width):
        super().__init__()
        # TODO: define self.up and self.down with the correct dimensions.
        raise NotImplementedError('Write the two Linear layers')

    def forward(self, x):
        # TODO: expansion -> GELU -> contraction.
        raise NotImplementedError('Write the FFN calculation')
''',
'''class FeedForward(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.up = nn.Linear(width, 4 * width)
        self.down = nn.Linear(4 * width, width)

    def forward(self, x):
        return self.down(F.gelu(self.up(x)))
''',
'''ffn = FeedForward(8).eval()
x = torch.randn(2, 5, 8)
altered = x.clone(); altered[:, 2] += 3
assert ffn(x).shape == x.shape
torch.testing.assert_close(ffn(x)[:, :2], ffn(altered)[:, :2])
torch.testing.assert_close(ffn(x)[:, 3:], ffn(altered)[:, 3:])
assert not torch.allclose(ffn(x)[:, 2], ffn(altered)[:, 2])
print('FFN changes one token independently; shared weights preserve shape.')
''')
exercise('5 · Connect the Transformer', '''
A pre-norm block does two residual updates:

`x = x + attention(norm1(x))`

`x = x + ffn(norm2(x))`

The bypass carries the original residual vector; **do not add the normalized vector instead**. Add token and position embeddings before the blocks, then final normalization and vocabulary projection after them. Output shape is `[batch,time,vocabulary]`, so every position produces next-character scores.

Complete the two forward methods. Keep shapes visible by printing them while you debug.
''',
'''class Block(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.attention, self.ffn = CausalAttention(width, heads), FeedForward(width)

    def forward(self, x):
        # TODO: two pre-norm residual updates.
        raise NotImplementedError('Connect attention and FFN with residuals')

class TinyTransformer(nn.Module):
    def __init__(self, vocabulary, width, heads, layers, context):
        super().__init__()
        self.context = context
        self.tokens = nn.Embedding(vocabulary, width)
        self.positions = nn.Embedding(context, width)
        self.blocks = nn.Sequential(*[Block(width, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.to_logits = nn.Linear(width, vocabulary)

    def forward(self, ids):
        # TODO: add token+position embeddings, run blocks, normalize, project.
        raise NotImplementedError('Write the decoder forward pass')
''',
'''class Block(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.attention, self.ffn = CausalAttention(width, heads), FeedForward(width)

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        return x + self.ffn(self.norm2(x))

class TinyTransformer(nn.Module):
    def __init__(self, vocabulary, width, heads, layers, context):
        super().__init__()
        self.context = context
        self.tokens = nn.Embedding(vocabulary, width)
        self.positions = nn.Embedding(context, width)
        self.blocks = nn.Sequential(*[Block(width, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.to_logits = nn.Linear(width, vocabulary)

    def forward(self, ids):
        position_ids = torch.arange(ids.shape[1], device=ids.device)
        x = self.tokens(ids) + self.positions(position_ids)
        return self.to_logits(self.norm(self.blocks(x)))
''',
'''torch.manual_seed(SEED)
model = TinyTransformer(len(vocab), **CONFIG).eval()
x, y = make_batch(train_data, CONFIG['context'], BATCH_SIZE)
logits = model(x)
assert logits.shape == (BATCH_SIZE, CONFIG['context'], len(vocab))
altered = x.clone(); altered[:, -1] = (altered[:, -1] + 1) % len(vocab)
torch.testing.assert_close(model(x)[:, :-1], model(altered)[:, :-1])
print('Logits:', list(logits.shape))
print('Trainable parameters:', sum(p.numel() for p in model.parameters()))
''')
exercise('6 · Write one training update', '''
The next-token objective is cross-entropy between logits and the shifted target. Flatten batch and time so cross-entropy sees a list of predictions.

Order matters: clear stale gradients → forward pass → loss → backward → clip → optimizer step. `backward()` computes derivatives; `step()` changes parameters. Return a plain number for logging, using `loss.item()`.

The check below verifies that weights really change, so printing a loss without an optimizer update will not pass.
''',
'''def update(model, optimizer, x, y):
    # TODO: zero_grad, forward, cross_entropy, backward, clip, optimizer.step.
    raise NotImplementedError('Write one training update and return the loss')
''',
'''def update(model, optimizer, x, y):
    optimizer.zero_grad(set_to_none=True)
    logits = model(x)
    loss = F.cross_entropy(logits.flatten(0, 1), y.flatten())
    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    return loss.item()
''',
'''model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.003)
before = model.to_logits.weight.detach().clone()
loss = update(model, optimizer, x, y)
assert math.isfinite(loss)
assert not torch.equal(before, model.to_logits.weight)
print('One update changed weights. Loss:', round(loss, 4))
''')
experiment='''
@torch.no_grad()
def evaluate(model):
    model.eval()
    generator = torch.Generator().manual_seed(1234)
    losses = []
    for _ in range(6):
        x, y = make_batch(val_data, CONFIG['context'], BATCH_SIZE, generator)
        losses.append(F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item())
    model.train()
    return sum(losses) / len(losses)

def experiment(learning_rate, steps=STEPS):
    # Fresh model, identical initialization and training batch sequence for each run.
    torch.manual_seed(SEED)
    model = TinyTransformer(len(vocab), **CONFIG)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    history = [dict(step=0, train_loss=None, validation_loss=evaluate(model))]
    for step in range(1, steps + 1):
        x, y = make_batch(train_data, CONFIG['context'], BATCH_SIZE)
        loss = update(model, optimizer, x, y)
        if step % 20 == 0 or step == steps:
            row = dict(step=step, train_loss=loss, validation_loss=evaluate(model))
            history.append(row)
            print(f'lr={learning_rate}: step {step}, train={loss:.3f}, val={row["validation_loss"]:.3f}')
    return model, history

model_a, history_a = experiment(0.001)
model_b, history_b = experiment(0.003)
for label, history in [('lr 0.001', history_a), ('lr 0.003', history_b)]:
    plt.plot([r['step'] for r in history], [r['validation_loss'] for r in history], marker='o', label=label)
plt.xlabel('Training step'); plt.ylabel('Held-out cross-entropy')
plt.title('Same initialization and data, different learning rates')
plt.legend(); plt.grid(alpha=0.2); plt.show()
print('Inspect the actual curves. Do not assume a higher learning rate always wins.')
'''
exercise('8 · Generate text one character at a time', '''
Use the final position's logits, not every position. Divide by a positive temperature, apply softmax, sample one ID, append it, and repeat. Crop the context to the model's maximum length.

Temperature changes the sampling distribution; it does not retrain the model. Compare two temperatures with the same model and random seed. Expect broken words from this tiny run. Fluent fragments are not proof of broad language ability.
''',
'''@torch.no_grad()
def generate(model, temperature=0.8, length=200):
    model.eval()
    torch.manual_seed(42)
    ids = train_data[:1].reshape(1, 1)
    # TODO: for each new character, predict, sample and append.
    raise NotImplementedError('Write the autoregressive generation loop')
''',
'''@torch.no_grad()
def generate(model, temperature=0.8, length=200):
    if temperature <= 0:
        raise ValueError('Use a positive temperature')
    model.eval()
    torch.manual_seed(42)
    ids = train_data[:1].reshape(1, 1)
    for _ in range(length):
        logits = model(ids[:, -model.context:])[:, -1] / temperature
        next_id = torch.multinomial(logits.softmax(-1), num_samples=1)
        ids = torch.cat([ids, next_id], dim=1)
    return ''.join(vocab[i] for i in ids[0].tolist())
''',
'''print('Temperature 0.5:\n', generate(model_b, temperature=0.5))
print('\nTemperature 1.0:\n', generate(model_b, temperature=1.0))
assert generate(model_b, length=0) == vocab[train_data[0].item()]
'''.replace("'Temperature 0.5:\n'", "'Temperature 0.5:\\n'").replace("'\nTemperature 1.0:\n'", "'\\nTemperature 1.0:\\n'"))
export='''
out = Path('notebook-run'); out.mkdir(exist_ok=True)
report = dict(config=CONFIG, history=history_b,
              text_sha256=hashlib.sha256(text.encode()).hexdigest(),
              note='Notebook run B; contiguous held-out teaching text, not a broad benchmark.')
(out / 'metrics.json').write_text(json.dumps(report, indent=2))
(out / 'sample.txt').write_text(generate(model_b), encoding='utf-8')
torch.save(dict(state_dict=model_b.state_dict(), config=CONFIG, vocabulary=vocab),
           out / 'notebook_weights.pt')
# This is an inference weights file, not the resumable checkpoint format of train.py.
saved = torch.load(out / 'notebook_weights.pt', weights_only=True, map_location='cpu')
restored = TinyTransformer(len(saved['vocabulary']), **saved['config'])
restored.load_state_dict(saved['state_dict']); restored.eval(); model_b.eval()
probe, _ = make_batch(train_data, CONFIG['context'], 1)
torch.testing.assert_close(restored(probe), model_b(probe))
print('Saved and reloaded matching weights.')
print('Import notebook-run/metrics.json into the dashboard: Train a small model → Inspect results.')
print('To resume full training with optimizer state, use the separate train.py workshop.')
'''

for reference in [False,True]:
    cells=[cell('markdown',intro.replace('# Write your first Transformer, one piece at a time','# Transformer reference — compare after you try') if reference else intro),cell('code',setup,['optional-install']),cell('code',imports)]
    for idx,(title,explanation,starter,solution,check) in enumerate(exercises):
        cells.append(cell('markdown','## '+title+'\n\n'+explanation))
        if idx==0:
            cells.append(cell('code',"TEXT_PATH = None  # Or a local UTF-8 file such as 'my-stories.txt'\nBUILT_IN_TEXT = "+repr(SAMPLE)+"\ntext = Path(TEXT_PATH).read_text(encoding='utf-8') if TEXT_PATH else BUILT_IN_TEXT\nsplit = int(len(text) * 0.9)\nvocab = ['<UNK>'] + sorted(set(text[:split]))\nlookup = {char: i for i, char in enumerate(vocab)}\nprint('Vocabulary size:', len(vocab))"))
        if title.startswith('8'):
            generation_heading = cells.pop()
            cells.append(cell('markdown','''## 7 · Compare two real training runs

Before running, predict which learning rate will reduce validation loss faster. The helper resets the random seed before model initialization, so both runs start with identical weights and see the same sampled training windows. Validation uses its own generator. Inspect the measured curves and explain the outcome. A validation region is not a final test set; repeated tuning can overfit it too.

Change only the learning rates first. Later, change width, context length, or text in the setup cells and rerun all dependent cells from the top. Parameter count and task difficulty may then change, so make comparisons carefully.'''))
            cells.append(cell('code',experiment))
            cells.append(generation_heading)
        cells.append(cell('code',solution if reference else starter,['exercise']))
        cells.append(cell('code',check,['check']))
    cells += [cell('markdown','## 9 · Keep your results\n\nSave and reload your model weights, export real losses, and inspect them alongside the dashboard visualizations. This saved notebook artifact is for inference; the separate `train.py` saves optimizer and random state for resumable training.'),cell('code',export),cell('markdown','''## Explain what you built

1. Why does attention mix tokens while the feed-forward layer does not?
2. What do the two residual connections preserve?
3. Why is the target shifted by one character?
4. Which function computes gradients, and which changes weights?
5. Why can lower training loss coexist with worse held-out loss?
6. What happened when you changed learning rate? Use your actual numbers.
7. How is this small character model different from an instruction-tuned assistant?

Keep one failure, your diagnosis, your change, and the measured effect. That is useful interview evidence.''')]
    filename='Transformer_Reference.ipynb' if reference else 'Write_Your_Transformer.ipynb'
    (DEST/filename).write_text(json.dumps({'nbformat':4,'nbformat_minor':5,'metadata':metadata,'cells':[dict(c,id=f'cell-{i:03d}') for i,c in enumerate(cells)]},indent=1))
print('Built two notebooks:',len(cells),'cells each; seven implementation exercises, comparison plots, and export.')
