# Publishing the study site

The original dashboard, separate résumé reference, CodeLab, beginner reader, and visual map load ordered script bundles. Edit the source JavaScript files, then run `node tools/build_study.cjs` and commit generated bundles alongside source changes. Bump the affected HTML bundle query versions on release. The retired unified-view sources remain in version control but are not loaded by the restored dashboard.

Keep existing browser storage keys. Never clear progress during an upgrade. The dashboard exports daily progress, reference notes, CodeLab solutions and drafts, and reading completion; it saves a recovery copy before importing a backup. Old unified-view notes remain visible under the original day notes.

Browser checks (with Playwright available in `NODE_PATH`):

- `node tools/check_restored.cjs`: all 30 original lessons, saved progress and notes, six daily activities, separate reference chapters and legacy routes. `BASE_URL` can point to GitHub Pages.
- The older `check_navigation.cjs`, `check_unified.cjs`, and `check_ai_depth.cjs` target the retired unified UI and are retained as historical checks.
- `python3 tools/check_ai_depth.py`: chapter structure and executable examples. Run the bundle build again if this regenerates content.

The site is static. Progress stays on the current origin and browser; export and restore a backup to move subsequent progress between devices or from localhost to GitHub Pages.


## Maintaining the 30 daily lessons

Edit `beginner/manuscript.md` for all lesson prose, `beginner/lesson-meta.json`
for navigation metadata, and `beginner/checks.json` for the 30 specific quizzes.
The manuscript is the source of truth for the dashboard and beginner reader.
Explain the concept, define every symbol, derive or justify the rule, identify
chosen versus learned quantities, and only then give the worked example.
Non-mathematical lessons should justify the mechanism rather than invent a formula.

`node tools/build_study.cjs` now builds the course first and runs all 29 standard
Python labs. The embedded example must match its downloadable lab exactly.
Run `node tools/check_beginner.cjs` for all 60 lesson views, strict formula
rendering, quizzes, reading order and mobile/desktop checks. Run
`node tools/check_restored.cjs` to verify saved progress and legacy navigation.
Both browser checks require Playwright and a local server on port 8765.

`node tools/export_beginner_pdf.cjs` prints the same lesson data with KaTeX.
It writes `output/pdf/AI_Engineering_First_Principles.pdf` and refreshes the
existing `beginner/Beginner_AI_Engineering.pdf` download. The reader PDF is tracked for GitHub Pages; other PDFs remain ignored by
Git. Regenerate and commit the reader PDF when publishing lesson changes. The optional PyTorch decoder is not run by the standard-library
build and requires a separate PyTorch environment.
