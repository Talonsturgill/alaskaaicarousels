
(function(){
  'use strict';
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* live countdowns: chips with data-date tick down to the start of that day */
  function pad(n){ return (n < 10 ? '0' : '') + n; }
  function tickChips(){
    var now = new Date();
    var mid = new Date(now); mid.setHours(0,0,0,0);
    document.querySelectorAll('[data-date]').forEach(function(el){
      var d = new Date(el.getAttribute('data-date') + 'T00:00:00');
      var days = Math.round((d - mid) / 86400000);
      var t;
      if (days < 0) { t = 'window passed'; el.classList.remove('days'); el.style.color = '#8da2be'; }
      else if (days === 0) { t = 'TODAY'; }
      else if (days > 14) { t = 'in ' + days + ' days'; }
      else {
        var ms = d - now, hh = Math.floor(ms / 3600000) % 24,
            mm = Math.floor(ms / 60000) % 60, ss = Math.floor(ms / 1000) % 60,
            dd = Math.floor(ms / 86400000);
        t = 'in ' + dd + 'd ' + pad(hh) + 'h ' + pad(mm) + 'm ' + pad(ss) + 's';
      }
      if (el.textContent !== t) el.textContent = t;
    });
  }
  tickChips();
  setInterval(tickChips, 1000);

  /* sticky nav turns to glass once the page moves */
  var nav = document.querySelector('.topnav');
  if (nav) {
    var onScroll = function(){ nav.classList.toggle('scrolled', scrollY > 30); };
    addEventListener('scroll', onScroll, {passive: true}); onScroll();
  }

  /* reveals */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin: '0px 0px -8% 0px'});
    document.querySelectorAll('[data-reveal]').forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function(el){ el.classList.add('in'); });
  }

  /* stat numbers count up when they enter the viewport */
  function countUp(el){
    var to = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduced || to === 0) { el.textContent = pad(to); return; }
    var t0 = null;
    function step(ts){
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / 900), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pad(Math.round(to * e));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); } });
    }, {threshold: 0.6});
    document.querySelectorAll('[data-count]').forEach(function(el){ cio.observe(el); });
  } else {
    document.querySelectorAll('[data-count]').forEach(countUp);
  }

  /* deck gallery: counter, arrows, keyboard, lightbox */
  var gal = document.querySelector('.gallery');
  if (gal) {
    var imgs = Array.prototype.slice.call(gal.querySelectorAll('img'));
    var count = document.querySelector('.galbar .count');
    var cur = 0;
    function setCur(i){
      cur = Math.max(0, Math.min(imgs.length - 1, i));
      if (count) count.textContent = pad(cur + 1) + ' / ' + pad(imgs.length);
    }
    setCur(0);
    if ('IntersectionObserver' in window) {
      var gio = new IntersectionObserver(function(es){
        es.forEach(function(e){ if (e.isIntersecting) setCur(imgs.indexOf(e.target)); });
      }, {root: gal, threshold: 0.6});
      imgs.forEach(function(im){ gio.observe(im); });
    }
    function go(i){
      var im = imgs[Math.max(0, Math.min(imgs.length - 1, i))];
      if (im) im.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block: 'nearest', inline: 'center'});
    }
    var prev = document.querySelector('.galbar .prev'), next = document.querySelector('.galbar .next');
    if (prev) prev.addEventListener('click', function(){ go(cur - 1); });
    if (next) next.addEventListener('click', function(){ go(cur + 1); });

    var lb = document.querySelector('.lightbox');
    if (lb && lb.showModal) {
      var lbimg = lb.querySelector('img'), lbcount = lb.querySelector('.count'), li = 0;
      function show(i){
        li = (i + imgs.length) % imgs.length;
        lbimg.src = imgs[li].src;
        lbimg.alt = imgs[li].alt;
        if (lbcount) lbcount.textContent = pad(li + 1) + ' / ' + pad(imgs.length);
      }
      imgs.forEach(function(im, i){
        im.addEventListener('click', function(){ show(i); lb.showModal(); });
      });
      lb.querySelector('.lbclose').addEventListener('click', function(){ lb.close(); });
      lb.querySelector('.lbprev').addEventListener('click', function(){ show(li - 1); });
      lb.querySelector('.lbnext').addEventListener('click', function(){ show(li + 1); });
      lb.addEventListener('click', function(e){ if (e.target === lb) lb.close(); });
      addEventListener('keydown', function(e){
        if (!lb.open) return;
        if (e.key === 'ArrowLeft') show(li - 1);
        if (e.key === 'ArrowRight') show(li + 1);
      });
    }
  }

})();
