const { chromium }=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8765/');await page.waitForSelector('.study-stage');
assert.equal(await page.locator('[data-study-step][aria-pressed=true]').getAttribute('data-study-step'),'2');
let p=await page.evaluate(()=>DAILY_STUDY.progress());for(let d=1;d<=5;d++){assert.equal(p.days[d].checks.design,false);assert.equal(p.days[d].checks.coding,true);}
await page.locator('#study-note').fill('Design catchup note');await page.locator('#study-complete').click();await page.reload();await page.waitForSelector('.study-stage');p=await page.evaluate(()=>DAILY_STUDY.progress());assert.equal(p.days[1].checks.design,true);assert.equal(p.days[1].unifiedNotes.design,'Design catchup note');
for(let d=1;d<=30;d++){
 await page.goto('http://127.0.0.1:8765/ai-depth/index.html#day-'+d);await page.waitForSelector('.study-stage');
 for(let i=0;i<4;i++){await page.locator('[data-study-step="'+i+'"]').click();assert.ok((await page.locator('.study-stage').innerText()).length>300);if(i===1)assert.ok(await page.locator('.study-stage a.button').getAttribute('href'));}
}
await page.locator('#walk-play').click();assert.match(await page.locator('#walk-play').innerText(),/Pause/);await page.locator('#walk-next').click();assert.equal(await page.locator('#walk-position').innerText(),'2 / 4');
const downloadPromise=page.waitForEvent('download');await page.locator('#study-export').click();const download=await downloadPromise;const path=await download.path();const backup=JSON.parse(require('fs').readFileSync(path,'utf8'));assert.ok(backup.progress.days[1].checks.design);await page.locator('#study-import').setInputFiles(path);await page.waitForTimeout(300);assert.equal(await page.evaluate(()=>DAILY_STUDY.progress().days[1].checks.design),true);
await page.setViewportSize({width:390,height:844});await page.goto('http://127.0.0.1:8765/ai-depth/index.html#day-6');await page.waitForSelector('.study-stage');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(11, 16, 32)');await page.screenshot({path:'/tmp/orbit-unified-mobile.png',fullPage:true});
await page.setViewportSize({width:1440,height:1000});await page.goto('http://127.0.0.1:8765/ai-depth/index.html#day-1');await page.screenshot({path:'/tmp/orbit-unified-desktop.png'});assert.deepEqual(errors,[]);await browser.close();console.log('PASS: 30 days / 120 steps, checkpoint, persistence, walkthrough, backup, dark mode, mobile');
})().catch(e=>{console.error(e);process.exit(1)});
