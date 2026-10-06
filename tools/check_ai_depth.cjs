/* Run with Playwright available in NODE_PATH. BASE_URL and CHROME_PATH are optional. */
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const page = await browser.newPage({viewport:{width:1440,height:1050},acceptDownloads:true});
  const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto(`${base}/ai-depth/index.html`);
  await page.waitForSelector('.cards .card');
  assert.equal(await page.locator('.cards .card').count(),28);
  const chapters = await page.evaluate(()=>AI_DEPTH.chapters.map(c=>({id:c.id,title:c.title,sim:c.sim})));
  for (const c of chapters) {
    await page.evaluate(id=>location.hash=id,c.id);
    await page.waitForFunction(title=>document.querySelector('h1').textContent===title,c.title);
    assert.equal(await page.locator('.interview').count(),3,c.id);
    assert.equal(await page.locator('.flow button').count(),4,c.id);
    await page.locator('[data-step="3"]').click();
    assert.equal(await page.locator('[data-step="3"]').getAttribute('aria-pressed'),'true');
    assert.ok((await page.locator('.flow-detail').innerText()).length>30,c.id);
    await page.locator('.interview summary').first().click();
    assert.ok(await page.locator('.interview').first().getAttribute('open') !== null,c.id);
    assert.ok(await page.locator('.sources a').count()>=1,c.id);
    if(c.sim) assert.ok((await page.locator('.sim-result').innerText()).length>10,c.id);
  }
  async function go(id){await page.goto(`${base}/ai-depth/index.html#${id}`);await page.waitForSelector('.flow');}
  async function slide(id,value){await page.locator(`#sim-${id}`).evaluate((e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));},String(value));}
  await go('inference');assert.match(await page.locator('.sim-result').innerText(),/192 MiB/);
  await slide('batch',4);assert.match(await page.locator('.sim-result').innerText(),/768 MiB/);
  await go('adaptation');assert.match(await page.locator('.sim-result').innerText(),/16,384/);
  await slide('rank',16);assert.match(await page.locator('.sim-result').innerText(),/32,768/);
  await go('ml-decisions');await slide('threshold',100);assert.match(await page.locator('.sim-result').innerText(),/undefined/);
  await go('evaluation-data');assert.match(await page.locator('.sim-result').innerText(),/71.1%–86.7%/);
  await go('production');assert.match(await page.locator('.sim-result').innerText(),/70.00 per day/);
  await go('embeddings-ranking');await slide('position',1);assert.match(await page.locator('.sim-result').innerText(),/1.000/);
  await page.selectOption('#rating','3');await page.fill('#evidence-note','My test evidence: independent held-out queries.');
  await page.reload();await page.waitForSelector('#rating');assert.equal(await page.locator('#rating').inputValue(),'3');
  assert.match(await page.locator('#evidence-note').inputValue(),/held-out/);
  const exportPromise=page.waitForEvent('download');await page.click('#export');const exported=await exportPromise;
  const exportPath=await exported.path();
  await page.evaluate(()=>localStorage.removeItem('orbit-ai-depth-v1'));await page.reload();
  await page.setInputFiles('#import',exportPath);await page.waitForFunction(()=>document.querySelector('#rating').value==='3');
  const codePromise=page.waitForEvent('download');await page.click('#code-download');assert.equal((await codePromise).suggestedFilename(),'embeddings-ranking.py');
  await page.goto(`${base}/ai-depth/index.html?day=24`);await page.waitForSelector('#chapters a');
  assert.equal(await page.locator('#day').inputValue(),'24');assert.match(await page.locator('#lesson').innerText(),/Your Day 24/);
  assert.ok(await page.locator('#chapters a').count()<28);
  await page.selectOption('#day','');await page.selectOption('#project','MFlash');
  const filtered=await page.locator('#chapters a').allTextContents();assert.ok(filtered.length>3&&filtered.length<28);
  await page.fill('#search','zzzz-no-match');assert.equal(await page.locator('#chapters a').count(),0);
  await page.fill('#search','');await page.selectOption('#project','');
  await page.goto(`${base}/ai-depth/index.html#unknown-topic`);assert.match(await page.locator('#lesson').innerText(),/not found/);
  await page.goto(`${base}/ai-depth/index.html`);await page.screenshot({path:'/tmp/ai-depth-overview.png'});
  await go('adaptation');await page.screenshot({path:'/tmp/ai-depth-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  for(const c of chapters){await go(c.id);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`Overflow: ${c.id}`);}
  await go('adaptation');await page.screenshot({path:'/tmp/ai-depth-mobile.png'});
  await page.click('#menu');assert.equal(await page.locator('#menu').getAttribute('aria-expanded'),'true');
  await page.goto(`${base}/beginner/index.html#lesson-24`);await page.waitForSelector('.learn-depth a');
  assert.ok(await page.locator('.learn-depth a').count()>=2);
  await page.goto(`${base}/visual-map.html?lesson=24#topic-guide`);await page.waitForSelector('.learn-depth a');
  await page.goto(`${base}/index.html#day-24`);await page.waitForSelector('.learn-depth a');
  assert.ok(await page.locator('a[href="ai-depth/index.html"]').count()>0);
  const navBounds=await page.locator('.topright a[href="ai-depth/index.html"]').boundingBox();
  assert.ok(navBounds.x>=0&&navBounds.x+navBounds.width<=390,'AI navigation must fit on mobile');
  await page.screenshot({path:'/tmp/ai-dashboard-mobile.png'});
  const mappings=await page.evaluate(()=>Array.from({length:30},(_,i)=>renderLessonGuide(i+1).includes('learn-depth')));
  assert.ok(mappings.every(Boolean));
  assert.deepEqual(errors,[]);
  console.log('28 chapters, 84 answers, diagrams, six calculators, notes persistence/import/export, downloads, filters, mobile layouts, and all 30 daily integrations passed; no page errors.');
  await browser.close();
})().catch(err=>{console.error(err);process.exit(1)});
