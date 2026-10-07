/* Shared, accessible diagram cards for the dashboard, beginner reader and map. */
(() => {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  window.renderLessonGuide = (day, prefix = '') => {
    const g = window.LESSON_GUIDES[Number(day)-1];
    if (!g) return '';
    const href = window.HELLO_PROBLEMS?.[g.problem] || `${prefix}practice.html#${g.problem}`;
    const deep = (window.AI_DEPTH_LINKS || []).filter(c => c.days.includes(Number(day)));
    return `<section class="learn-guide" aria-label="Simple explanation and topic diagram">
      <p class="learn-kicker">START HERE · THE TWO-MINUTE VERSION</p><h2>${esc(g.title)}</h2><p>${esc(g.summary)}</p>
      <p class="learn-help">Follow the arrows. Select a step to understand what happens.</p>
      <ol class="learn-flow">${g.steps.map(([name, detail], i) => `<li><button type="button" data-guide-step="${i}" aria-pressed="${i===0}"><span>${i+1}</span>${esc(name)}</button></li>`).join('')}</ol>
      <p class="learn-detail" aria-live="polite"><b>${esc(g.steps[0][0])}:</b> ${esc(g.steps[0][1])}</p>
      <p><b>Small example:</b> ${esc(g.example)}</p>
      <details><summary>Check your understanding</summary><p>${esc(g.check)}</p><p>Explain the diagram without looking, then use the full lesson to check your answer.</p></details>
      <a class="learn-practice" href="${esc(href)}" ${href.startsWith('https:') ? 'target="_blank" rel="noopener noreferrer"' : ''}>Practice the related concept · ${href.startsWith('https:') ? 'Hello Interview ↗' : 'Code Lab →'}</a>

      <span hidden data-guide-day="${g.day}"></span>
    </section>`;
  };
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-guide-step]');
    if (!button) return;
    const card = button.closest('.learn-guide');
    const g = window.LESSON_GUIDES[Number(card.querySelector('[data-guide-day]').dataset.guideDay)-1];
    card.querySelectorAll('[data-guide-step]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    const [title, detail] = g.steps[Number(button.dataset.guideStep)];
    card.querySelector('.learn-detail').innerHTML = `<b>${esc(title)}:</b> ${esc(detail)}`;
  });
})();
