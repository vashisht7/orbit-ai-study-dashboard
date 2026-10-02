"""A real CPU-trainable tiny causal decoder on a synthetic sequence.

Run: python tiny_transformer.py
Requires PyTorch. This is a mechanics lab, not a natural-language model.
"""

import json
import torch
from torch import nn

torch.manual_seed(7)
torch.set_num_threads(1)


class Block(nn.Module):
    def __init__(self, width=32):
        super().__init__()
        self.norm1 = nn.LayerNorm(width)
        self.attn = nn.MultiheadAttention(
            width, 4, dropout=0.0, batch_first=True
        )
        self.norm2 = nn.LayerNorm(width)
        self.mlp = nn.Sequential(
            nn.Linear(width, 64), nn.GELU(), nn.Linear(64, width)
        )

    def forward(self, x):
        n = x.size(1)
        mask = torch.triu(
            torch.ones(n, n, device=x.device, dtype=torch.bool), 1
        )
        h = self.norm1(x)
        h, _ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + h
        return x + self.mlp(self.norm2(x))


class TinyDecoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.tokens = nn.Embedding(4, 32)
        self.positions = nn.Embedding(16, 32)
        self.block = Block()
        self.norm = nn.LayerNorm(32)
        self.head = nn.Linear(32, 4)

    def forward(self, ids):
        pos = torch.arange(ids.size(1), device=ids.device)
        x = self.tokens(ids) + self.positions(pos)
        return self.head(self.norm(self.block(x)))


def main():
    model = TinyDecoder()
    opt = torch.optim.AdamW(model.parameters(), lr=0.01)
    # Repeating ABCD, with varying starting phase. Every target is shifted.
    data = torch.arange(2000) % 4
    fixed_x = torch.stack([data[i : i + 12] for i in range(16)])
    fixed_y = torch.stack([data[i + 1 : i + 13] for i in range(16)])

    def loss_on(x, y):
        return nn.functional.cross_entropy(
            model(x).reshape(-1, 4), y.reshape(-1)
        )

    initial = float(loss_on(fixed_x, fixed_y).detach())
    for _ in range(160):
        model.train()
        opt.zero_grad(set_to_none=True)
        starts = torch.randint(0, 1900, (16,))
        x = torch.stack([data[i : i + 12] for i in starts])
        y = torch.stack([data[i + 1 : i + 13] for i in starts])
        loss = loss_on(x, y)
        loss.backward()
        opt.step()
    model.eval()
    with torch.inference_mode():
        final = float(loss_on(fixed_x, fixed_y))
        assert final < initial * 0.1
        base = fixed_x[:1].clone()
        changed = base.clone()
        changed[0, -1] = (changed[0, -1] + 1) % 4
        assert torch.allclose(
            model(base)[:, :-1], model(changed)[:, :-1], atol=1e-5
        )
        ids = torch.tensor([[0, 1, 2]])
        for _ in range(13):
            next_id = model(ids[:, -16:])[:, -1].argmax(-1, keepdim=True)
            ids = torch.cat([ids, next_id], dim=1)
        output = "".join("ABCD"[i] for i in ids[0].tolist())
        assert output == "ABCDABCDABCDABCD"
    print(
        json.dumps(
            {
                "initial_loss": initial,
                "final_loss": final,
                "generated": output,
                "causality_test": "passed",
                "parameters": sum(p.numel() for p in model.parameters()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
