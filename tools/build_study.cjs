// Ship the daily reader as one versioned script so cached dependencies cannot disagree.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const bundles = {
  'ai-depth/study.bundle.js':['reader/vendor/marked.js','reader/vendor/katex.min.js','ai-depth/content.js','beginner/course.js','lesson-guides.js','coding-routes.js','plan-data.js','ai-depth/daily.js','ai-depth/game.js','ai-depth/unified.js','ai-depth/app.js'],
  'practice.bundle.js':['reader/vendor/marked.js','plan-data.js','coding-routes.js','problems-data.js','walkthroughs-data.js','solution-walkthrough.js','practice.js'],
  'beginner/study.bundle.js':['reader/vendor/marked.js','reader/vendor/katex.min.js','beginner/course.js','beginner/experiments.js','coding-routes.js','ai-depth-links.js','lesson-guides.js','learning-guides.js','beginner/app.js'],
  'vmap.bundle.js':['plan-data.js','coding-routes.js','ai-depth-links.js','problems-data.js','lesson-guides.js','learning-guides.js','vmap.js']
};
for(const [output,files] of Object.entries(bundles)) {
  fs.writeFileSync(path.join(root,output), files.map(f=>`\n/* ${f} */\n${fs.readFileSync(path.join(root,f),'utf8')}\n;`).join('\n'));
}
console.log('Built four ordered page bundles.');
