# Publishing the study site

The original dashboard, separate résumé reference, CodeLab, beginner reader, and visual map load ordered script bundles. Edit the source JavaScript files, then run `node tools/build_study.cjs` and commit generated bundles alongside source changes. Bump the affected HTML bundle query versions on release. The retired unified-view sources remain in version control but are not loaded by the restored dashboard.

Keep existing browser storage keys. Never clear progress during an upgrade. The dashboard exports daily progress, reference notes, CodeLab solutions and drafts, and reading completion; it saves a recovery copy before importing a backup. Old unified-view notes remain visible under the original day notes.

Browser checks (with Playwright available in `NODE_PATH`):

- `node tools/check_restored.cjs`: all 30 original lessons, saved progress and notes, six daily activities, separate reference chapters and legacy routes. `BASE_URL` can point to GitHub Pages.
- The older `check_navigation.cjs`, `check_unified.cjs`, and `check_ai_depth.cjs` target the retired unified UI and are retained as historical checks.
- `python3 tools/check_ai_depth.py`: chapter structure and executable examples. Run the bundle build again if this regenerates content.

The site is static. Progress stays on the current origin and browser; export and restore a backup to move subsequent progress between devices or from localhost to GitHub Pages.
