"""Build all 30 daily lessons from the reviewable manuscript and lab files."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'beginner'


def build():
    text = (BOOK / 'manuscript.md').read_text()
    starts = list(re.finditer(r'^# (\d{2})\. (.+)\n', text, re.M))
    metadata = json.loads((BOOK / 'lesson-meta.json').read_text())
    checks = json.loads((BOOK / 'checks.json').read_text())
    assert len(starts) == len(metadata) == len(checks) == 30
    lessons, outputs = [], {}
    for i, start in enumerate(starts):
        item = dict(metadata[i])
        assert start[1] == item['id'] == f'{i+1:02}'
        assert start[2] == item['title']
        body = text[start.end():starts[i+1].start() if i+1 < len(starts) else len(text)].strip()
        assert body.startswith('### The concept:'), item['id']
        assert '### Worked example:' in body and '### Check your understanding' in body
        assert body.index('### Worked example:') < body.index('```python')
        assert '{{LAB}}' not in body
        blocks = re.findall(r'^```python\n(.*?)\n```', body, re.M | re.S)
        assert len(blocks) == 1, item['id']
        lab = BOOK / 'labs' / item['lab']
        assert blocks[0].rstrip() == lab.read_text().rstrip(), f"Lab drift: {lab}"
        output = ''
        if i < 29:
            result = subprocess.run([sys.executable, str(lab)], capture_output=True, text=True, check=True, timeout=10)
            output = result.stdout.strip()
            outputs[item['id']] = output
        q, answer, *wrong = checks[i]
        options = [{'t': answer, 'c': True}] + [{'t': x, 'c': False} for x in wrong]
        offset = i % len(options)
        options = options[offset:] + options[:offset]
        meaning = {}
        for key, heading in [('why', 'Why we need this'), ('change', 'What changes when you use it'), ('project', 'A project connection'), ('watch', 'Read the visual')]:
            match = re.search(r'^### ' + re.escape(heading) + r'\n(.*?)(?=^### |\Z)', body, re.M | re.S)
            assert match and match[1].strip(), (item['id'], heading)
            meaning[key] = match[1].strip()
        item.update(body=body, output=output, meaning=meaning, quiz={
            'q': q, 'options': options,
            'hint': answer,
        })
        lessons.append(item)
    (BOOK / 'course.js').write_text('window.BEGINNER = ' + json.dumps(lessons, ensure_ascii=False) + ';\n')
    (BOOK / 'lab-checks.json').write_text(json.dumps({'standard_library_labs': 29, 'all_passed': True, 'outputs': outputs}, indent=2)+'\n')
    print(f"Built {len(lessons)} concept-first lessons; all 29 standard-library labs passed.")
    return lessons


if __name__ == '__main__':
    build()
