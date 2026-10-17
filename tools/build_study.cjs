// Ship the daily reader as one versioned script so cached dependencies cannot disagree.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
require('node:child_process').execFileSync(process.env.PYTHON || 'python3', [path.join(__dirname, 'build_beginner.py')], {stdio: 'inherit'});
require('./build_local_ai.cjs');
const bundles = {
  'dashboard.bundle.js':['local-ai/course.js','reader/vendor/marked.js','reader/vendor/katex.min.js','plan-data.js','coding-routes.js','ai-depth-links.js','beginner/course.js','beginner/experiments.js','lesson-guides.js','manim-visuals.js','learning-guides.js','orbit.js'],
  'ai-depth/reference.bundle.js':['reader/vendor/marked.js','beginner/course.js','lesson-guides.js','manim-visuals.js','ai-depth/content.js','ai-depth/resume-path.js','ai-depth/app.js'],
  'practice.bundle.js':['reader/vendor/marked.js','plan-data.js','coding-routes.js','problems-data.js','walkthroughs-data.js','solution-walkthrough.js','practice.js'],
  'beginner/study.bundle.js':['reader/vendor/marked.js','reader/vendor/katex.min.js','beginner/course.js','beginner/experiments.js','coding-routes.js','ai-depth-links.js','lesson-guides.js','manim-visuals.js','learning-guides.js','beginner/app.js'],
  'vmap.bundle.js':['plan-data.js','coding-routes.js','ai-depth-links.js','problems-data.js','beginner/course.js','lesson-guides.js','manim-visuals.js','learning-guides.js','vmap.js']
};
for(const [output,files] of Object.entries(bundles)) {
  fs.writeFileSync(path.join(root,output), files.map(f=>`\n/* ${f} */\n${fs.readFileSync(path.join(root,f),'utf8')}\n;`).join('\n'));
}
console.log('Built five ordered page bundles.');
