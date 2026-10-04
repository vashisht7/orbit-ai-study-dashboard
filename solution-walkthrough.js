/* Recorded, source-aligned teaching walkthroughs. No user code is executed here. */
(() => {
  const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const text = value => JSON.stringify(value, null, 2);
  let dispose = () => {};
  function download(blob, name) {
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = name; a.click(); setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function drawSnapshot(canvas, p, example, frame, line, position, length) {
    const ctx = canvas.getContext('2d'); canvas.width=1280; canvas.height=900;
    ctx.fillStyle='#0b1222';ctx.fillRect(0,0,1280,900);
    function wrap(value,x,y,width,font='20px system-ui',color='#dce7f4',maxLines=9) {
      ctx.font=font;ctx.fillStyle=color;let count=0;
      for (const paragraph of String(value).split('\n')) {
        let current='';
        for (const word of paragraph.split(' ')) {
          const trial=current ? current+' '+word : word;
          if(ctx.measureText(trial).width>width && current){ctx.fillText(current,x,y);y+=28;current=word;if(++count>=maxLines){ctx.fillText('…',x,y);return y+28;}}
          else current=trial;
        }
        ctx.fillText(current,x,y);y+=28;if(++count>=maxLines)return y;
      }
      return y;
    }
    wrap('CODE LAB · RECORDED PYTHON WALKTHROUGH',40,45,1200,'16px system-ui','#7be0ce',1);
    wrap(p.title,40,91,1200,'bold 30px system-ui','#fff',2);
    wrap(`Step ${position+1}/${length} · ${frame.function} · ${frame.event==='return'?'Returning from':'Before executing'} line ${frame.line}`,40,161,1200,'18px system-ui','#a4b9cb',1);
    ctx.fillStyle='#173d4d';ctx.fillRect(30,186,1220,83);
    wrap(line?.code.trim() || p.solution.split('\n')[frame.line-1],45,221,1180,'19px monospace','#9cf1df',2);
    wrap(line?.note || 'Return control to the caller.',40,305,1190,'21px system-ui','#e3edf6',4);
    ctx.fillStyle='#172238';ctx.fillRect(30,425,1220,345);
    wrap('VARIABLES AT THIS STEP (large values summarized)',45,454,1180,'16px system-ui','#f2cf8b',1);
    const entries=Object.entries(frame.state);
    entries.slice(0,8).forEach(([k,v],i)=>{
      const col=i%2,row=Math.floor(i/2), value=JSON.stringify(v);
      wrap(`${k} = ${value}`,45+col*600,492+row*66,565,'17px monospace','#e2eaf7',2);
    });
    wrap(frame.event==='return' ? `Returned: ${JSON.stringify(frame.returned)}` : 'Highlighted line runs next. Variables show the state before it executes.',40,812,1190,'18px system-ui','#7be0ce',2);
    wrap(`Expected complete result: ${JSON.stringify(example.expected)}`,40,868,1190,'16px monospace','#a4b9cb',1);
  }
  window.mountSolutionWalkthrough = (p) => {
    dispose();
    const host=document.querySelector('#solution-walkthrough');
    const lesson=window.WALKTHROUGHS[p.id];
    if(!lesson){host.textContent='This walkthrough is not available.';return;}
    let exampleIndex=0, index=0, timer=null, delay=1500, cancelled=false, recorder=null;
    const pause=()=>{clearInterval(timer);timer=null;const b=host.querySelector('[data-play]');if(b)b.textContent='▶ Play walkthrough';};
    dispose=()=>{cancelled=true;pause();if(recorder?.state==='recording')recorder.stop();};
    host.innerHTML=`<div class="walk-heading"><div><p class="walk-kicker">WATCH THE CODE WORK</p><h3>A guided execution, one line at a time</h3></div><span class="walk-badge">${lesson.lines.length} explained lines</span></div>
      <p class="walk-intro">Start with the input. Predict what changes, then press Next. The highlighted line is <b>about to run</b>; the variable cards show its current inputs. A return frame shows what the function just returned. These recordings use the reference solution, not your editor draft.</p>
      <div class="walk-controls"><label>Example <select data-example aria-label="Walkthrough example"><option value="0">1 · First test</option><option value="1">2 · Another test</option></select></label><button type="button" data-play>▶ Play walkthrough</button><button type="button" data-back>← Back</button><button type="button" data-next>Next →</button><button type="button" data-restart>↺ Restart</button><label>Speed <select data-speed aria-label="Walkthrough speed"><option value="2400">Slow</option><option value="1500" selected>Normal</option><option value="700">Fast</option></select></label></div>
      <div class="walk-contract"></div>
      <label class="walk-position"><span data-position></span><input type="range" min="0" value="0" data-seek aria-label="Execution step"></label>
      <div class="walk-grid"><div class="walk-code" aria-label="Reference source with active line">${lesson.lines.map(l=>`<div data-code-line="${l.number}"><span>${l.number}</span><code>${esc(l.code)}</code></div>`).join('')}</div>
      <div class="walk-inspector"><div class="walk-current" aria-live="polite"></div><div class="walk-state"></div></div></div>
      <p class="walk-limits">Library and comprehension internals are summarized by the line notes. Nested helper calls are shown. Large collections are shortened for readability; the tests use complete values. Async recordings show one valid scheduling order, not a guaranteed order.</p>
      <div class="walk-controls"><button type="button" data-image>Download this step as an image</button><button type="button" data-video>Download a short video</button><span data-export-status role="status"></span></div>
      <details class="walk-lines"><summary>Read every line: what it does and why</summary><p>These notes follow the exact reference code, including branches that may not run in the selected example.</p>${lesson.lines.map(l=>`<article><div class="walk-line-label">Line ${l.number}</div><pre><code>${esc(l.code)}</code></pre><p>${esc(l.note)}</p></article>`).join('')}</details>`;
    const find=s=>host.querySelector(s);
    const current=()=>lesson.examples[exampleIndex];
    function render() {
      const e=current(), f=e.frames[index], prev=e.frames[index-1];
      const line=lesson.lines.find(l=>l.number===f.line);
      find('[data-position]').textContent=`Step ${index+1} of ${e.frames.length} · ${f.function}${e.truncated?' · preview capped; tests run fully':''}`;
      find('[data-seek]').max=e.frames.length-1;find('[data-seek]').value=index;
      find('[data-back]').disabled=index===0;find('[data-next]').disabled=index===e.frames.length-1;
      find('.walk-contract').innerHTML=`<div><b>Example input</b><pre>${esc(text(e.input))}</pre></div><div><b>Expected full result</b><pre>${esc(text(e.expected))}</pre></div>`;
      host.querySelectorAll('[data-code-line]').forEach(el=>el.classList.toggle('active',Number(el.dataset.codeLine)===f.line));
      const active=host.querySelector(`[data-code-line="${f.line}"]`), box=find('.walk-code');
      if(active)box.scrollTop=Math.max(0,active.offsetTop-box.offsetTop-box.clientHeight/3);
      find('.walk-current').innerHTML=`<span class="walk-kicker">${f.event==='return'?'FUNCTION RETURN':'ABOUT TO EXECUTE'} · LINE ${f.line}</span><p>${esc(line?.note || 'Return control to the caller.')}</p>${f.event==='return'?`<p><b>Returned:</b> <code>${esc(JSON.stringify(f.returned))}</code></p>`:''}`;
      find('.walk-state').innerHTML=Object.entries(f.state).map(([key,value])=>{
        const changed=prev && (prev.function!==f.function || JSON.stringify(prev.state[key])!==JSON.stringify(value));
        let display;
        if(Array.isArray(value)&&value.every(v=>!v||typeof v!=='object'))display=`<div class="walk-array">${value.map((v,i)=>`<span><small>${i}</small>${esc(JSON.stringify(v))}</span>`).join('')||'<em>empty list</em>'}</div>`;
        else display=`<pre>${esc(text(value))}</pre>`;
        return `<div class="walk-variable ${changed?'changed':''}"><b>${esc(key)}</b>${changed?'<small> changed / new frame</small>':''}${display}</div>`;
      }).join('')||'<p class="quiet">No local variables in this frame yet.</p>';
    }
    function start(){pause();if(index===current().frames.length-1)index=0;find('[data-play]').textContent='❚❚ Pause';render();timer=setInterval(()=>{if(index>=current().frames.length-1){pause();return;}index++;render();},delay);}
    find('[data-play]').onclick=()=>timer?pause():start();
    find('[data-next]').onclick=()=>{pause();index=Math.min(index+1,current().frames.length-1);render();};
    find('[data-back]').onclick=()=>{pause();index=Math.max(0,index-1);render();};
    find('[data-restart]').onclick=()=>{pause();index=0;render();};
    find('[data-seek]').oninput=e=>{pause();index=Number(e.target.value);render();};
    find('[data-example]').onchange=e=>{pause();exampleIndex=Number(e.target.value);index=0;render();};
    find('[data-speed]').onchange=e=>{delay=Number(e.target.value);if(timer)start();};
    find('[data-image]').onclick=()=>{pause();const canvas=document.createElement('canvas'),e=current(),f=e.frames[index];drawSnapshot(canvas,p,e,f,lesson.lines.find(l=>l.number===f.line),index,e.frames.length);canvas.toBlob(blob=>download(blob,`${p.id}-step-${index+1}.png`),'image/png');};
    find('[data-video]').onclick=async()=>{
      pause();const button=find('[data-video]'),status=find('[data-export-status]');
      const canvas=document.createElement('canvas');
      if(!canvas.captureStream||!window.MediaRecorder){status.textContent='Video export is unavailable in this browser. Use Play or download an image.';return;}
      const e=current(),count=Math.min(12,e.frames.length),indices=Array.from({length:count},(_,i)=>Math.round(i*(e.frames.length-1)/Math.max(1,count-1)));
      button.disabled=true;status.textContent=`Recording ${count} one-second checkpoints. Intermediate steps remain available in the interactive walkthrough.`;
      let stream;
      try{
        drawSnapshot(canvas,p,e,e.frames[0],lesson.lines.find(l=>l.number===e.frames[0].line),0,e.frames.length);
        stream=canvas.captureStream(10);
        const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(m=>MediaRecorder.isTypeSupported(m));
        if(!mime)throw Error('WebM recording is not supported here.');
        const chunks=[];recorder=new MediaRecorder(stream,{mimeType:mime});
        recorder.ondataavailable=event=>{if(event.data.size)chunks.push(event.data);};
        const stopped=new Promise(resolve=>recorder.onstop=resolve);
        recorder.start();
        for(const n of indices){if(cancelled)break;const f=e.frames[n];drawSnapshot(canvas,p,e,f,lesson.lines.find(l=>l.number===f.line),n,e.frames.length);await new Promise(resolve=>setTimeout(resolve,1000));}
        if(recorder.state==='recording')recorder.stop();await stopped;
        if(!cancelled){download(new Blob(chunks,{type:'video/webm'}),`${p.id}-walkthrough.webm`);status.textContent='Video downloaded: silent checkpoint summary. Use Next for every execution step.';}
      }catch(error){if(!cancelled)status.textContent=`Could not export video: ${error.message} You can still play the walkthrough or save an image.`;}
      finally{stream?.getTracks().forEach(t=>t.stop());if(!cancelled)button.disabled=false;}
    };
    if(!window.MediaRecorder)find('[data-video]').title='Requires a browser with video recording support; animated playback works without it.';
    render();
  };
  window.pauseSolutionWalkthrough=()=>{dispose();};
})();
