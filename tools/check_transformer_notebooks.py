"""Validate notebook format and execute reference cells in a clean temporary folder."""
import contextlib
import json
import os
import tempfile
from pathlib import Path
import nbformat
import matplotlib
matplotlib.use('Agg')
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'learning/model-workshop'
for name in ['Write_Your_Transformer.ipynb','Transformer_Reference.ipynb']:
    nbformat.validate(nbformat.read(folder/name,as_version=4))
reference=json.loads((folder/'Transformer_Reference.ipynb').read_text())
starter=json.loads((folder/'Write_Your_Transformer.ipynb').read_text())
assert sum('exercise' in c['metadata'].get('tags',[]) for c in starter['cells'])==7
assert all('NotImplementedError' in ''.join(c['source']) for c in starter['cells'] if 'exercise' in c['metadata'].get('tags',[]))
original=Path.cwd()
with tempfile.TemporaryDirectory() as temp:
    os.chdir(temp)
    scope={'__name__':'__main__'}
    try:
        for index,cell in enumerate(reference['cells']):
            if cell['cell_type']=='code':
                exec(compile(''.join(cell['source']),f'notebook cell {index}','exec'),scope)
        a,b=scope['history_a'],scope['history_b']
        assert a[0]['validation_loss']==b[0]['validation_loss']
        assert b[-1]['validation_loss']<b[0]['validation_loss']
        assert Path('notebook-run/metrics.json').is_file()
        result=ROOT/'output/learning-review'
        result.mkdir(parents=True,exist_ok=True)
        scope['plt'].savefig(result/'notebook-loss-comparison.png',dpi=160,bbox_inches='tight')
        (result/'notebook-verification.json').write_text(json.dumps({'notebook_cells':len(reference['cells']),'implementation_exercises':7,'steps_per_run':scope['STEPS'],'run_a':a,'run_b':b,'checks':['notebook schema','starter TODOs present','all reference cells executed','causal attention','positionwise FFN','real parameter update','controlled initialization','save and reload identical predictions']},indent=2))
    finally:
        os.chdir(original)
print('PASS: notebook schema, seven unfinished exercises, all reference cells, controlled training, plot, generation, save/reload, metrics export.')
