"""Run every reference against the browser harness and audit study metadata.
New exercises have hand-specified expectations; the original 40 retain generated tests.
"""
import asyncio
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
raw = (ROOT / 'problems-data.js').read_text()
decoder = json.JSONDecoder()
prelude = decoder.raw_decode(raw.split('const PRELUDE_PY=', 1)[1])[0]
problems = decoder.raw_decode(raw.split('const PROBLEMS=', 1)[1])[0]
harness = re.search(r'const HARNESS = `(.*?)`;', (ROOT / 'practice.js').read_text(), re.S).group(1)
assert len({p['id'] for p in problems}) == len(problems)

async def check():
    total = 0
    for p in problems:
        assert p['tests'] and p['days'] and p['track'] and p['relevance'], p['id']
        assert all(heading in p['explanation'] for heading in ['How to think','Walk through','Time and space','Common mistake','Interview follow-up']), p['id']
        assert (p['evidence'] == 'Reported / adapted') == bool(p['sources']), p['id']
        for source in p['sources']:
            assert source['url'].startswith('https://') and source['company'] and source['checked']
        ns = {}
        exec(prelude + harness, ns)
        exec(p['solution'], ns)
        compile(p['starter'], p['id'], 'exec')
        for test in p['tests']:
            result = json.loads(await ns['_run_one'](json.dumps(test), p['fn'], p['kind'], p['cmp'], p['tree']))
            assert result['ok'], (p['id'], test, result)
            total += 1
    print(f'{len(problems)} reference solutions passed {total} cases using the browser Python harness.')
    print(f'{sum(bool(p["sources"]) for p in problems)} sourced problems; companies: ' + ', '.join(sorted({s['company'] for p in problems for s in p['sources']})))
    print('Metadata, unique IDs, starter syntax, explanations, and source labels verified.')

asyncio.run(check())
