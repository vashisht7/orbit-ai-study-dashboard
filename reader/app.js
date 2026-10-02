import { mountExperiment } from './experiments.js';
const {chapters, references} = window.COURSE;
const article=document.querySelector('#lesson');
let cleanup=()=>{}, completed=new Set();
try {completed=new Set(JSON.parse(localStorage.getItem('llm-workshop-completed')||'[]'));}catch{}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function renderBody(body){
 const blocks=[];
 body=body.replace(/^```[^\n]*\n[\s\S]*?^```/gm,m=>{blocks.push(marked.parse(m));return `\n\nLLMBLOCK${blocks.length-1}END\n\n`;});
 body=body.replace(/^\$\$ (.+) \$\$$/gm,(_,m)=>{blocks.push('<div class="equation">'+katex.renderToString(m,{displayMode:true,throwOnError:true,strict:'ignore'})+'</div>');return `\n\nLLMBLOCK${blocks.length-1}END\n\n`;});
 body=body.replace(/\$([^$\n]+)\$/g,(_,m)=>katex.renderToString(m,{throwOnError:true,strict:'ignore',trust:false}));
 body=body.replace(/^@visual (\w+).*$/gm,(_,kind)=>`<figure><img class="figure" src="figures/${kind}.svg" alt="${esc(kind)} mechanism diagram"><figcaption>Follow the quantities in the surrounding worked example.</figcaption></figure>`);
 body=body.replace(/^@matrix (.+) \| (.+)$/gm,(_,label,rows)=>`<figure><figcaption>${esc(label)}</figcaption><div class="table-wrap"><table aria-label="${esc(label)}"><tbody>${rows.split(';').map(r=>'<tr>'+r.split(',').map(v=>'<td>'+esc(v)+'</td>').join('')+'</tr>').join('')}</tbody></table></div></figure>`);
 body=body.replace(/^@diagram (.+)$/gm,(_,line)=>'<div class="flow-map">'+line.split(' | ').map(esc).join(' <span aria-hidden="true">→</span> ')+'</div>');
 body=body.replace(/\[(R\d+)\]/g,(m,key)=>references[key]?`[${key}](${references[key][1]})`:m);
 return marked.parse(body).replace(/<p>LLMBLOCK(\d+)END<\/p>/g,(_,i)=>blocks[+i]);
}
function current(){return chapters.find(c=>c.id===location.hash.slice(1))||chapters[0];}
function nav(){
 const query=document.querySelector('#search').value.toLowerCase().trim();let part='';
 document.querySelector('#chapters').innerHTML=chapters.map((c,i)=>{
   if(query&&!(`${c.title} ${c.body}`.toLowerCase().includes(query)))return '';
   const heading=c.part!==part?`<div class="part-label">${esc(c.part)}</div>`:'';part=c.part;
   return heading+`<a href="#${c.id}" ${c.id===current().id?'class="active" aria-current="page"':''}>${completed.has(c.id)?'✓ ':''}${i+1}. ${esc(c.title)}</a>`;
 }).join('')||'<p>No matching concepts. Try a shorter term.</p>';
 document.querySelector('#progress').textContent=`${chapters.filter(c=>completed.has(c.id)).length} of ${chapters.length} chapters marked studied`;
}
function show(){
 cleanup();const c=current(),i=chapters.indexOf(c);document.title=c.title+' · Modern LLM Workshop';
 article.innerHTML=`<div class="eyebrow">${esc(c.part)} · CHAPTER ${i+1}</div><h1>${esc(c.title)}</h1><div class="lesson-tools"><button id="mark">${completed.has(c.id)?'Studied ✓ · Mark unread':'Mark as studied'}</button><span>${Math.max(1,Math.ceil(c.body.split(/\s+/).length/180))} min reading · take longer for labs</span></div>${c.expanded?'<p class="edition-note">Expanded reading edition · includes a deeper worked explanation and practice exercise. <a class="deep-jump" href="#deeper-study">Jump to the new explanation ↓</a></p>':''}<div id="experiment"></div><div class="prose">${renderBody(c.body)}</div><div class="reflection"><h2>Close the loop</h2><p>Without looking above: explain the problem, the computation, its key assumption, and one failure test. Then run or modify the corresponding lab.</p></div><div class="lesson-nav">${i?`<a href="#${chapters[i-1].id}">← ${esc(chapters[i-1].title)}</a>`:'<span></span>'}${i<chapters.length-1?`<a href="#${chapters[i+1].id}">${esc(chapters[i+1].title)} →</a>`:''}</div>`;
 cleanup=c.experiment?mountExperiment(document.querySelector('#experiment'),c.experiment):()=>{};
 document.querySelector('#mark').onclick=()=>{completed.has(c.id)?completed.delete(c.id):completed.add(c.id);try{localStorage.setItem('llm-workshop-completed',JSON.stringify([...completed]));}catch{}document.querySelector('#mark').textContent=completed.has(c.id)?'Studied ✓ · Mark unread':'Mark as studied';nav();};
 const deepHeading=[...article.querySelectorAll('h2')].find(h=>h.textContent.startsWith('Deeper understanding'));if(deepHeading)deepHeading.id='deeper-study';
 article.querySelectorAll('h3').forEach((h,j)=>h.id='section-'+j);
 article.querySelectorAll('.prose table').forEach(t=>{if(!t.parentElement.classList.contains('table-wrap')){let w=document.createElement('div');w.className='table-wrap';t.replaceWith(w);w.append(t);}});
 nav();document.querySelector('#sidebar').classList.remove('open');document.querySelector('#menu').setAttribute('aria-expanded','false');window.scrollTo(0,0);
}
document.querySelector('#search').addEventListener('input',nav);
document.querySelector('#menu').onclick=()=>{const on=document.querySelector('#sidebar').classList.toggle('open');document.querySelector('#menu').setAttribute('aria-expanded',String(on));};
document.addEventListener('click',e=>{const link=e.target.closest('a[href="#deeper-study"]');if(link){e.preventDefault();document.getElementById('deeper-study')?.scrollIntoView({behavior:'auto',block:'start'});}});
window.addEventListener('hashchange',show);show();
window.WORKSHOP={current:()=>({id:current().id,title:current().title,studied:completed.has(current().id)}),navigate:id=>{if(!chapters.some(c=>c.id===id))throw new Error('Unknown chapter ID');location.hash=id;}};
if(document.modelContext?.registerTool){
 const lifecycle=new AbortController();
 for(const tool of [{name:'read_current_lesson',description:'Read the visible lesson title and study status.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:()=>window.WORKSHOP.current()},
 {name:'navigate_to_lesson',description:'Open an existing textbook chapter by ID without marking it studied.',inputSchema:{type:'object',properties:{id:{type:'string'}},required:['id'],additionalProperties:false},annotations:{readOnlyHint:false},execute:async input=>{if(!input||typeof input.id!=='string'||Object.keys(input).length!==1||!chapters.some(c=>c.id===input.id))throw new Error('Provide a valid chapter ID only.');history.replaceState(null,'','#'+input.id);show();return window.WORKSHOP.current();}}]){
  try{Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}
 }
 window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}
