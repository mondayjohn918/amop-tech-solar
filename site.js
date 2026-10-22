// Shared by both pages: mark JS as running and reveal blocks once as they scroll in.
(() => {
  document.documentElement.classList.add('js');
  const items = document.querySelectorAll('.rv');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { items.forEach(el => el.classList.add('in')); return; }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -10% 0px' });
  items.forEach(el => io.observe(el));
})();
