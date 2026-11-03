"""Train a small character-level Transformer on your own UTF-8 text.
CPU-friendly defaults. This is an educational model, not a useful assistant.
Only resume checkpoints you created yourself (torch.load uses pickle here).
"""
# SECTION: Imports and configuration
import argparse
import hashlib
import json
import math
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F

# SECTION: Attention — mix information from earlier characters
class Attention(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.heads = heads
        self.head_width = width // heads
        self.qkv = nn.Linear(width, 3 * width)
        self.output = nn.Linear(width, width)

    def forward(self, x):
        batch, time, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        def split(t):
            return t.view(batch, time, self.heads, self.head_width).transpose(1, 2)
        q, k, v = map(split, (q, k, v))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_width)
        future = torch.ones(time, time, device=x.device, dtype=torch.bool).triu(1)
        weights = scores.masked_fill(future, float('-inf')).softmax(-1)
        mixed = (weights @ v).transpose(1, 2).contiguous()
        return self.output(mixed.view(batch, time, width))

# SECTION: A Transformer block — communicate, then transform
class Block(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.attention = Attention(width, heads)
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(),
                                 nn.Linear(4 * width, width))

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        return x + self.mlp(self.norm2(x))

# SECTION: The model — IDs in, next-character scores out
class Decoder(nn.Module):
    def __init__(self, vocabulary, width, heads, layers, context):
        super().__init__()
        self.context = context
        self.tokens = nn.Embedding(vocabulary, width)
        self.positions = nn.Embedding(context, width)
        self.blocks = nn.Sequential(*[Block(width, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.output = nn.Linear(width, vocabulary)

    def forward(self, ids):
        positions = torch.arange(ids.shape[1], device=ids.device)
        x = self.tokens(ids) + self.positions(positions)
        return self.output(self.norm(self.blocks(x)))

# SECTION: Batches and evaluation — predict the next character

def batch_from(data, context, batch_size, generator=None):
    starts = torch.randint(len(data) - context, (batch_size,), generator=generator)
    x = torch.stack([data[i:i + context] for i in starts])
    y = torch.stack([data[i + 1:i + context + 1] for i in starts])
    return x, y

@torch.no_grad()
def evaluate(model, data, batch_size):
    model.eval()
    # A separate fixed generator compares the same validation windows each time.
    generator = torch.Generator().manual_seed(1234)
    losses = []
    for _ in range(8):
        x, y = batch_from(data, model.context, batch_size, generator)
        logits = model(x)
        losses.append(F.cross_entropy(logits.flatten(0, 1), y.flatten()).item())
    model.train()
    return sum(losses) / len(losses)

# SECTION: Load text and create separate training and validation regions

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', default=str(Path(__file__).with_name('sample.txt')))
    parser.add_argument('--steps', type=int, default=200, help='Additional steps per invocation')
    parser.add_argument('--width', type=int, default=64)
    parser.add_argument('--heads', type=int, default=4)
    parser.add_argument('--layers', type=int, default=2)
    parser.add_argument('--context', type=int, default=64)
    parser.add_argument('--batch-size', type=int, default=8)
    parser.add_argument('--lr', type=float, default=0.003)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--temperature', type=float, default=0.8)
    parser.add_argument('--generate', type=int, default=200)
    parser.add_argument('--out', default='run')
    parser.add_argument('--resume', help='Your own checkpoint.pt; never load untrusted files')
    args = parser.parse_args()
    if (min(args.width, args.heads, args.layers, args.context, args.batch_size, args.steps) < 1
            or args.width % args.heads or not math.isfinite(args.lr) or args.lr <= 0
            or not math.isfinite(args.temperature) or args.temperature <= 0 or args.generate < 0):
        parser.error('Use positive finite settings; width must be divisible by heads.')
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    text = Path(args.text).read_text(encoding='utf-8')
    fingerprint = hashlib.sha256(text.encode()).hexdigest()
    cut = int(len(text) * 0.9)
    # Vocabulary is learned from the training region. 0 represents unknown characters.
    vocabulary = ['<UNK>'] + sorted(set(text[:cut]))
    encode = {char: i for i, char in enumerate(vocabulary)}
    data = torch.tensor([encode.get(char, 0) for char in text], dtype=torch.long)
    train, validation = data[:cut], data[cut:]
    if min(len(train), len(validation)) <= args.context:
        parser.error('Text is too short: both 90% training and 10% validation need > context characters.')
    config = dict(vocabulary=len(vocabulary), width=args.width, heads=args.heads,
                  layers=args.layers, context=args.context)
    model = Decoder(**config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    start, history = 0, []
    if args.resume:
        saved = torch.load(args.resume, map_location='cpu', weights_only=False)
        if saved['config'] != config or saved['text_sha256'] != fingerprint:
            parser.error('Resume requires the same text, width, heads, layers, and context.')
        if saved['batch_size'] != args.batch_size or saved['lr'] != args.lr:
            parser.error('Resume requires the same batch size and learning rate.')
        model.load_state_dict(saved['model'])
        optimizer.load_state_dict(saved['optimizer'])
        torch.set_rng_state(saved['rng'])
        start, history = saved['step'], saved['history']
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    print('Parameters:', sum(p.numel() for p in model.parameters()))
    print('Training characters:', len(train), '| validation characters:', len(validation))
    print('Validation unknown-character fraction:', round((validation == 0).float().mean().item(), 4))
    initial = evaluate(model, validation, args.batch_size)
    print(f'Before this run: validation loss {initial:.4f}')
    if not history:
        history.append(dict(step=0, train_loss=None, validation_loss=initial))

    # SECTION: Learn — forward pass, loss, gradients, weight update
    model.train()
    for step in range(start, start + args.steps):
        x, y = batch_from(train, args.context, args.batch_size)
        logits = model(x)
        loss = F.cross_entropy(logits.flatten(0, 1), y.flatten())
        if not torch.isfinite(loss):
            raise RuntimeError('Non-finite loss. Try a smaller learning rate.')
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        if (step + 1) % 20 == 0 or step + 1 == start + args.steps:
            val = evaluate(model, validation, args.batch_size)
            row = dict(step=step + 1, train_loss=loss.item(), validation_loss=val)
            history.append(row)
            print(f"Step {step + 1}: train {loss.item():.4f} | validation {val:.4f}")

    # SECTION: Save a resumable checkpoint and measurements
    saved = dict(config=config, vocabulary=vocabulary, text_sha256=fingerprint,
                 model=model.state_dict(), optimizer=optimizer.state_dict(),
                 rng=torch.get_rng_state(), step=start + args.steps, history=history,
                 batch_size=args.batch_size, lr=args.lr)
    torch.save(saved, out / 'checkpoint.pt')
    report = dict(config=config, text_sha256=fingerprint, history=history,
                  note='Contiguous held-out text, not an independent benchmark. Inspect duplicates and source leakage.')
    (out / 'metrics.json').write_text(json.dumps(report, indent=2))

    # SECTION: Generate — append one sampled character at a time
    model.eval()
    with torch.no_grad():
        probe = train[:args.context].unsqueeze(0)
        altered = probe.clone()
        altered[0, -1] = (altered[0, -1] + 1) % len(vocabulary)
        torch.testing.assert_close(model(probe)[:, :-1], model(altered)[:, :-1])
        ids = train[:1].reshape(1, 1)
        for _ in range(args.generate):
            logits = model(ids[:, -args.context:])[:, -1] / args.temperature
            next_id = torch.multinomial(logits.softmax(-1), num_samples=1)
            ids = torch.cat([ids, next_id], dim=1)
    sample = ''.join(vocabulary[i] for i in ids[0].tolist())
    (out / 'sample.txt').write_text(sample, encoding='utf-8')
    print('\nGenerated text (expect imperfect output):\n' + sample)
    print('\nSaved checkpoint.pt, metrics.json, sample.txt in', out)
    print('Causal-mask check passed. Lower training loss alone does not prove generalization.')

if __name__ == '__main__':
    main()
