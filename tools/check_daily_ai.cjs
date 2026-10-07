const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1050},acceptDownloads:true});
 const base=process.env.BASE_URL||'http://127.0.0.1:8765';const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`${base}/ai-depth/index.html`);await page.waitForSelector('.daily-panel');
 assert.match(await page.title(),/^Day 1:/);assert.equal(await page.locator('#library').isVisible(),false);
 for(let day=1;day<=30;day++){
  await page.goto(`${base}/ai-depth/index.html#day-${day}`);await page.waitForSelector('[data-daily-step]');
  assert.match(await page.title(),new RegExp(`^Day ${day}:`));
  assert.equal(await page.locator('.daily-steps button').count(),3);
  assert.equal(await page.locator('.day-grid a').count(),30);
  assert.ok((await page.locator('.daily-panel .prose').first().innerText()).length>100);
  await page.click('[data-daily-flow="3"]');assert.equal(await page.locator('[data-daily-flow="3"]').getAttribute('aria-pressed'),'true');
  await page.click('#daily-next');assert.equal(await page.locator('[data-daily-step="1"]').getAttribute('aria-pressed'),'true');
  assert.ok((await page.locator('.simple-example').innerText()).length>25);
  const expected=await page.evaluate(d=>HELLO_PROBLEMS?.[LESSON_GUIDES[d-1].problem]||'../practice.html#'+LESSON_GUIDES[d-1].problem,day);
  assert.equal(await page.locator('.daily-panel .button').getAttribute('href'),expected);
  await page.click('#daily-next');await page.locator('.daily-answer summary').first().click();
  assert.ok((await page.locator('.daily-answer p').first().innerText()).length>50);
  assert.equal(await page.locator('.daily-extra details').count(),3);
 }
 await page.goto(`${base}/ai-depth/index.html#day-1`);await page.waitForSelector('#daily-note');
 await page.fill('#daily-note','I separate a model proposal from an authorized action.');
 await page.click('#daily-done');assert.match(await page.locator('.daily-finished').innerText(),/marked Day 1/);
 await page.reload();await page.waitForSelector('#daily-note');assert.match(await page.locator('#daily-note').inputValue(),/authorized action/);
 await page.goto(`${base}/ai-depth/index.html`);assert.match(await page.title(),/^Day 2:/);
 await page.click('#menu');const dl=page.waitForEvent('download');await page.click('#export');const file=await dl;const path=await file.path();
 await page.evaluate(()=>localStorage.removeItem('orbit-ai-daily-v1'));await page.reload();assert.match(await page.title(),/^Day 1:/);
 await page.click('#menu');await page.setInputFiles('#import',path);await page.waitForFunction(()=>document.title.startsWith('Day 2:'));
 await page.goto(`${base}/ai-depth/index.html#day-1`);await page.click('#daily-done');assert.equal(await page.locator('.daily-finished').count(),0);
 await page.goto(`${base}/ai-depth/index.html?day=24`);assert.match(await page.title(),/^Day 24:/);
 await page.goto(`${base}/ai-depth/index.html?day=2.5`);assert.match(await page.title(),/^Day 1:/);
 await page.goto(`${base}/ai-depth/index.html#day-15`);await page.click('[data-daily-step="0"]');await page.evaluate(()=>scrollTo(0,0));
 await page.screenshot({path:'/tmp/daily-ai-desktop.png'});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/daily-ai-mobile.png'});
 for(const day of [1,9,15,24,30]){
  await page.goto(`${base}/ai-depth/index.html#day-${day}`);
  for(let step=0;step<3;step++){
   await page.click(`[data-daily-step="${step}"]`);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`Mobile overflow day ${day} step ${step}`);
  }
 }
 await page.goto(`${base}/ai-depth/index.html#adaptation`);assert.equal(await page.locator('.simulator').count(),1);
 await page.goto(`${base}/index.html#day-15`);await page.waitForSelector('.learn-depth a');assert.equal(await page.locator('.learn-depth a').count(),1);
 assert.equal(await page.locator('.learn-depth a').getAttribute('href'),'ai-depth/index.html#day-15');
 assert.deepEqual(errors,[]);console.log('30 daily lessons, 90 steps, answers, exercise routing, resume/undo, notes/export/import, old reference links, and mobile views passed.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
