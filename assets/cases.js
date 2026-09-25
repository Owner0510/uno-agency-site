(function () {
  var d = document;

  /* catalog filter: chips toggle cards by data-cat; the choice lives in the URL hash */
  var chips = d.querySelectorAll('.chip[data-f]');
  if (chips.length) {
    var cards = d.querySelectorAll('.card[data-cat]');
    var valid = ['all', 'meta', 'smm', 'both'];
    var apply = function (f) {
      if (valid.indexOf(f) < 0) f = 'all';
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.f === f)); });
      cards.forEach(function (c) { c.hidden = f !== 'all' && c.dataset.cat !== f; });
      try { history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f); } catch (e) {}
    };
    chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.dataset.f); }); });
    apply(location.hash.slice(1));
  }

  /* lightbox for screenshots on case pages */
  var body = d.querySelector('.case-body');
  if (body) {
    var lb = d.createElement('div');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Збільшений скріншот');
    lb.tabIndex = -1;
    var big = d.createElement('img');
    big.alt = '';
    lb.appendChild(big);
    d.body.appendChild(lb);
    var opener = null;
    var close = function () {
      if (!lb.classList.contains('on')) return;
      lb.classList.remove('on');
      if (opener) { opener.focus(); opener = null; }
    };
    var open = function (t) {
      opener = t;
      big.src = t.currentSrc || t.src;
      big.alt = t.alt;
      lb.classList.add('on');
      lb.focus();
    };
    /* screenshots are focusable buttons so the lightbox works from the keyboard */
    body.querySelectorAll('img').forEach(function (im) {
      im.tabIndex = 0;
      im.setAttribute('role', 'button');
      im.setAttribute('aria-label', 'Збільшити: ' + (im.alt || 'скріншот'));
    });
    body.addEventListener('click', function (e) {
      if (e.target.tagName === 'IMG') open(e.target);
    });
    body.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target.tagName === 'IMG') { e.preventDefault(); open(e.target); }
    });
    lb.addEventListener('click', close);
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }
})();
