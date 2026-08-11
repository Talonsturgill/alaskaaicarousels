#!/usr/bin/env python3
"""Current Power Costs, the retail electricity panel on the gas watch page.

WHY THIS IS ITS OWN MODULE. The panel is drawn in one place and authorised in
another. gaswatch_build's numeral lint refuses any figure on that page which
traces back to nothing, and the honest way to bring a second dataset under a
lint like that is to authorise the second dataset rather than to widen the
rule. So html() renders ledger/power.json and numerals() renders the SAME file
the SAME way for the lint to compare against, and the only thing keeping the
two honest is that they sit beside each other and are read together.

They did not, briefly. site_build authorised the figures and gaswatch_pagecheck
did not, so the daily read-only check of the published page went red on the
first build that shipped the panel, reporting invented numerals for prices EIA
had measured. A checker that cries wolf about correct data is worse than no
checker, because the next real finding is the one nobody reads. Both importers
now read one implementation.

WHAT IT PUBLISHES AND WHAT IT REFUSES TO. Measured average retail price by
sector, the change against a year ago, and ten years of the household series.
No forecast and no cause, which are the collector's rules and not this file's
to relax. See scripts/power_collect.py.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gaswatch_build as gw  # esc, counted nouns, and the lint this feeds

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "ledger", "power.json")
esc = gw.esc


def load():
    """The committed file, or None. A missing ledger renders no panel and is
    never a build failure, the same way the gas strip degrades."""
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


# Ten years of months. Long enough that a reader can see whether this year is
# unusual rather than being told it is, short enough that the shape of the last
# two winters is still readable at the width of a phone.
SPARK_MONTHS = 120

CSS = """
/* CURRENT POWER COSTS. A measurement, presented as one. The three sectors sit
   side by side on purpose, because the gap between what a household pays and
   what an industrial customer pays is the thing a reader on this page is
   actually trying to see, and no sentence would say it as plainly. */
.pw{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:18px;}
.pwc{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:17px 18px 15px;}
.pwc .l{font-family:JBMono,ui-monospace,monospace;font-size:10.5px;
letter-spacing:.15em;color:var(--mute);}
.pwc .v{font-family:Fraunces,serif;font-weight:560;font-size:clamp(26px,4vw,36px);
color:var(--snow);line-height:1.05;margin-top:9px;font-variant-numeric:tabular-nums;}
.pwc .u{font-size:12.5px;color:var(--mute);margin-top:3px;}
.pwc .d{font-family:JBMono,ui-monospace,monospace;font-size:11px;
letter-spacing:.05em;margin-top:10px;color:var(--mute);}
.pwc .d b{font-weight:500;font-variant-numeric:tabular-nums;}
.pwc .d.up b{color:var(--amber);}
.pwc .d.down b{color:var(--green);}

/* THE READOUT SITS ABOVE THE LINE AND IS ALWAYS THERE. A floating tooltip was
   the obvious build and it is the wrong one here. The line is 96px tall inside
   a column of prose, so a tooltip either covers the data it describes or hangs
   over the paragraph below it, and on a phone there is no hover to summon it
   with at all. A fixed readout row costs one line of vertical space, never
   clips, never covers anything, and shows the latest month before anyone has
   touched it. Pointing at the line changes what it says; leaving puts the
   latest month back. */
.pwread{display:flex;align-items:baseline;gap:13px;margin-top:24px;
min-height:27px;flex-wrap:wrap;}
.pwread-m{font-family:JBMono,ui-monospace,monospace;font-size:10.5px;
letter-spacing:.15em;color:var(--mute);text-transform:uppercase;}
.pwread-v{font-family:Fraunces,serif;font-size:19px;color:var(--mute);
font-variant-numeric:tabular-nums;}
.pwread-v b{font-weight:560;color:var(--gold);font-size:22px;}
.pwchart{position:relative;margin-top:4px;}
.pwspark{display:block;width:100%;height:96px;overflow:visible;
touch-action:pan-y;}
.pwspark path{fill:none;stroke:var(--gold);stroke-width:1.6;
stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke;}
.pwspark .fill{fill:url(#pwgrad);stroke:none;}
.pwspark .end{fill:var(--gold);}
/* The crosshair says WHERE on the line the readout is reading from. Without it
   the reader has a number and no idea which of 120 months it belongs to. */
.pwrule{stroke:var(--snow);stroke-width:1;vector-effect:non-scaling-stroke;}
.pwdot{fill:var(--snow);}
.pwhit{cursor:crosshair;}
.pwhit:focus{outline:none;}
.pwhit:focus-visible{outline:2px solid var(--halo);outline-offset:-2px;}
/* Endpoint months as HTML rather than SVG text. The line is drawn with
   preserveAspectRatio none so it can fill any width, which stretches type
   horizontally, and at phone width a 640 unit viewBox takes 10px mono down to
   about 5px. Outside the svg both problems disappear. */
.pwaxis{display:flex;justify-content:space-between;
font-family:JBMono,ui-monospace,monospace;font-size:10px;letter-spacing:.12em;
color:var(--mute);text-transform:uppercase;margin-top:7px;}
.pwnote{font-size:13.5px;color:var(--mute);line-height:1.62;margin-top:16px;}
@media (max-width:640px){.pw{grid-template-columns:1fr;}}
"""

# The power line's hover layer. Small enough to inline, and with JS off the
# reader still gets the line, the endpoint months and the latest reading, which
# is why the readout renders filled in rather than empty.
JS = r"""
(function(){
  var c = document.querySelector('.pwchart');
  if (!c) return;
  var data;
  try { data = JSON.parse(c.getAttribute('data-pw')); } catch (e) { return; }
  var hits = c.querySelectorAll('.pwhit');
  var rule = c.querySelector('.pwrule'), dot = c.querySelector('.pwdot');
  var mo = document.querySelector('.pwread-m');
  var val = document.querySelector('.pwread-v b');
  if (!hits.length || !rule || !dot || !mo || !val) return;
  var home = [mo.textContent, val.textContent];

  function rest(){
    rule.setAttribute('opacity','0');
    dot.setAttribute('opacity','0');
    mo.textContent = home[0];
    val.textContent = home[1];
  }

  function show(i, el){
    var row = data[i];
    if (!row) return;
    var x = el.getAttribute('data-x'), y = el.getAttribute('data-y');
    rule.setAttribute('x1', x); rule.setAttribute('x2', x);
    rule.setAttribute('opacity','.5');
    dot.setAttribute('cx', x); dot.setAttribute('cy', y);
    dot.setAttribute('opacity','1');
    // textContent, never innerHTML. These strings are data.
    mo.textContent = row[0];
    val.textContent = row[1];
  }

  // Roving tabindex, one stop for the whole line. Ten years is 120 months and
  // a tab stop per month would be 120 presses to get past a sparkline.
  function rove(i){
    if (i < 0 || i >= hits.length) return;
    for (var a=0;a<hits.length;a++) hits[a].setAttribute('tabindex', a===i ? '0' : '-1');
    hits[i].focus();
  }

  for (var i=0;i<hits.length;i++){
    (function(el){
      var idx = parseInt(el.getAttribute('data-i'), 10);
      el.addEventListener('pointerenter', function(){ show(idx, el); });
      el.addEventListener('focus', function(){ show(idx, el); });
      el.addEventListener('blur', rest);
      el.addEventListener('keydown', function(ev){
        var to = ev.key === 'ArrowLeft' ? idx - 1
               : ev.key === 'ArrowRight' ? idx + 1
               : ev.key === 'Home' ? 0
               : ev.key === 'End' ? hits.length - 1 : null;
        if (to === null) return;
        ev.preventDefault();
        rove(to);
      });
    })(hits[i]);
  }
  c.addEventListener('pointerleave', rest);
})();
"""


def html(today):
    """What a kilowatt hour costs in Alaska, measured, with nothing added.

    THE QUESTION THIS ANSWERS. A reader who arrives at a page about data
    centres and the grid is often asking whether their own bill is going up.
    The record had no answer at all, because the body that would know is the
    Regulatory Commission of Alaska and its site answers a bot with a 403.

    WHAT IT REFUSES TO SAY. No forecast, in either direction, for the same
    reason the gas watch publishes no shortfall call. And no attribution: the
    price moved is a measurement, the price moved BECAUSE of data centres is a
    claim this data cannot carry, since EIA does not break out who used the
    power or why the rate changed. The docket tracks the decisions and this
    tracks the number, and joining them is the reader's judgement.
    """
    d = load()
    if not d:
        return ""
    sect = d.get("sectors") or {}
    if not all(k in sect for k in ("residential", "commercial", "industrial")):
        return ""

    def card(key, label):
        s = sect[key]
        ch = s.get("change_year")
        way = "up" if (ch or 0) > 0 else "down" if (ch or 0) < 0 else ""
        # "up 2.15 on a year ago" was the first phrasing and it is not a
        # sentence anyone says. The unit belongs in the clause, because the
        # figure above it is a price and this one is a difference between two
        # prices, and dropping the noun made the two look like the same kind of
        # number.
        move = (f'<div class="d {way}">{"up" if way == "up" else "down"} '
                f'<b>{abs(ch):.2f}</b> cents from a year ago</div>') if ch else (
                '<div class="d">level with a year ago</div>'
                if ch is not None else "")
        return (f'<div class="pwc"><div class="l">{esc(label)}</div>'
                f'<div class="v">{s["latest"]:.2f}</div>'
                f'<div class="u">cents per kilowatthour</div>{move}</div>')

    # The line is the last ten years of the residential series, which is what
    # makes this year legible as normal or not without anyone saying so.
    res = sect["residential"]
    pts = list(reversed(res["data"]))[-SPARK_MONTHS:]
    vals = [p[1] for p in pts]
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1
    w, h = 640, 96

    # X IS THE DATE, NOT THE POSITION IN THE ARRAY. EIA published no figure for
    # August or September 2016, so this window holds 120 readings across 122
    # months. Spacing the points evenly draws that three month step as a one
    # month step, which is a small lie a chart tells about a real hole in a
    # public record. Placed on their dates, the hole shows.
    def mnum(p):
        return int(p[:4]) * 12 + int(p[4:6]) - 1

    t0 = mnum(pts[0][0])
    tspan = (mnum(pts[-1][0]) - t0) or 1
    xy = [((mnum(p) - t0) / tspan * w, h - (v - lo) / span * (h - 10) - 5)
          for p, v in pts]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    area = line + f" L{w} {h} L0 {h} Z"

    # One hit target per reading, spanning the full height, so the pointer aims
    # at a month rather than at a 1.6px line. Each one runs from the midpoint
    # behind it to the midpoint ahead, which keeps the targets touching with no
    # overlap however unevenly the readings fall. Geometry rides on the rect so
    # the script never recomputes what Python already worked out, and every one
    # of these attributes is invisible to the numeral lint, which strips tags.
    xs = [x for x, _ in xy]
    edges = [0.0] + [(a + b) / 2 for a, b in zip(xs, xs[1:])] + [float(w)]
    hits = "".join(
        f'<rect class="pwhit" x="{edges[i]:.1f}" y="0" '
        f'width="{edges[i + 1] - edges[i]:.1f}" height="{h}" fill="transparent" '
        f'data-i="{i}" data-x="{x:.1f}" data-y="{y:.1f}" '
        f'tabindex="{0 if i == 0 else -1}" '
        f'role="button" aria-label="{esc(month_name(pts[i][0]))}, '
        f'{vals[i]:.2f} cents per kilowatthour"/>'
        for i, (x, y) in enumerate(xy))
    # Month and price, in the order the readout says them, so the script does no
    # formatting and cannot format them differently from the server.
    payload = json.dumps([[month_name(p[0]), f"{p[1]:.2f}"] for p in pts])

    spark = (
        f'<div class="pwchart" data-pw="{esc(payload)}">'
        f'<svg class="pwspark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
        f'role="img" aria-label="Alaska residential electricity price, '
        f'{esc(gw.count(len(vals), "month"))} from '
        f'{esc(month_name(pts[0][0]))} to {esc(month_name(pts[-1][0]))}">'
        f'<defs><linearGradient id="pwgrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#ffc72c" stop-opacity=".16"/>'
        f'<stop offset="1" stop-color="#ffc72c" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<path class="fill" d="{area}"/><path d="{line}"/>'
        f'<line class="pwrule" x1="0" y1="0" x2="0" y2="{h}" opacity="0"/>'
        f'<circle class="pwdot" cx="0" cy="0" r="3.4" opacity="0"/>'
        f'<circle class="end" cx="{xy[-1][0]:.1f}" cy="{xy[-1][1]:.1f}" r="3"/>'
        f'{hits}</svg></div>')

    return f"""<h2 data-reveal>Current Power Costs</h2>
<p class="sub" data-reveal>The average retail price of electricity in Alaska, measured by the
US Energy Information Administration and published monthly. It is one number for the whole
state, so it shows which way prices are moving and not what any one utility charges.</p>
<div class="pw" data-reveal>{card("residential", "HOUSEHOLDS")}{card("commercial", "BUSINESSES")}{card("industrial", "INDUSTRIAL")}</div>
<div data-reveal>
<div class="pwread"><span class="pwread-m">{esc(month_name(pts[-1][0]))}</span>
<span class="pwread-v"><b>{vals[-1]:.2f}</b> cents per kilowatthour, households</span></div>
{spark}
<div class="pwaxis"><span>{esc(month_name(pts[0][0]))}</span><span>{esc(month_name(pts[-1][0]))}</span></div>
</div>
<p class="pwnote" data-reveal>{esc(res["latest_label"])} is the most recent month EIA has
published, out of {esc(gw.count(res["points"], "month"))} going back to
{esc(month_name(res["first_period"]))}. The line is every month it has published for
households since {esc(month_name(pts[0][0]))}, each one placed on its own date. Touch it, point
at it, or tab to it and use the arrow keys, to read any month exactly. This page states what
the number did and never why, because the data can't say why, and it publishes no figure for a
month that hasn't happened.</p>
<p class="pwnote" data-reveal>The decisions behind Alaska's grid are tracked on
<a class="proselink" href="../docket/">the Alaska AI Docket</a>.</p>"""


def month_name(period):
    """202605 becomes May 2026."""
    m = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]
    return f"{m[int(period[4:6]) - 1]} {period[:4]}"


def numerals():
    """Every numeral the power section may legally print, derived from the file.

    The power section now lives on the gas watch page, whose numeral lint
    refuses any figure that traces back to nothing. That lint is the reason no
    typed number has ever reached that page, and the honest way to bring a
    second dataset under it is to authorise the SECOND DATASET, not to widen the
    rule. So this renders power.json exactly the way the section renders it and
    hands the lint the result. A price the collector measured passes. A price
    somebody typed into the copy does not, which is the whole point.

    Mirrors gaswatch_build.display_numerals(), including its reason for
    existing: the figures the page draws are not the figures the summary holds,
    and the ones the page draws are the ones a reader reads.
    """
    d = load()
    if not d:
        return []
    out = []
    for s in (d.get("sectors") or {}).values():
        pts = s.get("data") or []
        out += [f"{s['latest']:.2f}", str(s.get("points", "")),
                month_name(s["latest_period"]), month_name(s["first_period"])]
        if s.get("change_year") is not None:
            out.append(f"{abs(s['change_year']):.2f}")
        # Only the window the line actually draws. Authorising all 303 months
        # would let any figure in a twenty five year series stand in for a
        # mistyped one in the ten the reader can see.
        for p, v in list(reversed(pts))[-SPARK_MONTHS:]:
            out += [f"{v:.2f}", month_name(p)]
    out.append(str(SPARK_MONTHS))
    return out


def self_test():
    """The renderer and the lint authorisation have to agree, or the page they
    build together goes red on correct data."""
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    d = load()
    if not d:
        print("no ledger/power.json in this checkout, nothing to test")
        return 0

    page = html(None)
    allowed = set(gw.tokens(" ".join(numerals())))
    print("every numeral it draws is one the collector measured")
    planted = [t for t in gw.numeral_lint(page, allowed)]
    check("the panel's own prose passes its own lint", not planted,
          str(sorted(set(planted))[:6]))

    print("and a number nobody measured does not")
    faked = page.replace("cents per kilowatthour", "cents per kilowatthour, up 99.97", 1)
    check("a typed figure is caught", "99.97" in gw.numeral_lint(faked, allowed))

    print("it draws what the file holds")
    res = d["sectors"]["residential"]
    check("the latest month reaches the readout", res["latest_label"] in page,
          res["latest_label"])
    check(f"one hit target per reading, up to {SPARK_MONTHS}",
          page.count('class="pwhit"') == min(SPARK_MONTHS, len(res["data"])),
          str(page.count('class="pwhit"')))
    check("exactly one keyboard stop", page.count('tabindex="0"') == 1)
    check("every target names its month and its price",
          page.count("cents per kilowatthour\"/>") == page.count('class="pwhit"'))

    print("it states a measurement and refuses everything else")
    # Whitespace normalised, because the copy is wrapped at the source and a
    # sentence this test looks for straddles a newline in the file.
    import re
    flat = re.sub(r"\s+", " ", page)
    low = flat.lower()
    for word in ("forecast", "predict", "expected", "will rise", "will fall",
                 "because of", "driven by", "caused"):
        check(f"the panel never says {word}", word not in low)
    check("it says whose number it is", "Energy Information Administration" in flat)
    check("it says the number is a state average",
          "one number for the whole state" in flat)

    print("house voice")
    check("no 'cannot' anywhere in it", "cannot" not in low)
    check("no em or en dash", "\u2014" not in page and "\u2013" not in page)

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--self-test":
        print(f"usage: {os.path.basename(__file__)} [--self-test]", file=sys.stderr)
        sys.exit(2)
    sys.exit(self_test())
