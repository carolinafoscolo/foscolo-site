/* Progressive enhancement: navigation stays visible when JavaScript is unavailable. */
(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  if (!button || !nav) return;
  document.documentElement.classList.add('js');
  button.hidden = false;
  const setOpen = (open) => {
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? button.dataset.close : button.dataset.open);
    nav.classList.toggle('is-open', open);
  };
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      button.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target) && !button.contains(event.target)) setOpen(false);
  });
  window.matchMedia('(min-width: 1001px)').addEventListener('change', () => setOpen(false));
})();
