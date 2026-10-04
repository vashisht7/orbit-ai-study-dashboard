"""Check source/annotation alignment and recorded outputs independently of rendering."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
dec=json.JSONDecoder()
problems=dec.raw_decode((root/'problems-data.js').read_text().split('const PROBLEMS=')[1])[0]
walks=dec.raw_decode((root/'walkthroughs-data.js').read_text().split('window.WALKTHROUGHS=')[1])[0]
ns={}
harness=re.search(r'const HARNESS = `(.*?)`;', (root/'practice.js').read_text(),re.S).group(1)
exec(harness,ns)
assert set(walks)=={p['id'] for p in problems}
for p in problems:
 w=walks[p['id']]
 code=p['solution'].splitlines()
 assert len(w['lines'])==len([s for s in code if s.strip()]),p['id']
 for line in w['lines']:
  assert line['code']==code[line['number']-1] and len(line['note'])>10,p['id']
 for e in w['examples']:
  assert e['frames'] and ns['_eq'](e['actual'],e['expected'],p['cmp']),(p['id'],e['actual'],e['expected'])
  for frame in e['frames']:
   assert 1<=frame['line']<=len(code),p['id']
   assert frame['event'] in ('line','return') and isinstance(frame['state'],dict)
print(f'{len(walks)} walkthroughs: every code line explained, all 168 recorded example outputs match expected answers.')
