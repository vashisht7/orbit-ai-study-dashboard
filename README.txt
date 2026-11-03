Mechanism animation update (November 3, 2026)
Inside the model now provides a computed Transformer architecture view with
residual bypasses, two-head attention with a causal-mask heatmap, an inspectable
feed-forward neuron network (4 -> 8 -> 4), and real browser bigram training.
The Watch tabs for model-internals lessons open these specialized views.
All displayed matrices, weighted sums, activations, and losses are calculated.
Fixed teaching weights are clearly separate from live trained weights.

Train a small model -> Write it yourself provides a starter notebook with seven
unfinished implementation exercises, a reference notebook, shape/causality
checks, controlled learning-rate experiments, plots, generation, and export.
Use local JupyterLab, VS Code notebooks, or Colab; full PyTorch execution occurs
there, not in the static dashboard. The browser bigram model is explicitly not
a Transformer. No extra animation plugin is needed.
Rebuild notebook artifacts and ZIP: node tools/build_learning.cjs.
Check browser math: node tools/check_mechanisms.cjs.
Check notebook code: python tools/check_transformer_notebooks.py (PyTorch,
Matplotlib and nbformat required). Original readers and progress are retained.

Orbit AI notebook — two connected learning paths (November 3, 2026)

Open index.html for the simplified dashboard. It works locally without a build.
1. Learn AI: 30 lessons, plain-language explanations, sketch-style animated
   flows, small Python examples, quizzes, and personal notes.
2. Interview preparation: six resume project routes and 28 concept deep dives,
   linked back to beginner explanations and hands-on lessons.
3. Train a small model: a downloadable CPU PyTorch workshop with explained
   source, custom text input, held-out loss, checkpoints, resume, generation,
   and a local metrics-file chart. Actual model training runs in Python.

The sidebar collapses using the top-left button. Each lesson has Understand,
Watch, Try & code, and Explain steps. Animations have play/pause, step, reset,
and speed controls. Attention/softmax and gradient lessons include live numeric
experiments. Notes and practiced flags use orbit-two-paths-v1 browser storage;
Save progress exports them and Restore progress merges them. Original progress
is untouched and remains available in classic-dashboard.html.

The original dashboard and all reference readers remain available. The new
resume routes reuse ai-depth/resume-path.js; reported resume metrics retain
their original scope and should be supported by the learner's own evidence.
Maintain the small-model workshop in learning/model-workshop/. Regenerate its
embedded source with node tools/build_learning.cjs after changing source files.
The training checkpoint test is tools/check_model_workshop.py (needs PyTorch).

Earlier dashboard notes follow; their original daily UI is now classic-dashboard.html.

Vashisht AI Interview Study Dashboard

Open index.html in Arc or another browser. Keep all files in this folder together.
Choose a week and a day to see the assigned coding, AI reading, design, and project practice.
The textbook, labs, and resume are included. Hello Interview lessons require internet access and your existing account for Premium content.
Daily schedule: 60 minutes coding, 45 minutes AI reading and recall, 45 minutes design, 30 minutes implementation or project evidence.
This is a 30-day first pass; use the readiness checks and repeat weak areas before interviews.

The advanced dark reference reader is included in reader/index.html. Daily AI assignments now link to the beginner course. All 62 chapters are available; chapters 1-53 contain new deeper explanations. Original PDF downloads retain the earlier print edition; the expanded text is in the website. All reading assets and interactive libraries are included locally.

Easy learning edition: open cheatsheet.html for all 27 topics with NoteEchoes examples, model-process.html for the model walkthrough, or NoteEchoes_AI_Cheatsheet.pdf for the complete 38-page dark PDF.

Start here: beginner/index.html. The new 30-lesson beginner course includes an updated first-principles PDF, 29 small runnable labs, an optional tested PyTorch decoder, plain-language math and interactive parameter experiments. Spend 20 minutes reading, 15 minutes running and changing one example, and 10 minutes explaining it aloud. Repeat a lesson when needed; 30 sessions need not mean 30 calendar days. The earlier book and cheat sheet remain available as references.


Code Lab expansion (October 4, 2026): 84 Python exercises with walkthroughs,
complexity, pitfalls, follow-ups, profile relevance, and company-source links.
Company reports are historical/self-reported; role practice is labeled separately.
Use company, topic, study-track, difficulty, and day filters.

Daily exercise routing is maintained in coding-routes.js against the public Hello
Interview catalog. Exact matching lessons use Hello Interview; local practical
exercises and mocks open specific Code Lab problems. The unsorted Two Sum and
local array-merge contracts are different from the external sorted/linked-list variants.

Each of the 30 beginner lessons has a shared simple explanation and clickable
flow diagram, also available in Visual Map's topic explorer. Visual Map includes
a coverage review and five bridge notes for areas needing a second study pass.

Maintain problem content in tools/gen_problems.py, tools/interview_problems.py,
and tools/problem_notes.py, then run python3 tools/gen_problems.py. Validate with
python3 tools/check_problems.py. The original 40 have generated expected results;
the added problems have independently specified expected results.

AI Deep Dives (October 6, 2026): open ai-depth/index.html for 28 personalized
chapters supplementing the 30 beginner lessons and 62-chapter reference.
Includes 27 checked Python examples, 28 clickable concept diagrams, six types
of interactive calculators, 84 interview questions, four system-design cases,
and browser-local evidence notes with export/import. Every daily lesson links
to relevant deep dives. Examples are synthetic; proposed designs are clearly
distinguished from actual resume claims. Original PDFs are unchanged; use the
chapter print button or ai-depth/content.md for the new offline material.

Edit ai-depth/content.md and ai-depth/sources.json, then run
python3 tools/build_ai_depth.py and python3 tools/check_ai_depth.py.
Sources were reviewed October 6, 2026; living APIs need rechecking when used.

Daily AI simplification (October 6, 2026): ai-depth/index.html now starts a
guided 30-day route matching the dashboard. Each day has Learn, Example, and
Explain steps, a short recall answer, notes, and an explicit practiced toggle.
Full foundation and interview lessons remain expandable in the day itself;
existing chapter URLs and the reference library remain available. Daily progress
uses orbit-ai-daily-v1 without overwriting dashboard or reference progress.
Notes export/import includes both the older reference notes and daily progress.


First-principles revision (October 15, 2026): all 30 daily lessons now explain
the concept, symbols, rule and derivation before a worked example. The dashboard
and beginner reader put interactive practice after the lesson, and use specific
recall questions. The beginner PDF matches this revision; earlier reference-book
PDFs remain separate historical materials. Read beginner/manuscript.md offline.


Meaning and visual revision: every day now includes why the idea is needed,
what it changes, a labeled project illustration and instructions for reading
the visual. A dedicated Lesson animation tab opens the current day directly;
the gallery/job audit is separate. Concept walkthroughs no longer display
invented response percentages. Static diagrams expose sliders rather than
nonfunctional playback controls. The beginner PDF includes the expanded text.
