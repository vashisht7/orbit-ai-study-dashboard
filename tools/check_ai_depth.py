"""Check lesson contracts, links, and execute every self-contained Python example."""
import json
import re
from pathlib import Path
from build_ai_depth import ROOT, build


def main():
    data = build()
    text = (ROOT / 'problems-data.js').read_text()
    problems = json.JSONDecoder().raw_decode(text.split('const PROBLEMS=', 1)[1])[0]
    problem_ids = {p['id'] for p in problems}
    chapters = data['chapters']
    by_id = {c['id']: c for c in chapters}
    code_count = questions = 0
    for c in chapters:
        assert c['practice'] in problem_ids, (c['id'], c['practice'])
        assert c['words'] >= 400, c['id']
        assert 1 <= c['foundation'] <= 30
        assert c['sources'] and all(s['url'].startswith('https://') for s in c['sources'])
        body = c['body']
        assert body.count('```') % 2 == 0, c['id']
        qa = body.split('## Interview rehearsal\n')[1].split('## Prove it yourself\n')[0]
        count = len(re.findall(r'^### ', qa, re.M))
        assert count == 3, c['id']
        questions += count
        for block in re.findall(r'```python\n(.*?)\n```', body, re.S):
            assert 'assert ' in block, c['id']
            exec(compile(block, f'{c["id"]} teaching example', 'exec'), {})
            code_count += 1
        for url in re.findall(r'\]\(([^)]+)\)', body):
            if not url.startswith(('https://', '#')):
                assert (ROOT / 'ai-depth' / url.split('#')[0]).exists(), url
    for day in range(1, 31):
        assert any(day in c['days'] for c in chapters), f'No depth links for day {day}'
    def walk(id, ancestors):
        assert id not in ancestors, f'Prerequisite cycle: {id}'
        for prereq in by_id[id]['prereq']:
            walk(prereq, ancestors | {id})
    for c in chapters:
        walk(c['id'], set())
    # The root entry now redirects to the unified dark study plan; the
    # legacy visual-map and beginner pages retain their AI-depth links.
    assert "ai-depth/index.html" in (ROOT / 'index.html').read_text()
    for path in ['visual-map.html', 'beginner/index.html']:
        assert 'ai-depth-links.js' in (ROOT / path).read_text(), path
    assert code_count == 27 and questions == 84
    print(f'{len(chapters)} chapters: {code_count} executable examples passed, {questions} answers, 30 daily mappings, Code Lab links, and acyclic prerequisites verified.')


if __name__ == '__main__':
    main()
