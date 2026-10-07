const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://127.0.0.1:8765';
(async()=>{
 const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const p=await b.newPage({viewport:{width:1440,height:1000}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'/index.html#day-5');await p.waitForSelector('#reading h3');
 const before=await p.evaluate(()=>{const s=JSON.parse(localStorage.getItem('orbit-ai-progress-v1'));s.days[5]={checks:{reading:true,coding:true,design:false,lab:true,recall:false,localai:true},notes:'My Day 5 original notes',quizDone:true,unifiedNotes:{learn:'Recent AI note',coding:'Recent coding note'}};s.days[9]={checks:{coding:true},notes:'Later work'};localStorage.setItem('orbit-ai-progress-v1',JSON.stringify(s));return s;});
 await p.reload();await p.waitForSelector('#reading h3');
 assert.equal(await p.locator('#notes').inputValue(),before.days[5].notes);
 await p.locator('#saved-step-notes summary').click();
 assert.match(await p.locator('#saved-step-notes').innerText(),/Recent AI note/);
 assert.equal(await p.locator('.task input[type=checkbox]:checked').count(),4);
 assert.equal(await p.locator('[data-key="design"]').isChecked(),false);
 let minimum=Infinity;
 for(let d=1;d<=30;d++){
   await p.locator(`#level-map [data-day="${d}"]`).click();
   await p.waitForFunction(n=>document.title.startsWith('Level '+n+' ·'),d);
   const length=await p.locator('#reading').innerText();minimum=Math.min(minimum,length.split(/\s+/).length);
   assert.ok(length.length>1200,'Full lesson '+d);
   assert.equal(await p.locator('.task input[type=checkbox]').count(),6);
   assert.equal(await p.locator('.resume-defense-card').count(),0);
 }
 await p.goto(base+'/index.html#day-5');await p.waitForSelector('#reading h3');
 const after=await p.evaluate(()=>JSON.parse(localStorage.getItem('orbit-ai-progress-v1')));
 for(const d of [1,2,3,4,5,9])assert.deepEqual(after.days[d],before.days[d]);
 await p.locator('[data-key="design"]').check();await p.reload();await p.waitForSelector('#reading h3');assert.equal(await p.locator('[data-key="design"]').isChecked(),true);assert.equal(await p.locator('[data-key="recall"]').isChecked(),false);
 await p.locator('a.nav-pill[href="ai-depth/index.html#overview"]').click();await p.waitForSelector('.resume-path');
 assert.equal(await p.locator('.resume-path>details').count(),6);
 const chapters=await p.evaluate(()=>AI_DEPTH.chapters.map(x=>x.id));
 for(const id of chapters){await p.goto(base+'/ai-depth/index.html#'+id);await p.waitForSelector('.flow');assert.equal(await p.locator('.interview').count(),3);}
 await p.goto(base+'/ai-depth/index.html#day-5/design');await p.waitForSelector('#reading h3');assert.match(p.url(),/index.html#day-5$/);
 for(const width of [390,1440]){await p.setViewportSize({width,height:1000});await p.screenshot({path:`/tmp/orbit-restored-${width}.png`});}
 assert.deepEqual(errors,[]);await b.close();console.log(`PASS: original 30 full lessons (minimum ${minimum} rendered words), 6 manual activities, saved progress/notes preserved, 28 separate reference chapters and legacy links.`);
})().catch(e=>{console.error(e);process.exit(1)});
