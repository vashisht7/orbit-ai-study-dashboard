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


Daily visual guidance is extracted from the manuscript's “Why we need this”,
“What changes when you use it”, “A project connection” and “Read the visual”
sections. Every visual uses that same explanation. Quantitative diagrams must
calculate the stated quantity; conceptual flows must say they are walkthroughs
and must not display invented outcome metrics. Time-driven visuals have playback
controls; parameter-driven static diagrams have sliders and Reset.

## Local AI companion track

`local-ai/lessons.json` contains 30 distinct lessons. `tools/build_local_ai.cjs`
adds explicit consequences and primary references, and emits `local-ai/course.js`
and the downloadable `local-ai/guide.md`. It runs as part of the study build.
The dashboard tab, daily spotlight and checklist all open `#day-N/local-ai`.
The shared NoteEchoes simulator stays separately accessible as `#day-N/lab`.
Local AI completion uses the existing `localai` progress key; no stored notes or
old completion marks are cleared. The reader explicitly labels this as expanded
content so existing completion does not imply the new lessons were read.

## Calm chapter navigation

`learning-path.js` defines five subject chapters and 30 distinct session outcomes.
Lesson routes and stored day keys are retained for compatibility. The main path
uses reading checks as self-reported progress, not all six optional activities.
The page starts with one goal, a reason to learn it and a stopping point. Extra
practice, project views and tool controls use expandable sections. The dedicated
animation tab remains directly available. Validate chapter boundaries (1, 9, 14,
21, 27), all 30 goals, optional-view entry points and saved notes when editing.

## Reading layout and Focus mode

`reading-layout.css` owns dashboard header/toolbar positioning and responsive Focus
layout. Keep the progress track inside `.bookbar`; it must not have an independent
sticky offset. Header and toolbar sizes are observed in `orbit.js` and supply
scroll offsets for section links. Focus hides the surrounding dashboard, preserves
the current reading block, and exits through its button or Escape. The tools menu
is a bounded dropdown, not extra content inside a fixed-height header.

Layout verification: test 1440, 820, 390 and 320 px widths; open/close Tools;
enter Focus, scroll into a later section, exit by button and Escape; check the
progress line is at the toolbar bottom and the exit button remains in view.
Switch Read, Animation, Recall and Local AI while focused. Compare notes and task
checks before/after. No horizontal page overflow or browser errors should occur.

## Training walkthrough (Lessons 6–8)

`training-story.js` and `training-story.css` provide an eight-scene, captioned
walkthrough with Play/Pause, Previous/Next, direct scene selection and Restart.
It is embedded early in both readers and directly accessible at
`#day-6/training`. All numbers derive from y_hat=x*w, squared error and mean batch
loss; the weight remains 1 until the optimizer scene. Check both batch sizes and
all three learning rates against a numerical derivative when modifying it.
Lesson 7's manuscript and `lesson_07.py` now perform the same two-example update.
Rebuild the PDF and lab ZIP when changing that downloadable lesson.
