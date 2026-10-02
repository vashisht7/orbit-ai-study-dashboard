"""A teaching decoder, not Qwen and not a production assistant.
Needs Python 3 and PyTorch. Uses only a small synthetic local corpus.
Example: python3 tiny_decoder.py --steps 40 --width 32 --heads 4
"""
import argparse
import math
import torch
from torch import nn
from torch.nn import functional as F

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
        # Split feature coordinates across heads, retaining token order.
        def split(tensor):
            return tensor.view(batch, time, self.heads,
                               self.head_width).transpose(1, 2)
        q, k, v = map(split, (q, k, v))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_width)
        future = torch.ones(time, time, device=x.device,
                            dtype=torch.bool).triu(1)
        weights = scores.masked_fill(future, float('-inf')).softmax(-1)
        mixed = (weights @ v).transpose(1, 2).contiguous()
        return self.output(mixed.view(batch, time, width))

class Block(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.attention = Attention(width, heads)
        self.feed_forward = nn.Sequential(nn.Linear(width, 4 * width),
                                         nn.GELU(),
                                         nn.Linear(4 * width, width))

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        return x + self.feed_forward(self.norm2(x))

class Decoder(nn.Module):
    def __init__(self, vocabulary, width, heads, layers, context):
        super().__init__()
        self.context = context
        self.tokens = nn.Embedding(vocabulary, width)
        self.positions = nn.Embedding(context, width)
        self.blocks = nn.Sequential(*[Block(width, heads)
                                      for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.to_logits = nn.Linear(width, vocabulary)

    def forward(self, ids):
        length = ids.shape[1]
        positions = torch.arange(length, device=ids.device)
        x = self.tokens(ids) + self.positions(positions)
        return self.to_logits(self.norm(self.blocks(x)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=32)
    parser.add_argument('--heads', type=int, default=4)
    parser.add_argument('--layers', type=int, default=1)
    parser.add_argument('--context', type=int, default=32)
    parser.add_argument('--steps', type=int, default=40)
    parser.add_argument('--lr', type=float, default=0.003)
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    if (min(args.width, args.heads, args.layers, args.context, args.steps) < 1
            or args.width % args.heads or args.lr <= 0):
        parser.error('Use positive values; width must divide evenly by heads.')
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    text = ('remind me to call maya. save a note. ask for a time. ' * 40)
    vocabulary = sorted(set(text))
    encode = {char: i for i, char in enumerate(vocabulary)}
    data = torch.tensor([encode[char] for char in text])
    if args.context >= len(data) - 1:
        parser.error('Context is too long for the toy corpus.')
    model = Decoder(len(vocabulary), args.width, args.heads,
                    args.layers, args.context)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    print('Trainable parameters:', sum(p.numel() for p in model.parameters()))
    # Repeated synthetic data is for mechanics, not independent evaluation.
    for step in range(args.steps):
        starts = torch.randint(len(data) - args.context - 1, (8,))
        x = torch.stack([data[i:i+args.context] for i in starts])
        y = torch.stack([data[i+1:i+args.context+1] for i in starts])
        logits = model(x)
        loss = F.cross_entropy(logits.reshape(-1, len(vocabulary)),
                               y.reshape(-1))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        if step == 0 or (step + 1) % 10 == 0:
            print('Step', step + 1, 'training loss', round(loss.item(), 4))
    model.eval()
    with torch.no_grad():
        # Change the final input; earlier causal outputs must stay identical.
        probe = data[:args.context].unsqueeze(0).clone()
        altered = probe.clone()
        altered[0, -1] = (altered[0, -1] + 1) % len(vocabulary)
        torch.testing.assert_close(model(probe)[:, :-1],
                                   model(altered)[:, :-1])
        assert torch.isfinite(loss)
        ids = torch.tensor([[encode['r']]])
        for _ in range(60):
            logits = model(ids[:, -args.context:])[:, -1]
            next_id = logits.argmax(-1, keepdim=True)
            ids = torch.cat([ids, next_id], dim=1)
        print('Toy greedy sample:', ''.join(vocabulary[i] for i in ids[0]))
    print('Causal check passed. Training loss is not a quality benchmark.')

if __name__ == '__main__':
    main()
