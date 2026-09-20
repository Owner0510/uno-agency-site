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
    lb.setAttribute('aria-label', 'Збільшений скріншот');
    var big = d.createElement('img');
    big.alt = '';
    lb.appendChild(big);
    d.body.appendChild(lb);
    var close = function () { lb.classList.remove('on'); };
    body.addEventListener('click', function (e) {
      var t = e.target;
      if (t.tagName !== 'IMG') return;
      big.src = t.currentSrc || t.src;
      big.alt = t.alt;
      lb.classList.add('on');
    });
    lb.addEventListener('click', close);
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }
})();
