"""Tiny decoder with explicit attention. Requires PyTorch; CPU is sufficient.
This synthetic task validates mechanics, not natural-language capability.
"""
import math
import torch
from torch import nn
from torch.nn import functional as F


class Attention(nn.Module):
    def __init__(self, width, heads, context):
        super().__init__()
        if width % heads:
            raise ValueError("Width must be divisible by head count.")
        self.heads = heads
        self.head_width = width // heads
        self.qkv = nn.Linear(width, 3 * width, bias=False)
        self.output = nn.Linear(width, width, bias=False)
        self.register_buffer("mask", torch.tril(
            torch.ones(context, context, dtype=torch.bool)))

    def forward(self, x):
        batch, time, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)

        def split(tensor):
            return tensor.reshape(batch, time, self.heads,
                                  self.head_width).transpose(1, 2)

        q, k, v = map(split, (q, k, v))
        scores = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_width)
        scores = scores.masked_fill(~self.mask[:time, :time], float("-inf"))
        weights = F.softmax(scores, dim=-1)
        mixed = weights @ v
        mixed = mixed.transpose(1, 2).contiguous().reshape(batch, time, width)
        return self.output(mixed)


class Block(nn.Module):
    def __init__(self, width, heads, context):
        super().__init__()
        self.norm1 = nn.LayerNorm(width)
        self.attention = Attention(width, heads, context)
        self.norm2 = nn.LayerNorm(width)
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(),
                                 nn.Linear(4 * width, width))

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        return x + self.mlp(self.norm2(x))


class Decoder(nn.Module):
    def __init__(self, vocabulary=4, context=12, width=24, heads=3, layers=2):
        super().__init__()
        self.context = context
        self.token = nn.Embedding(vocabulary, width)
        self.position = nn.Embedding(context, width)
        self.blocks = nn.Sequential(*[
            Block(width, heads, context) for _ in range(layers)])
        self.final_norm = nn.LayerNorm(width)
        self.head = nn.Linear(width, vocabulary)

    def forward(self, tokens, targets=None):
        if tokens.ndim != 2 or not 1 <= tokens.shape[1] <= self.context:
            raise ValueError("Tokens must have shape batch,time within context.")
        positions = torch.arange(tokens.shape[1], device=tokens.device)
        x = self.token(tokens) + self.position(positions)
        logits = self.head(self.final_norm(self.blocks(x)))
        loss = None if targets is None else F.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, tokens, count, temperature=1.0):
        if temperature <= 0:
            raise ValueError("Temperature must be positive.")
        was_training = self.training
        self.eval()
        try:
            for _ in range(count):
                logits, _ = self(tokens[:, -self.context:])
                p = F.softmax(logits[:, -1] / temperature, dim=-1)
                tokens = torch.cat((tokens, torch.multinomial(p, 1)), dim=1)
            return tokens
        finally:
            self.train(was_training)


def checks_and_train(steps=180):
    torch.manual_seed(23)
    torch.set_num_threads(1)
    model = Decoder()
    # Earlier logits cannot depend on future token identities.
    first = torch.tensor([[0, 1, 2, 3, 0, 1]])
    changed = first.clone()
    changed[0, 4:] = torch.tensor([2, 3])
    with torch.no_grad():
        a, _ = model(first)
        b, _ = model(changed)
    assert torch.allclose(a[:, :4], b[:, :4], atol=1e-6)
    # Synthetic sequence: every next token is current token plus one modulo 4.
    starts = torch.arange(4).unsqueeze(1)
    sequence = (starts + torch.arange(13).unsqueeze(0)) % 4
    x, y = sequence[:, :-1], sequence[:, 1:]
    optimizer = torch.optim.AdamW(model.parameters(), lr=.008)
    initial = model(x, y)[1].item()
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        _, loss = model(x, y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    final = model(x, y)[1].item()
    assert final < .02 and final < initial / 20
    sample = model.generate(torch.tensor([[0]]), 16, .5)[0].tolist()
    assert sample == [i % 4 for i in range(17)]
    return {"parameters": sum(p.numel() for p in model.parameters()),
            "initial_loss": initial, "final_loss": final,
            "causal_invariance": True, "sample": sample,
            "torch_version": torch.__version__}


if __name__ == "__main__":
    print(checks_and_train())
