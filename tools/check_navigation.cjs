const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://127.0.0.1:8765';
(async()=>{
  const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/ai-depth/index.html');await page.waitForSelector('.study-stage');
  const original={days:{1:{checks:{reading:true,coding:true,design:true,lab:true,recall:true,localai:true},notes:'Keep original notes',quizDone:true},5:{checks:{coding:false,design:false},notes:'Keep Day 5'},12:{checks:{coding:true,design:true},notes:'Later progress'}},last:12,streak:{count:7},achievements:{test:true}};
  await page.evaluate(p=>{localStorage.setItem('orbit-ai-progress-v1',JSON.stringify(p));localStorage.setItem('orbit.practice.v1',JSON.stringify({solved:{'two-sum':true},code:{'two-sum':'# my solution'}}));localStorage.setItem('beginner-ai-practiced','["01","06"]');},original);
  await page.reload();await page.waitForSelector('.study-stage');
  let saved=await page.evaluate(()=>DAILY_STUDY.progress());
  for(const d of [1,5,12]){assert.equal(saved.days[d].notes,original.days[d].notes);for(const [k,v] of Object.entries(original.days[d].checks))assert.equal(saved.days[d].checks[k],v);}
  assert.equal(saved.last,12);assert.equal(saved.streak.count,7);assert.equal(saved.days[1].quizDone,true);
  const urls=new Set();
  for(let d=1;d<=30;d++){
    await page.goto(base+'/index.html#day-'+d);await page.waitForSelector('.study-steps');
    for(const [i,step] of ['learn','coding','design','explain'].entries()){
      await page.locator(`[data-study-step="${i}"]`).click();
      await page.waitForFunction(s=>document.querySelector('[aria-current="step"]')?.getAttribute('href').endsWith('/'+s),step);
      assert.ok(page.url().endsWith('/'+step));
      for(const a of await page.locator('.study-stage a').evaluateAll(as=>as.map(a=>a.href)))if(a.startsWith(base))urls.add(a.split('#')[0]);
    }
    await page.reload();await page.waitForSelector('[aria-current="step"]');assert.equal(await page.locator('[aria-current="step"]').getAttribute('data-study-step'),'3');
  }
  for(const url of urls){const response=await page.request.get(url);assert.equal(response.status(),200,url);}
  await page.goto(base+'/ai-depth/index.html#day-6/learn');await page.waitForSelector('.study-stage');
  await page.locator('[data-study-step="1"]').click();await page.waitForFunction(()=>location.hash.endsWith('/coding'));
  await page.goBack();await page.waitForSelector('[data-study-step="0"][aria-current="step"]');await page.goForward();await page.waitForSelector('[data-study-step="1"][aria-current="step"]');
  const exercise=page.locator('.study-stage a.button');assert.equal(await exercise.getAttribute('target'),null);
  await page.locator('#study-note').fill('Persist after a refresh');await page.reload();await page.waitForSelector('#study-note');assert.equal(await page.locator('#study-note').inputValue(),'Persist after a refresh');
  const event=page.waitForEvent('download');await page.locator('#study-export').click();const dl=await event;const file=await dl.path();const backup=JSON.parse(require('fs').readFileSync(file));assert.match(backup.storage['orbit.practice.v1'],/my solution/);
  await page.evaluate(()=>localStorage.removeItem('orbit.practice.v1'));await page.locator('#study-import').setInputFiles(file);await page.waitForFunction(()=>localStorage.getItem('orbit.practice.v1')?.includes('my solution'));
  await page.locator('header a[href="#library"]').click();await page.waitForSelector('.cards .card');assert.equal(await page.locator('.cards .card').count(),28);
  await page.locator('.cards .card a').first().click();await page.waitForSelector('.flow');await page.reload();await page.waitForSelector('.flow');
  await page.locator('header a[href="#overview"]').first().click();await page.waitForSelector('.study-stage');
  for(const width of [390,1440]){await page.setViewportSize({width,height:900});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:`/tmp/orbit-navigation-${width}.png`,fullPage:false});}
  assert.deepEqual(errors,[]);await browser.close();console.log('PASS: actual day/step links, 30 refreshes, history, local destinations, preserved old progress, full backup, reference navigation, responsive layout.');
})().catch(e=>{console.error(e);process.exit(1)});
