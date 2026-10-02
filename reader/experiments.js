import * as THREE from './vendor/three.module.js';
const definitions={
 gradient:{title:'Move a parameter along a loss curve',label:'Learning rate',min:0,max:1.2,step:.02,start:.2,tip:'Predict whether one update moves toward or beyond the minimum. Horizontal position is w; vertical height shows L = (w − 2)², scaled by one half to fit the view.',predict:'Starting at w = 0, what happens when the learning rate is 1?',answer:'The gradient is −4. The update reaches w = 4, where loss is still 4. A larger rate makes loss worse.'},
 attention:{title:'Attention is a moving weighted mixture',label:'Second key score',min:-4,max:4,step:.1,start:1,tip:'Blue and gold are two value vectors. Teal is their softmax-weighted mixture. The first key score stays at zero.',predict:'Can the mixture move beyond both value endpoints?',answer:'Within this one attention mixture, nonnegative weights sum to one, so it stays on the segment. Later projections and residual operations are not restricted to that segment.'},
 rotation:{title:'Position changes a vector’s direction',label:'Relative rotation (degrees)',min:0,max:360,step:1,start:60,tip:'The gold unit vector rotates. The blue vector stays on the first axis. Watch their dot product while both lengths remain one.',predict:'What is the dot product at 90 degrees?',answer:'Zero, up to floating-point rounding. Orthogonal unit vectors have zero dot product.'},
 geometry:{title:'Direction and magnitude are different signals',label:'Document-vector magnitude',min:.2,max:5,step:.1,start:1,tip:'The query is (1, 0). The document points 45 degrees upward; its magnitude changes. Cosine ignores this magnitude while dot product does not.',predict:'If the vector length doubles, what happens to cosine and dot product?',answer:'Cosine remains about 0.707; dot product doubles. This is why normalization changes the meaning of a retrieval score.'},
 lora:{title:'A rank-one update has one output direction',label:'Input second coordinate',min:-2,max:2,step:.1,start:1,tip:'Here A = [1, 2], B = [1, 0.5]ᵀ and x = [1, s]ᵀ. Every update B(Ax) lies on the same line. The frozen base is omitted so the update is visible.',predict:'Which slider setting makes the update zero?',answer:'s = −0.5 makes Ax = 1 + 2s = 0, so B(Ax) is zero even though neither factor is zero.'},
 cache:{title:'Watch KV memory grow with context',label:'Stored tokens',min:1024,max:32768,step:1024,start:4096,tip:'Fixed example: 32 layers, 8 KV heads, head width 128, 2 bytes per value, one sequence. This bar shows KV storage only.',predict:'If both tokens and batch size double, how does KV memory change?',answer:'It becomes four times larger under the same uncompressed-cache assumptions. Weights and workspace are additional memory.'},
 fusion:{title:'Two rankings vote through reciprocal rank',label:'Document A dense rank',min:1,max:10,step:1,start:3,tip:'A is lexical rank 1. B is rank 2 in both searches. The fusion constant is 60. Bar height is the fused score, scaled for visibility.',predict:'At dense rank 3, is A decisively better than B?',answer:'No. A scores about 0.032266 and B about 0.032258. The difference is tiny and is not calibrated relevance confidence.'},
 state:{title:'Follow a durable operation through its states',label:'Workflow step',min:0,max:4,step:1,start:0,tip:'This animation explains a state machine; it does not execute a real action. Succeeded appears only after an observed committed effect.',predict:'Does a model-generated “done” message move the workflow to succeeded?',answer:'No. Trusted execution and an observed result control that transition. The model’s text is a proposal or explanation, not the ledger.'}
};
export function quantities(kind,value){
 if(kind==='gradient'){let w=4*value;return {w,loss:(w-2)**2};}
 if(kind==='attention'){let weight=1/(1+Math.exp(-value));return {weight,x:2*(1-weight),y:4*weight};}
 if(kind==='rotation'){let r=value*Math.PI/180;return {x:Math.cos(r),y:Math.sin(r),dot:Math.cos(r),norm:1};}
 if(kind==='geometry')return {x:value/Math.sqrt(2),y:value/Math.sqrt(2),cosine:1/Math.sqrt(2),dot:value/Math.sqrt(2)};
 if(kind==='lora')return {projection:1+2*value,x:1+2*value,y:(1+2*value)/2};
 if(kind==='cache')return {bytes:2*32*value*8*128*2,gib:2*32*value*8*128*2/(1024**3)};
 if(kind==='fusion')return {a:1/61+1/(60+value),b:2/62};
 return {state:['Proposed','Validated','Executing','Effect observed','Succeeded'][value]};
}
export function mountExperiment(root,kind){
 const d=definitions[kind];
 root.innerHTML=`<section class="lab-panel"><div class="eyebrow">INTERACTIVE LAB · THREE.JS</div><h2>${d.title}</h2><p>${d.tip}</p><div class="scene" role="img" aria-label="Interactive ${kind} visualization"></div><div class="controls"><label>${d.label}<input aria-label="${d.label}" type="range" min="${d.min}" max="${d.max}" step="${d.step}" value="${d.start}"></label><button class="play">Play transition</button><button class="reset">Reset</button></div><p class="readout" aria-live="polite"></p><details class="answer"><summary>Predict first: ${d.predict}</summary><p>${d.answer}</p></details></section>`;
 const holder=root.querySelector('.scene'), slider=root.querySelector('input'),readout=root.querySelector('.readout');
 let renderer,scene,camera,group,raf=0,disposed=false,startTime=0;
 const color={teal:0x77d7c9,blue:0x77a6ff,gold:0xffc579};
 function clear(){if(!group)return;while(group.children.length){let o=group.children[0];group.remove(o);o.traverse(x=>{x.geometry?.dispose();if(Array.isArray(x.material))x.material.forEach(m=>m.dispose());else x.material?.dispose();});}}
 function line(points,c){const geo=new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p)));group.add(new THREE.Line(geo,new THREE.LineBasicMaterial({color:c})));}
 function dot(x,y,c,size=.12){let o=new THREE.Mesh(new THREE.SphereGeometry(size,18,12),new THREE.MeshBasicMaterial({color:c}));o.position.set(x,y,0);group.add(o);}
 function vector(x,y,c){line([[0,0,0],[x,y,0]],c);dot(x,y,c);}
 function bar(x,height,c,width=.6){let o=new THREE.Mesh(new THREE.BoxGeometry(width,Math.max(.01,height),.4),new THREE.MeshStandardMaterial({color:c,roughness:.5}));o.position.set(x,height/2,0);group.add(o);}
 try{
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x102737);holder.append(renderer.domElement);
  scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(40,1,.1,100);camera.position.set(1.5,2,12);camera.lookAt(1,1,0);group=new THREE.Group();scene.add(group);scene.add(new THREE.AmbientLight(0xffffff,2));let light=new THREE.DirectionalLight(0xffffff,3);light.position.set(4,8,5);scene.add(light);
 }catch{holder.innerHTML='<p class="fallback">3D graphics are unavailable in this browser. The controls and exact numerical explanation below still work.</p>';}
 function draw(){
  const v=+slider.value,q=quantities(kind,v);
  const texts={gradient:()=>`η = ${v.toFixed(2)} · start w = 0, loss = 4 · updated w = ${q.w.toFixed(2)}, loss = ${q.loss.toFixed(3)}`,
   attention:()=>`Second weight = ${q.weight.toFixed(3)} · first weight = ${(1-q.weight).toFixed(3)} · mixture = (${q.x.toFixed(3)}, ${q.y.toFixed(3)})`,
   rotation:()=>`Angle = ${v}° · vector = (${q.x.toFixed(3)}, ${q.y.toFixed(3)}) · dot = ${q.dot.toFixed(3)} · norm = 1`,
   geometry:()=>`Magnitude = ${v.toFixed(1)} · cosine = ${q.cosine.toFixed(3)} · dot = ${q.dot.toFixed(3)}`,
   lora:()=>`s = ${v.toFixed(1)} · Ax = ${q.projection.toFixed(2)} · update = (${q.x.toFixed(2)}, ${q.y.toFixed(2)})`,
   cache:()=>`${v.toLocaleString()} tokens · ${q.bytes.toLocaleString()} bytes · ${q.gib.toFixed(3)} GiB KV cache`,
   fusion:()=>`A = ${q.a.toFixed(6)} · B = ${q.b.toFixed(6)} · leading document: ${q.a>q.b?'A':'B'}`,
   state:()=>`Step ${v}: ${q.state}. ${v<3?'No confirmed effect yet.':v===3?'The committed effect has been observed.':'Success is recorded against the operation ID.'}`};
  readout.textContent=texts[kind]();root.dataset.value=String(v);root.dataset.kind=kind;
  if(!renderer)return;clear();line([[-5,0,0],[6,0,0]],0x49616f);line([[0,-3,0],[0,5,0]],0x49616f);
  if(kind==='gradient'){let points=[];for(let w=-.3;w<4.8;w+=.05)points.push([w,(w-2)**2/2,0]);line(points,color.blue);dot(0,2,color.gold);dot(q.w,q.loss/2,color.teal);line([[0,2,0],[q.w,q.loss/2,0]],color.teal);}
  if(kind==='attention'){vector(2,0,color.blue);vector(0,4,color.gold);line([[2,0,0],[0,4,0]],0x49616f);vector(q.x,q.y,color.teal);}
  if(kind==='rotation'||kind==='geometry'){vector(1,0,color.blue);vector(q.x,q.y,color.gold);if(kind==='rotation'){let points=[];for(let i=0;i<=100;i++)points.push([Math.cos(i*Math.PI/50),Math.sin(i*Math.PI/50),0]);line(points,0x49616f);}}
  if(kind==='lora'){line([[-4,-2,0],[5,2.5,0]],color.blue);vector(q.x,q.y,color.teal);}
  if(kind==='cache')bar(1,q.gib,color.teal,1.5);
  if(kind==='fusion'){bar(0,q.a*100,color.blue);bar(2,q.b*100,color.gold);}
  if(kind==='state'){for(let i=0;i<5;i++){let x=-3+i*1.8;dot(x,1,i<=v?color.teal:0x49616f,.22);if(i<4)line([[x,1,0],[x+1.8,1,0]],i<v?color.teal:0x49616f);}}
  renderer.render(scene,camera);
 }
 function size(){if(renderer){renderer.setSize(holder.clientWidth,holder.clientHeight);camera.aspect=holder.clientWidth/holder.clientHeight;camera.updateProjectionMatrix();}draw();}
 const observer=new ResizeObserver(size);observer.observe(holder);
 function stop(){cancelAnimationFrame(raf);raf=0;root.querySelector('.play').textContent='Play transition';}
 slider.oninput=()=>{stop();draw();};
 root.querySelector('.reset').onclick=()=>{stop();slider.value=d.start;draw();};
 root.querySelector('.play').onclick=()=>{
  if(raf){stop();return;}
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){slider.value=d.max;draw();return;}
  startTime=performance.now();root.querySelector('.play').textContent='Pause';
  function tick(t){if(disposed)return;const f=Math.min(1,(t-startTime)/4500);slider.value=d.min+Math.round(f*(d.max-d.min)/d.step)*d.step;draw();if(f<1)raf=requestAnimationFrame(tick);else stop();}
  raf=requestAnimationFrame(tick);
 };
 size();return()=>{disposed=true;stop();observer.disconnect();clear();renderer?.dispose();};
}
