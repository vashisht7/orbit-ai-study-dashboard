/* A calculated, captioned walkthrough. No model downloads or external services. */
(() => {
  const states = new WeakMap();
  const labels = ['Choose examples','Forward pass','Measure loss','Backward pass','Combine the batch','Update the weight','Predict again','Count steps and epochs'];
  const fmt = n => Number(n.toFixed(4)).toString();
  function values(batch, rate) {
    const rows = (batch === 1 ? [[2,6]] : [[1,3],[2,6]]).map(([x,y]) => ({x,y,p:x,e:x-y,l:(x-y)**2,g:2*(x-y)*x}));
    const loss = rows.reduce((s,r)=>s+r.l,0)/rows.length;
    const gradient = rows.reduce((s,r)=>s+r.g,0)/rows.length;
    const weight = 1-rate*gradient;
    const nextLoss = rows.reduce((s,r)=>s+(r.x*weight-r.y)**2,0)/rows.length;
    return {rows,loss,gradient,weight,nextLoss};
  }
  window.trainingStoryValues = values;
  window.renderTrainingStory = day => [6,7,8].includes(Number(day)) ? `
    <section class="training-story" aria-label="See one training update" data-training-story>
      <p class="eyebrow">SEE ONE TRAINING UPDATE · START HERE IF THE WORDS ARE NEW</p>
      <h2>Prediction first. Learning comes afterward.</h2>
      <p>Imagine example cards on a workbench and one adjustable dial, the weight. Follow what is calculated and when that dial actually changes. This is a captioned animation of a tiny numerical model.</p>
      <div class="training-story-settings">
        <label>Examples in this batch <select data-story-batch><option value="1">1 example · Lesson 6</option><option value="2">2 examples · Lesson 7</option></select></label>
        <label>Learning rate <select data-story-rate><option value="0.1">0.1 · gentle update</option><option value="0.01">0.01 · smaller update</option><option value="0.3">0.3 · larger update</option></select></label>
      </div>
      <div class="training-story-controls" aria-label="Walkthrough playback">
        <button type="button" data-story-action="play">Play walkthrough</button>
        <button type="button" data-story-action="back">← Previous</button>
        <button type="button" data-story-action="next">Next step →</button>
        <button type="button" data-story-action="reset">Restart</button>
      </div>
      <p class="training-story-help">Next advances one scene. Play advances every 7 seconds; pause whenever you need. Changing a setting restarts this one-update demonstration.</p>
      <ol class="training-story-stages">${labels.map((l,i)=>`<li><button type="button" data-story-stage="${i}">${i+1}. ${l}</button></li>`).join('')}</ol>
      <div data-story-scene aria-live="polite" aria-atomic="true"></div>
      <details class="training-story-check"><summary>Check yourself: does backward change the weight?</summary><p>No. Backward computes gradients. The optimizer update changes the weight. During ordinary inference, we use the trained weights for forward prediction without a training backward pass.</p></details>
    </section>` : '';
  function render(root) {
    const s=states.get(root),v=values(s.batch,s.rate),i=s.stage;
    const cards=v.rows.map((r,n)=>`<div class="training-example"><strong>Card ${n+1}</strong><span>Input x = ${r.x}</span><span>Target y = ${r.y} · fixed</span></div>`).join('');
    const prediction=v.rows.map(r=>`${r.x} × ${i>=6?fmt(v.weight):'1'} = ${fmt(r.x*(i>=6?v.weight:1))}`).join('<br>');
    const losses=v.rows.map(r=>`(${r.p} − ${r.y})² = ${r.l}`).join('<br>');
    const gradients=v.rows.map(r=>`2 × (${r.p} − ${r.y}) × ${r.x} = ${r.g}`).join('<br>');
    const captions=[
      ['Choose the cards we will learn from','The dataset is the whole collection; a batch is the group used for this calculation. Both cards, when selected, share the same adjustable weight. The target stays outside the prediction calculation and is used to score it.','Model rule: prediction = input × weight. Start with weight w = 1.'],
      ['Forward: what does the model predict now?','We must see the current prediction before we can judge it. Follow the input through multiplication to the output. Nothing is learning yet: the weight is still 1. In a larger model there are more operations along this route.','Prediction rule: ŷ = xw. Substitute the input and the current weight for each card.'],
      ['Loss: how far are those predictions from the targets?','The training target supplies the desired answer. Subtract it from each prediction, then square the error. A loss is a score; it does not yet tell us how to change the weight.','Loss rule per card: L = (prediction − target)². The targets remain fixed.'],
      ['Backward: how sensitive is the loss to the weight?','Trace the dependencies backward: loss ← prediction ← weight. The square contributes 2 × error, and prediction changes at rate x with respect to w. Multiply them using the chain rule. These arrows carry derivative information, not input data traveling backward.','Gradient rule: g = 2(xw − y)x. A negative gradient suggests increasing this weight to lower loss locally. Weight is STILL 1.'],
      ['Combine the cards before making one change','Our objective is the mean of the card losses. The derivative of that average is the average of their gradients. All cards used the same weight, so this is one shared direction for the selected batch.','Mean loss = '+fmt(v.loss)+'. Mean gradient = '+fmt(v.gradient)+'. Add the values and divide by '+s.batch+'. With one card, its value is already the mean.'],
      ['Update: this is when the model changes','The optimizer is the rule for changing parameters. We use gradient descent: subtract learning rate × gradient. The rate scales the move; it is not the gradient itself. Saved predictions on the left are from the old weight and must be recomputed.','w_new = w_old − ηg = 1 − '+s.rate+' × ('+fmt(v.gradient)+') = '+fmt(v.weight)+'. The targets do not change.'],
      ['Forward again: did the changed weight help?','Use the new weight to recalculate predictions and loss. This comparison checks what the update did. A large step can overshoot and increase loss; a backward pass alone cannot guarantee a safe update size.','Mean loss before = '+fmt(v.loss)+'; after = '+fmt(v.nextLoss)+'. '+(v.nextLoss<v.loss?'This update reduced the selected batch’s loss.':'This update did not reduce the selected batch’s loss.')+' This is not a held-out evaluation.'],
      ['One update is one step; one dataset pass is one epoch','Imagine six cards in a dataset. With batch size two, process cards 1–2 and update, then 3–4 and update, then 5–6 and update. Those three steps complete one epoch. A new epoch revisits the cards using the weights reached so far.','For six cards: batch size 2 → 3 updates per epoch; batch size 1 → 6 updates per epoch. This assumes one update per batch and no gradient accumulation.']
    ][i];
    root.querySelector('[data-story-scene]').innerHTML=`
      <p class="training-scene-number">SCENE ${i+1} OF 8 · ${labels[i]}</p>
      <h3>${captions[0]}</h3><p>${captions[1]}</p>
      <p class="training-rule">${captions[2]}</p>
      <div class="training-cards">${cards}</div>
      <div class="training-flow ${i===3?'training-backward':''}">
        <div class="training-node ${[0,5].includes(i)?'is-current':''}"><b>Weight · the dial</b><strong>${i>=5?fmt(v.weight):'1'}</strong><small>${i===5?'Changed by the optimizer':i>5?'New weight':'Unchanged so far'}</small></div>
        <span class="training-arrow" aria-hidden="true">${i===3?'←':'→'}</span>
        <div class="training-node ${[1,6].includes(i)?'is-current':''}"><b>Prediction</b><strong>${i>=1?prediction:'Not calculated yet'}</strong><small>${i===5?'From OLD weight 1':'Input × current weight'}</small></div>
        <span class="training-arrow" aria-hidden="true">${i===3?'←':'→'}</span>
        <div class="training-node ${i===2?'is-current':''}"><b>${i>=6?'Mean loss after':'Loss per card'}</b><strong>${i>=6?fmt(v.nextLoss):i>=2?losses:'Not calculated yet'}</strong><small>${i===5?'From OLD predictions':'Compare with fixed targets'}</small></div>
      </div>
      <div class="training-gradient ${[3,4].includes(i)?'is-current':''}"><b>Gradients · guidance for a change</b><p>${i>=3?gradients:'Not calculated yet. First make and score a prediction.'}</p>${i>=4?`<p>Mean gradient: <strong>${fmt(v.gradient)}</strong> ${i>=5?'(calculated at the old weight 1)':''}</p>`:''}</div>
      ${i===7?'<div class="training-epoch"><span>Cards 1–2<br>Step 1</span><span>Cards 3–4<br>Step 2</span><span>Cards 5–6<br>Step 3</span></div><p>All six cards used once = one epoch. This row illustrates a separate six-card dataset.</p>':''}`;
    root.querySelectorAll('[data-story-stage]').forEach(b=>b.setAttribute('aria-current',Number(b.dataset.storyStage)===i?'step':'false'));
    root.querySelector('[data-story-action="back"]').disabled=i===0;
    root.querySelector('[data-story-action="next"]').disabled=i===7;
    const play=root.querySelector('[data-story-action="play"]');play.textContent=s.playing?'Pause':i===7?'Replay walkthrough':'Play walkthrough';play.setAttribute('aria-pressed',String(s.playing));
  }
  function pause(root) { const s=states.get(root);clearTimeout(s.timer);s.playing=false; }
  function tick(root) {
    const s=states.get(root);
    s.timer=setTimeout(()=>{if(!root.isConnected){pause(root);return;} if(document.hidden){pause(root);render(root);return;}s.stage=Math.min(7,s.stage+1);if(s.stage===7)s.playing=false;render(root);if(s.playing)tick(root);},7000);
  }
  window.mountTrainingStories = container => container.querySelectorAll('[data-training-story]').forEach(root=>{
    if(states.has(root))return;
    const s={stage:0,batch:1,rate:0.1,playing:false,timer:null};states.set(root,s);render(root);
    root.addEventListener('click',e=>{
      const button=e.target.closest('button');if(!button)return;
      const action=button.dataset.storyAction;
      if(button.dataset.storyStage!==undefined){pause(root);s.stage=Number(button.dataset.storyStage);}
      else if(action==='play'){if(s.playing)pause(root);else{if(s.stage===7)s.stage=0;s.playing=true;tick(root);}}
      else if(action){pause(root);s.stage=action==='reset'?0:Math.max(0,Math.min(7,s.stage+(action==='next'?1:-1)));}
      render(root);
    });
    root.addEventListener('change',()=>{pause(root);s.stage=0;s.batch=Number(root.querySelector('[data-story-batch]').value);s.rate=Number(root.querySelector('[data-story-rate]').value);render(root);});
  });
})();
