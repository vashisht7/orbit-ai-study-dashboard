const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base=process.env.BASE_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try {
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const report=[];
 for(const reader of ['index.html#day-','beginner/index.html#lesson-']){
  for(let d=1;d<=30;d++){
   const standalone=reader.startsWith('beginner/'), id=standalone?String(d).padStart(2,'0'):d;
   await page.goto(`${base}/${reader}${id}`);
   await page.waitForFunction(()=>window.BEGINNER?.length===30);
   const root=standalone?'#lesson':'#reading';
   await page.locator(root+' h3').first().waitFor();
   const checks=await page.locator(root).evaluate(el=>{
    const headings=[...el.querySelectorAll('h3')].map(h=>h.textContent);
    const code=el.querySelector('pre');const experiment=el.querySelector('#experiment');
    const worked=[...el.querySelectorAll('h3')].find(h=>h.textContent.startsWith('Worked example:'));
    const before=(a,b)=>Boolean(a.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING);
    return {concept:headings[0].startsWith('The concept:'),workedBeforeCode:before(worked,code),codeBeforePractice:before(code,experiment),mathErrors:el.querySelectorAll('.katex-error').length,formulaCount:el.querySelectorAll('.katex').length,rawBlocks:el.innerText.includes('BOOKBLOCK'),animationExposed:!!el.querySelector('.lesson-animation .b1b-canvas')&&!el.querySelector('.lesson-animation')?.closest('details')};
   });
   assert.ok(checks.concept&&checks.workedBeforeCode&&checks.codeBeforePractice&&checks.animationExposed,`${reader}${id} reading order`);
   assert.equal(checks.mathErrors,0,`${reader}${id} equations`);assert.equal(checks.rawBlocks,false);
   if(!standalone){
    assert.equal(await page.locator('.quiz-opt-btn').count(),3);
    assert.ok(await page.locator('.quick-check-prompt').innerText());
    assert.equal(await page.locator('.task input[type=checkbox]').count(),6);
   }
   report.push({reader:standalone?'beginner':'dashboard',day:d,...checks});
  }
 }
 // The strict reader throws on invalid math, so also render every lesson in a single pass.
 const math=await page.evaluate(()=>BEGINNER.map(c=>({id:c.id,rendered:renderBeginner(c.body).length,quiz:c.quiz.options.filter(o=>o.c).length})));
 assert.ok(math.every(c=>c.rendered>1000&&c.quiz===1));
 // Actually submit an incorrect and correct answer on the first-principles gradient check.
 await page.goto(base+'/index.html#day-6');await page.locator('.quiz-opt-btn').first().waitFor();
 await page.locator('.quiz-opt-btn[data-correct="false"]').first().click();
 assert.equal(await page.locator('.quiz-opt-btn:disabled').count(),0);
 await page.locator('.quiz-opt-btn[data-correct="true"]').click();
 assert.equal(await page.locator('.quiz-opt-btn:disabled').count(),3);
 // The day's animation is one click away, independently of the audit.
 await page.locator('[data-open-lesson-animation]').click();
 assert.match(page.url(),/#day-6\/animation$/);
 assert.equal(await page.locator('#job-readiness-hub').count(),0);
 assert.equal(await page.locator('.b1b-theater[data-b1b-day="6"] canvas').isVisible(),true);
 await page.locator('[data-b1b-action="reset"]').click();
 assert.match(await page.locator('.b1b-telemetry').innerText(),/Step 0/);
 await page.locator('[data-b1b-action="step"]').click();
 assert.match(await page.locator('.b1b-telemetry').innerText(),/Step 1/);
 await page.locator('#animation-back').click();
 await page.locator('#job-audit-pill').click();
 assert.equal(await page.locator('#job-readiness-hub').isVisible(),true);
 const dir=path.resolve(__dirname,'../tmp/lesson-rewrite');fs.mkdirSync(dir,{recursive:true});
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:1000});
  await page.goto(base+'/index.html#day-6');await page.locator('#reading h3').first().waitFor();
  const h=page.locator('#reading h3').first();await h.scrollIntoViewIfNeeded();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2),`page overflow ${width}`);
  await page.screenshot({path:path.join(dir,`day6-${width}.png`)});
  await page.goto(base+'/beginner/index.html#lesson-09');await page.locator('#lesson h3').first().waitFor();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2),`reader overflow ${width}`);
  await page.screenshot({path:path.join(dir,`attention-${width}.png`)});
 }
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.resolve(__dirname,'../beginner/browser-checks.json'),JSON.stringify({passed:true,views:report.length,equations:math.length,quizInteraction:true,mobileAndDesktop:true,lessons:report},null,2)+'\n');
 console.log('PASS: 60 daily lesson views, concept/derivation/example/practice order, strict math rendering, 30 specific quizzes, quiz interaction, direct animation access, step/reset, separate audit, and mobile/desktop overflow.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
