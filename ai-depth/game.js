/* Rewards are derived from the existing progress record: opening a page earns nothing. */
window.STUDY_GAME = (() => {
  const points={reading:100,coding:120,design:100,lab:80,recall:60,localai:70};
  const ranks=[[0,'Neuron Novice'],[250,'Token Trapper'],[600,'Embedding Explorer'],[1100,'Attention Architect'],[1800,'Loss Optimizer'],[2700,'KV Cache Master'],[3800,'RAG Navigator'],[5100,'Agent Orchestrator'],[6600,'Safety Sentinel'],[8300,'Principal AI Engineer']];
  function score(state){
    let xp=Object.keys(state.achievements||{}).length*100;
    for(let d=1;d<=30;d++){const x=state.days[d]||{};for(const [k,value] of Object.entries(points))if(x.checks?.[k])xp+=value;if(x.notes?.trim().length>=20)xp+=50;if(x.quizDone)xp+=25;}
    return xp;
  }
  function render(state,d){
    const xp=score(state),index=ranks.findLastIndex(([min])=>xp>=min),rank=ranks[index];
    const next=ranks[index+1],percent=next?Math.min(100,(xp-rank[0])/(next[0]-rank[0])*100):100;
    const keys=Object.keys(points),completed=Array.from({length:30},(_,i)=>i+1).filter(n=>keys.every(k=>state.days[n]?.checks?.[k])).length;
    const activities=Array.from({length:30},(_,i)=>i+1).reduce((sum,n)=>sum+keys.filter(k=>state.days[n]?.checks?.[k]).length,0);
    const checks=state.days[d]?.checks||{},task=keys.find(k=>!checks[k]);
    const steps={reading:'learn',coding:'coding',design:'design',lab:'learn',recall:'explain',localai:'learn'};
    const labels={reading:'AI reading',coding:'Coding',design:'System design',lab:'Hands-on lab',recall:'Interview recall',localai:'Everyday local AI'};
    const target=task?d:Math.min(30,d+1),href=`#day-${target}${task?'/'+steps[task]:''}`;
    return `<section class="game-profile" aria-label="Your study rewards"><div class="game-profile-top"><div><span class="kicker">YOUR STUDY ADVENTURE</span><h2>Level ${index+1} · ${rank[1]}</h2><p>${xp.toLocaleString()} XP earned · ${activities} activities completed</p></div><span class="game-emblem" aria-hidden="true">✦</span></div><div class="game-meter" role="progressbar" aria-label="Progress toward the next XP level" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(percent)}"><i style="width:${percent}%"></i></div><p class="game-next">${next?`${next[0]-xp} XP to Level ${index+2} · ${next[1]}`:'Top XP level reached. Keep practising your skills.'}</p><div class="game-milestones"><span class="${xp>0?'earned':''}">✦ First steps ${xp>0?'✓':''}</span><span class="${completed>=1?'earned':''}">★ First full day ${completed>=1?'✓':''}</span><span class="${completed>=7?'earned':''}">◆ 7 full days ${completed>=7?'✓':''}</span><span class="${completed>=30?'earned':''}">♛ 30 full days ${completed>=30?'✓':''}</span></div><div class="game-mission"><div><b>${task?'Next for Day '+d+': '+labels[task]:'Day '+d+' complete — well done!'}</b><small>${task?'Study it, then tick its checkbox to earn '+points[task]+' XP.':'All six activities are checked.'}</small></div><a class="button primary" href="${href}">${task?'Study this activity':'Continue'} →</a></div><details class="game-rules"><summary>How XP works · your previous rewards count</summary><p>Activities earn 60–120 XP. Your original day notes (20+ characters), completed quizzes, and saved achievements retain their original bonuses. Undoing a checkbox removes its activity XP; checking it repeatedly never earns extra. XP measures study progress, not interview readiness.</p><p>${completed}/30 days fully finished. ${Object.keys(state.achievements||{}).length} saved achievements retained${state.streak?.count?'; previous recorded streak: '+Number(state.streak.count)+' days':''}.</p></details></section>`;
  }
  return {points,score,render};
})();
