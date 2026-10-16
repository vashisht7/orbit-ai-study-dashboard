/* Shared, accessible diagram cards + 3Blue1Brown interactive theater for dashboard, beginner reader, and visual map. */
(() => {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  window.renderLessonGuide = (day, prefix = '') => {
    const g = window.LESSON_GUIDES[Number(day)-1];
    if (!g) return '';
    const href = window.HELLO_PROBLEMS?.[g.problem] || `${prefix}practice.html#${g.problem}`;
    const b1bHtml = typeof window.render3B1BTheaterHTML === 'function' ? window.render3B1BTheaterHTML(day) : '';
    return `<section class="learn-guide" aria-label="Simple explanation and topic diagram">
      <p class="learn-kicker">REVIEW · CONNECT THE STEPS</p><h2>${esc(g.title)}</h2><p>${esc(g.summary)}</p>
      <p class="learn-help">Follow the arrows. Select a step to understand what happens.</p>
      <ol class="learn-flow">${g.steps.map(([name, detail], i) => `<li><button type="button" data-guide-step="${i}" aria-pressed="${i===0}"><span>${i+1}</span>${esc(name)}</button></li>`).join('')}</ol>
      <p class="learn-detail" aria-live="polite"><b>${esc(g.steps[0][0])}:</b> ${esc(g.steps[0][1])}</p>
      <p><b>Small example:</b> ${esc(g.example)}</p>
      <details><summary>Check your understanding</summary><p>${esc(g.check)}</p><p>Explain the diagram without looking, then use the full lesson to check your answer.</p></details>
      <a class="learn-practice" href="${esc(href)}" ${href.startsWith('https:') ? 'target="_blank" rel="noopener noreferrer"' : ''}>Practice the related concept · ${href.startsWith('https:') ? 'Hello Interview ↗' : 'Code Lab →'}</a>

      <span hidden data-guide-day="${g.day}"></span>
    </section>${b1bHtml ? `<section class="lesson-animation" id="lesson-animation-${g.day}" aria-label="Lesson ${g.day} animation">${b1bHtml}</section>` : ''}`;
  };
  // The same navigation and section IDs are used by both daily readers.
  window.renderLessonContents = day => {
    const c = window.BEGINNER?.[Number(day)-1];
    if (!c) return '';
    const headings = [...c.body.matchAll(/^### (.+)$/gm)].map(m => m[1]);
    return `<nav class="lesson-contents" aria-label="Lesson ${Number(day)} sections">
      <p><b>Understand the rule, then try it</b></p>
      <button type="button" class="lesson-watch" data-open-lesson-animation="${Number(day)}">🎬 ${window.getLessonVisualKind?.(day) === 'diagram' ? 'Explore' : 'Watch'} Lesson ${Number(day)} ${window.getLessonVisualKind?.(day) || 'animation'}</button>
      <p class="lesson-contents-help">Read in order, or jump to the part you want to understand.</p>
      <ol>${headings.map((h,i)=>`<li><button type="button" data-lesson-section="lesson-${Number(day)}-section-${i}">${esc(h)}</button></li>`).join('')}</ol>
    </nav>`;
  };
  window.renderLessonText = (day, renderer) => {
    let i = 0;
    return renderer(window.BEGINNER[Number(day)-1].body).replace(/<h3>/g, () => `<h3 id="lesson-${Number(day)}-section-${i++}" class="lesson-section-heading" tabindex="-1">`);
  };
  document.addEventListener('click', event => {
    const jump = event.target.closest('[data-lesson-section]');
    if (jump) {
      const heading = document.getElementById(jump.dataset.lessonSection);
      heading?.scrollIntoView({block:'start'});
      heading?.focus({preventScroll:true});
      return;
    }
    const watch = event.target.closest('[data-open-lesson-animation]');
    if (watch) {
      if (typeof window.openLessonAnimation === 'function') window.openLessonAnimation();
      else document.getElementById('lesson-animation-'+watch.dataset.openLessonAnimation)?.scrollIntoView({block:'start'});
      return;
    }
    const button = event.target.closest('[data-guide-step]');
    if (!button) return;
    const card = button.closest('.learn-guide');
    const g = window.LESSON_GUIDES[Number(card.querySelector('[data-guide-day]').dataset.guideDay)-1];
    card.querySelectorAll('[data-guide-step]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    const [title, detail] = g.steps[Number(button.dataset.guideStep)];
    card.querySelector('.learn-detail').innerHTML = `<b>${esc(title)}:</b> ${esc(detail)}`;
  });
})();
