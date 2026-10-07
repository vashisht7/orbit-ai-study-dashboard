# Publishing the study site

The study plan, CodeLab, beginner reader, and visual map load one ordered script bundle each. Edit the source JavaScript files, then run `node tools/build_study.cjs` and commit the generated bundles alongside the source changes. Bump the bundle query version in the four HTML entry pages when publishing a new release.

Keep the existing browser storage keys. Never clear progress during an upgrade. The unified reader exports daily progress, reference notes, CodeLab solutions and drafts, and reading completion; it saves a recovery copy before importing a backup.

Browser checks (with Playwright available in `NODE_PATH`):

- `node tools/check_navigation.cjs`: actual day and step links, refresh, history, saved progress, backups, and local exercise destinations. `BASE_URL` can point to GitHub Pages.
- `node tools/check_ai_depth.cjs`: reference chapters, calculators, downloads, notes, and mobile layouts.
- `python3 tools/check_ai_depth.py`: chapter structure and executable examples. Run the bundle build again if this regenerates content.

The site is static. Progress stays on the current origin and browser; export and restore a backup to move subsequent progress between devices or from localhost to GitHub Pages.
