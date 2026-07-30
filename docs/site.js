
/* ---------- readership ----------
   In its OWN IIFE, and first, on purpose. Sitting at the end of the main one
   meant any earlier failure in the map, gallery or lightbox code would starve
   it, and readership would silently stop being counted while the page still
   looked fine. A counter must not depend on the rest of the page succeeding,
   and nothing below depends on the counter either.

   Counts that a page was read and deliberately learns nothing about who read
   it. No cookie is set or read, no localStorage, no visitor id, nothing that
   could identify or re-identify anyone. The only things sent are the path, the
   referrer's HOST (a full referrer URL never leaves the browser, it can carry
   private context) and an explicit campaign tag when the link had one.

   Honours Do Not Track and Global Privacy Control by sending nothing at all.
   Silent on failure, because a counter must never be visible on the page or
   delay it. Full disclosure lives at /privacy/. */
(function(){
  'use strict';
  try {
    var nav = navigator || {};
    if (nav.doNotTrack === '1' || nav.globalPrivacyControl === true ||
        window.doNotTrack === '1' || nav.msDoNotTrack === '1') return;
    if (/^(localhost|127\.|0\.0\.0\.0|\[?::1)/.test(location.hostname) ||
        location.protocol === 'file:') return;
    var q = new URLSearchParams(location.search);
    var host = null;
    if (document.referrer) {
      try { host = new URL(document.referrer).hostname; } catch (e) { host = null; }
    }
    var payload = JSON.stringify({
      p: location.pathname,
      r: host ? ('https://' + host + '/') : null,
      c: q.get('c') || q.get('utm_campaign') || null
    });
    var TRACK = 'https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1/track';
    /* text/plain, NOT application/json, and that is the whole reason this
       works. A JSON content type is not CORS safelisted, so it makes the
       browser send a preflight first, and sendBeacon cannot carry the headers
       that preflight then negotiates (it has no headers API at all beyond the
       Blob type). The observed result was nine OPTIONS preflights from real
       visits with not one POST behind them: every reader was counted as zero.

       text/plain is safelisted, so this is a simple request with no preflight
       and nothing to negotiate. The collector parses the body as JSON
       regardless of what the content type claims, so nothing is lost. */
    var body = new Blob([payload], {type: 'text/plain;charset=UTF-8'});
    if (!(nav.sendBeacon && nav.sendBeacon(TRACK, body))) {
      /* sendBeacon returns false when it refuses to queue, so fall through
         rather than assume it took it. */
      fetch(TRACK, {method: 'POST', headers: {'content-type': 'text/plain;charset=UTF-8'},
                    body: payload, keepalive: true, mode: 'cors'}).catch(function(){});
    }
  } catch (e) { /* a counter never breaks a page */ }
})();

(function(){
  'use strict';
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* live countdowns: chips with data-date tick down to the start of that day.
     The dates are Alaska calendar dates (a public-comment deadline is an
     Alaska/agency date), so the day boundary must flip at Alaska midnight, not
     the viewer's. Parsing 'YYYY-MM-DDT00:00:00' used the viewer's local zone, so
     a reader in Sydney saw "window passed" ~19h before the window actually
     closed in Alaska. Compute both sides in Alaska wall-clock instead. */
  function pad(n){ return (n < 10 ? '0' : '') + n; }
  var akFmt;
  try { akFmt = new Intl.DateTimeFormat('en-US', {timeZone: 'America/Anchorage',
    year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',
    second:'2-digit',hour12:false}); } catch(e) { akFmt = null; }
  /* "now" as an Alaska wall-clock instant, expressed via Date.UTC so both the
     target midnight and now use the same fiction and subtract cleanly. Falls
     back to plain local time where Intl lacks the zone (very old engines). */
  function akNow(){
    if (!akFmt) return Date.now();
    var g = {}; akFmt.formatToParts(new Date()).forEach(function(p){ g[p.type] = p.value; });
    var hh = g.hour === '24' ? 0 : +g.hour;
    return Date.UTC(+g.year, +g.month - 1, +g.day, hh, +g.minute, +g.second);
  }
  function tickChips(){
    var now = akNow();
    var mid = Date.UTC(new Date(now).getUTCFullYear(), new Date(now).getUTCMonth(), new Date(now).getUTCDate());
    document.querySelectorAll('[data-date]').forEach(function(el){
      var p = el.getAttribute('data-date').split('-');
      var target = Date.UTC(+p[0], +p[1] - 1, +p[2]);  /* Alaska midnight of that day */
      var days = Math.round((target - mid) / 86400000);
      var t;
      if (days < 0) { t = 'window passed'; el.classList.remove('days'); el.style.color = '#8da2be'; }
      else if (days === 0) { t = 'TODAY'; }
      else if (days > 14 || reduced) { t = 'in ' + days + (days === 1 ? ' day' : ' days'); }
      else {
        var ms = target - now, hh = Math.floor(ms / 3600000) % 24,
            mm = Math.floor(ms / 60000) % 60, ss = Math.floor(ms / 1000) % 60,
            dd = Math.floor(ms / 86400000);
        t = 'in ' + dd + 'd ' + pad(hh) + 'h ' + pad(mm) + 'm ' + pad(ss) + 's';
      }
      if (el.textContent !== t) el.textContent = t;
    });
  }
  tickChips();
  /* WCAG 2.2.2: a per-second ticker is auto-updating info with no pause control,
     so under prefers-reduced-motion show day granularity and refresh once a
     minute instead of every second. */
  setInterval(tickChips, reduced ? 60000 : 1000);

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
  /* The reveal machinery is now wired, so cancel the inline failsafe. If this
     script had failed to load or thrown before here, the timeout would fire and
     reveal-fallback would show all [data-reveal] content, so a broken deploy
     shows the whole page rather than only the hero over a blank body. */
  clearTimeout(window.__revealFallback);

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
