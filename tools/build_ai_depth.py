"""Build the static personalized AI reader from reviewable Markdown.

No model calls or network are needed. Run from any directory.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'ai-depth'


def build():
    sources = json.loads((FOLDER / 'sources.json').read_text())
    text = (FOLDER / 'content.md').read_text()
    pattern = r'^# ([a-z0-9-]+) \| (.+)\n<!-- (.+) -->\n'
    matches = list(re.finditer(pattern, text, re.M))
    chapters = []
    foundations = [27, 21, 7, 10, 11, 13, 14, 15, 16, 21, 18, 20, 19, 24, 25, 26, 26, 23, 23, 24, 26, 16, 26, 26, 18, 28, 23, 27]
    for i, match in enumerate(matches):
        body = text[match.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
        chapter = json.loads(match[3])
        chapter.update(id=match[1], title=match[2], body=body, number=i+1)
        chapter['foundation'] = foundations[i]
        chapter['words'] = len(body.split())
        chapter['minutes'] = max(5, round(chapter['words'] / 150))
        chapter['sources'] = [dict(title=sources[k][0], url=sources[k][1], checked='2026-10-06') for k in chapter['refs']]
        chapters.append(chapter)
    ids = {c['id'] for c in chapters}
    assert len(ids) == len(chapters) == 28
    for chapter in chapters:
        assert all(p in ids for p in chapter['prereq']), chapter['id']
        assert len(chapter['flow']) == 4
        assert all(1 <= day <= 30 for day in chapter['days'])
        for heading in ['## Interview rehearsal', '## Prove it yourself']:
            assert heading in chapter['body'], (chapter['id'], heading)
    manifest = [{k: c[k] for k in ['id', 'title', 'track', 'days', 'projects', 'number']} for c in chapters]
    data = dict(reviewed='2026-10-06', chapters=chapters, words=sum(c['words'] for c in chapters))
    (FOLDER / 'content.js').write_text('window.AI_DEPTH = ' + json.dumps(data, ensure_ascii=False) + ';\n')
    (ROOT / 'ai-depth-links.js').write_text('window.AI_DEPTH_LINKS = ' + json.dumps(manifest, ensure_ascii=False) + ';\n')
    print(f"Built {len(chapters)} chapters, {data['words']:,} words, {len({r for c in chapters for r in c['refs']})} primary references.")
    return data


if __name__ == '__main__':
    build()
