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


/* Client-side search over the generated public archive. */
(() => {
  const root = document.querySelector('[data-search-page]');
  if (!root) return;

  const form = root.querySelector('.search-form');
  const input = root.querySelector('input[type="search"]');
  const results = root.querySelector('.search-results');
  const status = root.querySelector('.search-status');
  const lang = root.dataset.lang;

  const normalize = (value) =>
    String(value || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();

  const escapeHTML = (value) =>
    String(value || '').replace(/[&<>"']/g, (char) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    }[char]));

  const score = (doc, tokens) => {
    const title = normalize(doc.title);
    const desc = normalize(doc.desc);
    const meta = normalize(doc.meta);
    const text = normalize(doc.text);
    let total = 0;
    for (const token of tokens) {
      if (!text.includes(token) && !title.includes(token) && !desc.includes(token) && !meta.includes(token)) return -1;
      if (title.includes(token)) total += 8;
      if (meta.includes(token)) total += 5;
      if (desc.includes(token)) total += 3;
      if (text.includes(token)) total += 1;
    }
    return total;
  };

  const render = (docs, query) => {
    const tokens = normalize(query).split(/\s+/).filter(Boolean);
    let matches = docs.map((doc, index) => ({
      ...doc,
      _index: index,
      _score: tokens.length ? score(doc, tokens) : 0
    })).filter((doc) => doc._score >= 0);

    if (tokens.length) matches.sort((a, b) => b._score - a._score || a._index - b._index);

    const label = matches.length === 1 ? root.dataset.one : root.dataset.many;
    status.textContent = tokens.length
      ? (matches.length ? String(matches.length) + ' ' + label : root.dataset.empty)
      : root.dataset.all + ' · ' + String(matches.length);

    results.innerHTML = matches.map((doc) =>
      '<article class="search-result">' +
        '<p class="eyebrow">' + escapeHTML(doc.meta) + '</p>' +
        '<h2><a href="' + escapeHTML(doc.url) + '">' + escapeHTML(doc.title) + '</a></h2>' +
        '<p>' + escapeHTML(doc.desc) + '</p>' +
        '<a class="text-link" href="' + escapeHTML(doc.url) + '">' + escapeHTML(root.dataset.open) + '<span aria-hidden="true"> ↗</span></a>' +
      '</article>'
    ).join('');

    if (!matches.length) results.innerHTML = '<p class="search-empty">' + escapeHTML(root.dataset.empty) + '</p>';
  };

  fetch('/assets/search/' + lang + '.json')
    .then((response) => {
      if (!response.ok) throw new Error('Search index unavailable');
      return response.json();
    })
    .then((docs) => {
      const params = new URLSearchParams(window.location.search);
      input.value = params.get('q') || '';
      render(docs, input.value);

      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = input.value.trim();
        const url = new URL(window.location.href);
        if (query) url.searchParams.set('q', query);
        else url.searchParams.delete('q');
        window.history.replaceState({}, '', url);
        render(docs, query);
      });

      input.addEventListener('input', () => render(docs, input.value));
    })
    .catch(() => {
      status.textContent = root.dataset.empty;
    });
})();
