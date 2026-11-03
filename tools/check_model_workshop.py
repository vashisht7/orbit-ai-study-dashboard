"""Check causality, actual learning, and exact checkpoint continuation on CPU."""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import torch
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'learning/model-workshop/train.py'
spec = importlib.util.spec_from_file_location('workshop', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
torch.set_num_threads(1)
model = m.Decoder(vocabulary=12, width=16, heads=4, layers=1, context=8).eval()
x = torch.randint(12, (2, 8))
y = x.clone(); y[:, -1] = (y[:, -1] + 1) % 12
with torch.no_grad():
    torch.testing.assert_close(model(x)[:, :-1], model(y)[:, :-1])
assert model(x).shape == (2, 8, 12)
with tempfile.TemporaryDirectory() as tmp:
    base = [sys.executable, str(SCRIPT), '--width', '16', '--heads', '4', '--layers', '1', '--context', '16', '--generate', '5']
    def run(extra):
        r = subprocess.run(base + extra, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr + r.stdout
    a, b = Path(tmp)/'whole', Path(tmp)/'split'
    run(['--steps', '40', '--out', str(a)])
    run(['--steps', '20', '--out', str(b)])
    run(['--steps', '20', '--resume', str(b/'checkpoint.pt'), '--out', str(b)])
    full = torch.load(a/'checkpoint.pt', weights_only=False)
    resumed = torch.load(b/'checkpoint.pt', weights_only=False)
    assert full['step'] == resumed['step'] == 40
    for key in full['model']:
        torch.testing.assert_close(full['model'][key], resumed['model'][key], rtol=0, atol=0)
    rows = json.loads((a/'metrics.json').read_text())['history']
    assert rows[-1]['validation_loss'] < rows[0]['validation_loss']
    wrong = subprocess.run(base + ['--steps','1','--lr','0.1','--resume',str(b/'checkpoint.pt')], capture_output=True, text=True)
    assert wrong.returncode != 0 and 'same batch size and learning rate' in wrong.stderr
print('PASS: output shapes, causal masking, real learning, exact resumed weights, resume mismatch rejection.')
