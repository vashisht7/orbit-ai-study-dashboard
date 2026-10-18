// Print the same local Markdown + KaTeX lesson content used by both readers.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try {
  const page=await browser.newPage();
  await page.goto((process.env.BASE_URL||'http://127.0.0.1:8765')+'/beginner/index.html');
  await page.waitForFunction(()=>window.BEGINNER&&window.renderBeginner);
  await page.evaluate(()=>{
   document.querySelectorAll('link[rel=stylesheet],style').forEach(el=>el.remove());
   const css=document.createElement('link');css.rel='stylesheet';css.href='../reader/vendor/katex.min.css';document.head.append(css);
   const style=document.createElement('style');
   style.textContent=`
    @page {size: A4; margin: 18mm 17mm 20mm;}
    html {color-scheme:light;background:white!important;}
    body {margin:0;background:white!important;color:#1e293b!important;font:11pt/1.5 Arial,sans-serif!important;}
    body>header,.skip {display:none!important;}
    .print-cover {break-after:page;padding-top:45mm;}
    .print-cover h1 {font-size:34pt;line-height:1.15;color:#123a5a;}
    .print-cover p {max-width:145mm;font-size:13pt;}
    .toc {break-after:page;} .toc li {font-size:9.4pt;line-height:1.35;margin-bottom:1mm;}
    article {padding:0!important;max-width:none!important;}
    .print-lesson {break-before:page;}
    h1 {font-size:23pt;line-height:1.2;color:#123a5a;break-after:avoid;}
    h3 {font-size:13pt;line-height:1.3;margin:7mm 0 2mm;break-after:avoid;color:#123a5a;}
    p {margin:0 0 3mm;orphans:3;widows:3;}
    ul,ol {padding-left:6mm;} li {margin-bottom:1.5mm;}
    a {color:#17658a;text-decoration:none;overflow-wrap:anywhere;}
    pre {white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f9!important;color:#1e293b!important;border:1px solid #dbe3ec;padding:3mm;font-size:8pt;line-height:1.4;break-inside:auto;}
    code {font-size:0.92em;background:#f1f5f9!important;color:#1e293b!important;}
    pre code {font-size:inherit;}
    .equation {background:white!important;border:0!important;padding:1mm!important;overflow:visible!important;break-inside:avoid;font-size:10pt;}
    .katex-display {margin:2mm 0;}
    p:has(+ .equation) {break-after:avoid;}
    .print-lesson pre {break-inside:avoid;}
    .print-lesson pre.long-code {break-inside:auto;}
    table {width:100%;border-collapse:collapse;} th,td {padding:2mm;border:1px solid #cbd5e1;}
   `;document.head.append(style);
   document.body.innerHTML=`<section class="print-cover"><p>START SMALL · UNDERSTAND THE MECHANISM</p><h1>AI Engineering<br>From First Principles</h1><p>30 lessons · read at your own pace</p><p>Concept → rule and derivation → worked example → practice → explain it.</p><p>Revised October 18, 2026</p><p>Read at your own pace. Each lesson defines its symbols and separates the general rule from the numbers used to illustrate it.</p></section><section class="toc"><h1>Your learning route</h1><ol>${BEGINNER.map(c=>`<li>${c.title}</li>`).join('')}</ol></section>${BEGINNER.map(c=>`<article class="print-lesson"><h1>${Number(c.id)}. ${c.title}</h1>${renderBeginner(c.body)}</article>`).join('')}`;
  });
  await page.evaluate(()=>document.querySelectorAll('pre').forEach(el=>{if(el.innerText.split('\n').length>40)el.classList.add('long-code');}));
  await page.evaluate(()=>document.fonts.ready);
  await page.waitForFunction(()=>[...document.styleSheets].some(s=>s.href&&s.href.includes('katex.min.css')));
  const failures=await page.locator('.katex-error').count();if(failures)throw Error(`${failures} invalid equations`);
  const folder=path.join(root,'output/pdf');fs.mkdirSync(folder,{recursive:true});
  const target=path.join(folder,'AI_Engineering_First_Principles.pdf');
  await page.pdf({path:target,printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font:8px Arial;color:#64748b;width:100%;text-align:center">AI Engineering · First Principles &nbsp; | &nbsp; <span class="pageNumber"></span> / <span class="totalPages"></span></div>',preferCSSPageSize:true});
  fs.copyFileSync(target,path.join(root,'beginner/Beginner_AI_Engineering.pdf'));
  console.log('Exported updated course PDF and refreshed the existing reader download.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
