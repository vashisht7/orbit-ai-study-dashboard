const assert=require('node:assert/strict');
const {math:m}=require('../learning/mechanisms.js');
const close=(a,b,t=1e-8)=>assert.ok(Math.abs(a-b)<t,`${a} != ${b}`);
const model=m.forward(true);
for(const head of model.heads)for(let i=0;i<4;i++){
 close(head.weights[i].reduce((a,b)=>a+b,0),1);
 for(let j=i+1;j<4;j++)assert.equal(head.weights[i][j],0);
 for(let d=0;d<2;d++)close(head.mixed[i][d],head.weights[i].reduce((s,w,j)=>s+w*head.v[j][d],0));
}
assert.ok(m.forward(false).heads[0].weights[0][3]>0);
assert.equal(model.afterFFN.length,4);
assert.equal(model.ffn[0].h.length,8);
for(let i=0;i<4;i++)for(let j=0;j<4;j++)close(model.afterFFN[i][j],model.afterAttention[i][j]+model.ffn[i].out[j]);
close(m.gelu(0),0);assert.ok(m.gelu(-1)<0);
let weights=Array.from({length:4},()=>Array(4).fill(0));
const counts=[[0,0,8,0],[0,0,2,0],[0,0,0,10],[9,1,0,0]],initial=m.trainStep(weights,counts,1);
close(initial.loss,Math.log(4));
for(let i=0;i<4;i++)for(let j=0;j<4;j++){
 const plus=weights.map(r=>r.slice()),minus=weights.map(r=>r.slice()),eps=1e-5;
 plus[i][j]+=eps;minus[i][j]-=eps;
 close((m.trainStep(plus,counts,0).loss-m.trainStep(minus,counts,0).loss)/(2*eps),initial.gradient[i][j],1e-6);
}
for(let i=0;i<50;i++)weights=m.trainStep(weights,counts,1).weights;
const trained=m.trainStep(weights,counts,1);assert.ok(trained.loss<initial.loss*.5);assert.ok(trained.probs[2][3]>.8);
console.log('PASS: masked attention, head mixtures, FFN residual arithmetic, GELU, finite-difference gradients, real learning.');
