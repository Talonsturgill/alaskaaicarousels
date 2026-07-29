#!/usr/bin/env python3
"""docket_build.py builds the public Alaska AI Docket site from ledger/docket.json.

The daily routine runs this in Phase 11 (ship) after Phase 3.5 updates the
ledger; docs/ is committed with the run and GitHub Pages serves it. The
script is also the ledger's lint gate: it validates every item against the
schema, checks every date parses, and refuses to emit a page containing
banned punctuation (em or en dashes, curly quotes, emoji).

Design: the site carries the studio's deck language to the web. Dark
arctic night, an aurora that actually drifts, the glowing Alaska
coastline as the hero, door glyphs for the four-rooms access model, gold
reserved for open doors and deadlines, grain over everything. Zero
dependencies, one HTML file, fast.

  python scripts/docket_build.py --date 2026-07-09 [--out docs]

Exit 0 on success, 1 on any validation failure.
"""

import argparse
import base64
import io
import json
import math
import random
import re
import sys
from datetime import date as ddate
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_DOMAIN = "alaskaaihq.com"
DEFAULT_SITE = f"https://{DEFAULT_DOMAIN}"

KINDS = {"state-land-lease", "federal-lease", "utility-decision", "legislation",
         "regulatory-docket", "procurement", "grant", "other"}
STATUSES = {"open-for-comment", "pending-decision", "decided", "closed", "watching"}
ACCESS = {"open", "indirect", "closed"}
DATE_KINDS = {"deadline", "vote", "decision", "milestone"}

ACCESS_LABEL = {"open": "OPEN TO YOU", "indirect": "INDIRECT", "closed": "CLOSED"}
STATUS_LABEL = {"open-for-comment": "Open for comment", "pending-decision": "Pending decision",
                "decided": "Decided", "closed": "Closed", "watching": "Watching"}
KIND_LABEL = {"state-land-lease": "State land lease", "federal-lease": "Federal lease",
              "utility-decision": "Utility decision", "legislation": "Legislation",
              "regulatory-docket": "Regulatory docket", "procurement": "Procurement",
              "grant": "Grant", "other": "Decision"}
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

BANNED = re.compile("[–—‘’“”]|[\U0001F000-\U0001FAFF]")


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_date(s, ctx):
    try:
        return ddate.fromisoformat(s)
    except Exception:
        fail(f"{ctx}: bad date {s!r}")


def mon_day(s):
    d = ddate.fromisoformat(s)
    return f"{MONTHS[d.month - 1]} {d.day}"


def validate(items):
    seen = set()
    for it in items:
        i = it.get("id", "<missing id>")
        if i in seen:
            fail(f"duplicate id {i}")
        seen.add(i)
        for field in ("id", "title", "kind", "status", "decider", "public_access",
                      "access_note", "summary", "key_dates", "sources",
                      "first_seen", "last_updated", "history"):
            if field not in it:
                fail(f"{i}: missing {field}")
        if it["kind"] not in KINDS:
            fail(f"{i}: bad kind {it['kind']}")
        if it["status"] not in STATUSES:
            fail(f"{i}: bad status {it['status']}")
        if it["public_access"] not in ACCESS:
            fail(f"{i}: bad public_access {it['public_access']}")
        if not it["sources"]:
            fail(f"{i}: needs at least one source")
        for s in it["sources"]:
            if not s.get("url", "").startswith("http"):
                fail(f"{i}: source without a real url")
        for d in it["key_dates"]:
            parse_date(d["date"], i)
            if d.get("kind") not in DATE_KINDS:
                fail(f"{i}: key_date kind {d.get('kind')!r}")
        parse_date(it["first_seen"], i)
        parse_date(it["last_updated"], i)


# ---------- dates have roles ----------
#
# An item's key_dates are not a bag of timestamps. On 2026-07-21 Phase 3.5
# added the Houston City Council's August 13 vote to the AIDEA item, whose own
# DNR comment window closes August 19. Every surface picked the soonest
# upcoming date of any kind, so a different body's vote on a different question
# won the slot and the page shipped a gold button reading COMMENT NOW, CLOSES
# AUG 13 while the entry's own prose, rail and change notes all said August 19.
# A reader who trusted the button would have believed the window shut six days
# early, on the one publication whose entire product is when it lands and
# whether you get a say.
#
# The schema already carried the answer. kind is the role:
#
#   deadline   the reader must act by this date. This and only this can fill
#              a comment-closes slot.
#   vote       a body votes. May be a DIFFERENT body than this item's decider.
#   decision   the deciding body rules.
#   milestone  context. Never actionable.
#
# So there is no schema change here. The bug was that the selector ignored the
# field the schema already had.

ACTION_KINDS = {"deadline"}
# How a date reads on a chip when it is not an action deadline. "by" is
# deadline language and is reserved for one.
ROLE_PREFIX = {"deadline": "by", "vote": "vote", "decision": "decision",
               "milestone": "next"}


def _future(it, today, kinds=None):
    up = [d for d in it["key_dates"]
          if parse_date(d["date"], it["id"]) >= today
          and (kinds is None or d["kind"] in kinds)]
    up.sort(key=lambda d: d["date"])
    return up[0] if up else None


def next_event(it, today):
    """The soonest upcoming date of ANY kind. A true statement about when this
    item next moves, and a safe sort key. NOT a deadline, and never to be
    rendered with deadline language. See resolve()."""
    return _future(it, today)


# next_date is the name this selector shipped under. It read as "this item's
# date", every surface believed that, and that reading is what put another
# body's vote behind a COMMENT NOW button. Kept as an alias so nothing breaks,
# but new code should say which of the two it means.
next_date = next_event


def action_deadline(it, today):
    """The deadline for the action THIS item asks the reader to take, or None.
    Rule 3: None means render no date. Never fall back to a nearby one."""
    return _future(it, today, ACTION_KINDS)


def had_action_deadline(it):
    """True when an action deadline was ever recorded, whether or not it has
    passed. Distinguishes an expired window (degrade, the site must not keep
    soliciting comment) from one whose close date was never published
    (keep the call to action, show no date)."""
    return any(d["kind"] in ACTION_KINDS for d in it["key_dates"])


def resolve(it, today):
    """The single resolved value per role for one item. Every surface reads
    this and nothing else, so the badge, the header, the closing-soon strip,
    the call to action, the homepage and the subscriber email cannot drift
    apart (rule 5). Returns:

      deadline   the action deadline, or None
      event      the soonest upcoming date of any kind, or None
      headline   what this item's chrome shows: the action deadline when it
                 has one, else the next event, honestly prefixed
      access     effective public access
      status     effective status
      expired    the action deadline is in the past
      cta        whether an action call to action may render at all
    """
    dl = action_deadline(it, today)
    ev = next_event(it, today)
    access, status = it["public_access"], it["status"]

    # Rule 4: status follows the deadline, automatically. A published close
    # date that has passed means no comment path exists NOW, which is exactly
    # what public_access closed means under this repo's four-rooms model. The
    # ledger keeps saying open-for-comment until Phase 3.5 next runs; the page
    # stops saying it the morning the window shuts, with nobody in the loop.
    # This is the same shape a human recorded by hand for the STAK lease once
    # its window closed: pending-decision, closed.
    expired = status == "open-for-comment" and had_action_deadline(it) and dl is None
    if expired:
        access, status = "closed", "pending-decision"

    open_now = access == "open" and status == "open-for-comment"
    return {
        "deadline": dl,
        "event": ev,
        "headline": dl or ev,
        "access": access,
        "status": status,
        "expired": expired,
        # Rule 3: an open window whose close date was never published still
        # deserves its call to action. It just does not get a date.
        "cta": open_now and bool(it["sources"]),
    }


def chip_html(r):
    """The date chip. Its prefix comes from the role of the date it shows, so
    "by" can never again be stuck on another body's vote."""
    d = r["headline"]
    if not d:
        return f'<span class="chip" style="color:var(--mute)">{esc(STATUS_LABEL[r["status"]])}</span>'
    return (f'<span class="chip days" data-date="{d["date"]}">'
            f'{ROLE_PREFIX[d["kind"]]} {mon_day(d["date"])}</span>')


def nearest_headline(items, today):
    """The docket-wide NEXT DATE stat. It reads the same resolved headline the
    closing-soon cards read, so the page header and the marquee card cannot
    disagree (rule 5). This understates by design: on 2026-07-29 it shows the
    AIDEA comment close, AUG 19, and not the Houston City Council's AUG 13
    vote, which is genuinely sooner but is a different body on a different
    question and is not what this page is asking anyone to act on. That vote
    stays fully visible on its item's timeline rail."""
    ds = sorted((d for d in (resolve(it, today)["headline"] for it in items) if d),
                key=lambda d: d["date"])
    return ds[0] if ds else None


def open_count(items, today):
    """How many doors are open RIGHT NOW, not how many the ledger last said
    were open. Counts the resolved access so the stat drops the morning a
    comment window shuts."""
    return sum(1 for it in items if resolve(it, today)["access"] == "open")


def _decolon(text):
    """Remove colons from prose the way prose_colon_gate counts them.

    The gate exempts exactly two things, clock times and URLs, then fails the
    build on any colon left over. Replacing ": " was not the same rule: copy
    like "SB 250:the vote" or a bare "Note:x" sailed through and took the
    nightly ship down with sys.exit(1) at the gate. Match the gate's own
    exemptions instead of approximating them."""
    keep = re.compile(r"https?://\S+|\d{1,2}:\d{2}")
    out, at = [], 0
    for m in keep.finditer(text):
        out.append(re.sub(r"\s*:\s*", ", ", text[at:m.start()]))
        out.append(m.group(0))
        at = m.end()
    out.append(re.sub(r"\s*:\s*", ", ", text[at:]))
    return "".join(out)

def house(text):
    """House style, applied to text this generator pulls out of a run.

    Slide copy is written to the house rules, but claims.json quotes sources
    verbatim and a source is free to use an em dash and curly quotes. Those
    would fail the punctuation gate and take the whole build down, so they are
    normalized here rather than left to break a ship at midnight."""
    if not text:
        return ""
    for bad, good in (("—", ", "), ("–", ", "),
                      ("‘", "'"), ("’", "'"),
                      ("“", '"'), ("”", '"')):
        text = text.replace(bad, good)
    text = BANNED.sub("", text)                 # anything left (emoji) goes
    text = " ".join(_decolon(text).split())
    # A dash sitting between spaces leaves "a , b" once it becomes a comma.
    text = re.sub(r"\s+([,.;])", r"\1", text)
    return text.rstrip(" ,:")

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


# ---------- grain tile (seeded, like AK.grainTile) ----------

def grain_data_uri(size=110, strength=26, seed=11):
    try:
        from PIL import Image
    except ImportError:
        return ""
    rng = random.Random(seed)
    im = Image.new("L", (size, size))
    im.putdata([128 + rng.randint(-strength, strength) for _ in range(size * size)])
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------- Alaska map (Albers equal-area conic, the house projection) ----------

def albers(lon, lat, lon0=-154.0, p1=55.0, p2=65.0, lat0=63.0):
    rad = math.radians
    n = (math.sin(rad(p1)) + math.sin(rad(p2))) / 2.0
    C = math.cos(rad(p1)) ** 2 + 2.0 * n * math.sin(rad(p1))
    rho0 = math.sqrt(C - 2.0 * n * math.sin(rad(lat0))) / n
    rho = math.sqrt(max(0.0, C - 2.0 * n * math.sin(rad(lat)))) / n
    dlon = ((lon - lon0 + 540.0) % 360.0) - 180.0
    th = n * rad(dlon)
    return rho * math.sin(th), rho0 - rho * math.cos(th)


def alaska_paths(max_points=3000, keep_rings=16):
    geo = json.loads((REPO / "assets/geo/alaska-state.geo.json").read_text())
    g = geo["features"][0]["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings = sorted((r[0] for r in polys), key=len, reverse=True)[:keep_rings]
    total = sum(len(r) for r in rings)
    step = max(1, total // max_points)
    out = []
    for r in rings:
        pts = [albers(lon, lat) for lon, lat in r[::step]]
        if len(pts) >= 8:
            out.append(pts)
    return out


def graticule_paths(lon_step=10, lat_step=5):
    paths = []
    for lon in range(-180, -125, lon_step):
        paths.append([albers(lon, lat / 2.0) for lat in range(102, 145)])
    for lat in range(50, 75, lat_step):
        paths.append([albers(lon / 2.0, lat) for lon in range(-360, -249, 2)])
    return paths


def fit_transform(paths, w, h, pad):
    xs = [p[0] for path in paths for p in path]
    ys = [p[1] for path in paths for p in path]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min((w - 2 * pad) / (x1 - x0), (h - 2 * pad) / (y1 - y0))
    ox = (w - (x1 - x0) * s) / 2.0
    oy = (h - (y1 - y0) * s) / 2.0
    def T(p):
        return ((p[0] - x0) * s + ox, h - ((p[1] - y0) * s + oy))
    return T


def path_d(paths, T, close=True):
    z = " Z" if close else ""
    return " ".join(
        "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (T(p) for p in path)) + z
        for path in paths)


PIN_COLOR = {"open": "#3ce6b4", "indirect": "#8da2be", "closed": "#f2a43a"}

# The transmission backbone, drawn under the pins. Almost every decision on this
# docket is really a decision about this grid, so without it the pins look like
# a coincidence: four of them cluster on the Railbelt because that is where the
# power is, and the map should say so rather than leave the reader to know it.
#
# Three weights, because the difference between a 69 kV line and the 230 kV
# Anchorage ring is the difference between serving a town and carrying a load.
GRID_TIERS = [("t1", 69.0, 138.0), ("t2", 138.0, 230.0), ("t3", 230.0, 1e9)]


LAYER_FILES = {
    "grid": "ak-transmission-69kv.geo.json",
    "gen": "ak-generation-20mw.geo.json",
    "taps": "ak-taps.geo.json",
}


@lru_cache(maxsize=None)
def layer_data(name):
    """A layer's asset, or None. Cached: one build asked for the same three
    files seven times, parsing each from disk on every call. A missing context layer must never break the
    docket, so every caller treats absence as "do not draw and do not offer"."""
    src = REPO / "assets/geo" / LAYER_FILES[name]
    if not src.exists():
        return None
    try:
        return json.loads(src.read_text())
    except (ValueError, OSError):
        return None


def available_layers():
    """Which layers can actually be drawn. The page asks before it offers a
    toggle for something that would not appear."""
    return [k for k in ("grid", "gen", "taps") if layer_data(k)]


def _polyline(segs, T):
    return " ".join("M" + " L".join("%.1f,%.1f" % T(albers(x, y)) for x, y in seg)
                    for seg in segs if len(seg) >= 2)


def grid_paths(T):
    """Transmission projected through the map's own transform, split into voltage
    tiers so weight can carry voltage."""
    d = layer_data("grid")
    if not d:
        return []
    lines = d.get("lines", [])
    out = []
    for tier, lo, hi in GRID_TIERS:
        segs = [L["pts"] for L in lines if lo <= L.get("kv", 0) < hi]
        if segs:
            out.append((tier, _polyline(segs, T)))
    return out


def taps_path(T):
    d = layer_data("taps")
    return _polyline(d.get("lines", []), T) if d else ""


def generation_marks(T):
    """Plants as circles with area proportional to nameplate capacity, which is
    the honest encoding: doubling the megawatts doubles the ink, where doubling
    the radius would quadruple it and overstate the big plants.

    Floored at 3.2 so the smallest kept plant is still a target a thumb can hit
    on a phone, since most readers are on one."""
    d = layer_data("gen")
    if not d:
        return ""
    out = []
    for p in d.get("plants", []):
        x, y = T(albers(p["at"][0], p["at"][1]))
        # Scaled so the biggest plant in Alaska, Sullivan at 309 MW, lands near
        # 16px rather than 24. At 24 the Cook Inlet plants merged into one beige
        # mass that swallowed two pins, which is the opposite of informative.
        r = max(2.8, 0.92 * math.sqrt(p.get("mw", 0)))
        out.append('<g class="mk" data-x="%.1f" data-y="%.1f" transform="translate(%.1f,%.1f)">'
                   '<circle class="gen" cx="0" cy="0" r="%.1f"><title>%s, %g MW, %s</title>'
                   '</circle></g>'
                   % (x, y, x, y, r, esc(p.get("n", "")), p.get("mw", 0), esc(p.get("src", ""))))
    return "".join(out)


def map_svg(ordered_items, today=None, w=1000, h=620):
    located = [(n, it) for n, it in enumerate(ordered_items, 1) if it.get("location")]
    coast = alaska_paths()
    T = fit_transform(coast, w, h, 44)
    coast_d = path_d(coast, T)
    grat_d = path_d(graticule_paths(), T, close=False)

    # THE DOT NEVER MOVES. It sits on the projected coordinate and nothing is
    # allowed to nudge it, because a pin that has drifted for the sake of tidy
    # spacing is a map telling a small lie. Only the LABEL is placed for
    # legibility, and any label that had to move is tethered to its dot by a
    # visible line, which is how a paper atlas has always handled this.
    #
    # What this replaced: a relaxation pass that pushed every pin apart to a
    # 34px floor. At this scale 1px is about 3.7 km, so that floor was 125 km.
    # Two docket items sharing one coordinate ended up drawn 78 miles apart.
    anchors = [T(albers(it["location"]["lon"], it["location"]["lat"])) for _, it in located]

    # Items at one coordinate are ONE place, so they get one dot carrying every
    # number, rather than being spread out to look like several places.
    groups = []   # (x, y, [(n, item), ...])
    for (n, it), (x, y) in zip(located, anchors):
        for g in groups:
            if math.hypot(g[0] - x, g[1] - y) < 2.0:
                g[2].append((n, it))
                break
        else:
            groups.append((x, y, [(n, it)]))

    # Label placement. Width comes from how many numbers the badge carries.
    def badge_w(g):
        return 28.0 if len(g[2]) == 1 else 20.0 + 15.0 * len(g[2])
    # A displaced label has to clear its own dot, or the badge covers the dot and
    # the tether it is meant to disclose, and the reader is back to trusting a
    # badge that has quietly moved. LEAD_MIN is measured from the dot, so at a
    # badge radius of 14 there is always visible tether between the two.
    LEAD_MIN = 27.0
    labels = [[g[0], g[1]] for g in groups]
    for _ in range(12):
        for _ in range(40):                       # push labels off each other
            moved = False
            for a in range(len(groups)):
                for b in range(a + 1, len(groups)):
                    need = (badge_w(groups[a]) + badge_w(groups[b])) / 2.0 + 6.0
                    dx = labels[b][0] - labels[a][0]; dy = labels[b][1] - labels[a][1]
                    dist = max(0.001, math.hypot(dx, dy))
                    if dist < need:
                        push = (need - dist) / 2.0
                        ux, uy = dx / dist, dy / dist
                        if abs(dx) < 1 and abs(dy) < 1: ux, uy = 0.0, 1.0
                        labels[a][0] -= ux * push; labels[a][1] -= uy * push
                        labels[b][0] += ux * push; labels[b][1] += uy * push
                        moved = True
            if not moved:
                break
        # then push any label that moved at all out far enough to be readable
        for i, g in enumerate(groups):
            dx = labels[i][0] - g[0]; dy = labels[i][1] - g[1]
            dist = math.hypot(dx, dy)
            if 0.5 < dist < LEAD_MIN:
                ux, uy = dx / dist, dy / dist
                labels[i][0] = g[0] + ux * LEAD_MIN
                labels[i][1] = g[1] + uy * LEAD_MIN

    # Three layers, because a dot hidden under a NEIGHBOUR's badge is just as
    # useless as one hidden under its own. Tethers at the back, badges over
    # them, and the dots last so nothing can ever cover the one mark on this
    # map that is telling the literal truth about where something is.
    #
    # Every mark is emitted as a MARKER: a <g class="mk"> that carries its map
    # coordinate in data-x and data-y and draws its contents around its own
    # origin. Geometry lives in a separate group that the zoom scales, markers
    # get repositioned instead of resized. Without that, fitting the view to the
    # pins on a phone would blow the badges up to the size of boroughs, and on a
    # 390px screen the marks also have to be scaled UP rather than down.
    #
    # With no script the transform below is already the correct unzoomed
    # position, so the map is complete and clickable before anything runs.
    def mk(layer, x, y, body, cls=""):
        layer.append(f'<g class="mk{(" " + cls) if cls else ""}" data-x="{x:.1f}" '
                     f'data-y="{y:.1f}" transform="translate({x:.1f},{y:.1f})">{body}</g>')

    # A pulsing pin promises the reader a comment window is open RIGHT NOW, so
    # it reads the resolved access, not the ledger's. Without today it cannot
    # resolve and falls back to the stored value.
    def acc(it):
        return resolve(it, today)["access"] if today else it["public_access"]

    leads, badges, dots = [], [], []
    for g, (lx, ly) in zip(groups, labels):
        ax, ay, members = g
        first = members[0][1]
        c = PIN_COLOR[acc(first)]
        ox, oy = lx - ax, ly - ay          # badge offset, constant in screen units
        # The status classes ride on the tether and the dot as well as the badge,
        # so a filter that dims a pin dims the whole mark rather than leaving an
        # orphan dot and a line pointing at nothing.
        acls = "pinmk " + " ".join(sorted({"a-" + acc(it) for _, it in members}))
        # Any member being open earns the pulse, so a live decision still reads
        # as live when it shares a coordinate with a settled one.
        if any(acc(it) == "open" for _, it in members):
            mk(leads, ax, ay,
               f'<circle cx="0" cy="0" r="8" fill="none" stroke="{PIN_COLOR["open"]}" '
               f'stroke-width="1.6" opacity="0.8">'
               f'<animate attributeName="r" values="8;26" dur="2.8s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="0.8;0" dur="2.8s" repeatCount="indefinite"/>'
               f'</circle>', cls=acls)
        # The tether and the dot exist only when the label had to move. An
        # undisplaced badge is already sitting on the coordinate, so a dot under
        # it would just collide with its own number.
        if math.hypot(ox, oy) > 3.0:
            mk(leads, ax, ay, f'<line class="pinlead" x1="0" y1="0" x2="{ox:.1f}" '
                              f'y2="{oy:.1f}" stroke="{c}"/>', cls=acls)
            mk(dots, ax, ay, f'<circle class="pindot" cx="0" cy="0" r="3.4" fill="{c}"/>', cls=acls)
        if len(members) == 1:
            n, it = members[0]
            body = (f'<a href="#{esc(it["id"])}" aria-label="{esc(it["title"])}">'
                    f'<circle class="pinbadge" cx="{ox:.0f}" cy="{oy:.0f}" r="14" fill="#050b16" '
                    f'stroke="{c}" stroke-width="2.6"/><text x="{ox:.0f}" y="{oy + 5:.0f}" '
                    f'text-anchor="middle" class="pinnum" fill="{c}">{n}</text></a>')
            mk(badges, ax, ay, body, cls=acls)
        else:
            bw = badge_w(g)
            x0 = ox - bw / 2.0
            parts = [f'<rect x="{x0:.0f}" y="{oy - 14:.0f}" width="{bw:.0f}" height="28" rx="14" '
                     f'fill="#050b16" stroke="{c}" stroke-width="2.6"/>',
                     # No colon and no item titles in here. This is visible prose to
                     # the build's colon gate, and a title can carry a colon of its own.
                     f'<title>{len(members)} decisions at '
                     f'{esc(first["location"]["name"])}</title>']
            for i, (n, it) in enumerate(members):
                tx = x0 + 10.0 + 15.0 * i + 7.5
                parts.append(
                    f'<a href="#{esc(it["id"])}" aria-label="{esc(it["title"])}">'
                    f'<text x="{tx:.0f}" y="{oy + 5:.0f}" text-anchor="middle" class="pinnum" '
                    f'fill="{PIN_COLOR[acc(it)]}">{n}</text></a>')
            mk(badges, ax, ay, "".join(parts), cls=acls)
    pins = leads + badges + dots
    grid = "".join(f'<path class="gx gx-{tier}" d="{d}"/>' for tier, d in grid_paths(T))
    _taps_d = taps_path(T)
    taps = f'<path class="tp" d="{_taps_d}"/>' if _taps_d else ""
    gen = generation_marks(T)
    caption = "".join(
        f'<a class="mapkey" href="#{esc(it["id"])}"><b class="k-{acc(it)}">{n}</b>'
        f'<span>{esc(it["location"]["name"])}</span></a>'
        for n, it in located)
    svg = f"""<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Map of Alaska with every tracked decision pinned">
<defs>
  <filter id="coastglow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <radialGradient id="landfill" cx="60%" cy="30%" r="90%">
    <stop offset="0%" stop-color="#0d2038"/><stop offset="100%" stop-color="#081426"/>
  </radialGradient>
</defs>
<g id="mzoom">
  <path d="{grat_d}" fill="none" stroke="rgba(110,165,255,0.07)" stroke-width="1"/>
  <path class="coast" d="{coast_d}" fill="url(#landfill)" stroke="#5ac8f0" stroke-width="1.5" filter="url(#coastglow)"/>
  <g class="lyr lyr-taps" aria-hidden="true">{taps}</g>
  <g class="lyr lyr-grid" aria-hidden="true">{grid}</g>
</g>
<g class="lyr lyr-gen">{gen}</g>
{''.join(pins)}
</svg>"""
    return svg, caption


# ---------- door glyphs (the four rooms, from slide 8) ----------

def door_svg(access):
    if access == "open":
        return """<svg class="door" viewBox="0 0 44 56" aria-hidden="true">
<polygon points="30,6 44,50 10,46" fill="rgba(255,199,44,0.13)"/>
<rect x="7" y="4" width="26" height="48" rx="2" fill="none" stroke="#ffc72c" stroke-width="2.4"/>
<polygon points="9,6 22,12 22,48 9,50" fill="#12233a" stroke="#ffc72c" stroke-width="1.6"/>
<rect x="24" y="12" width="7" height="36" fill="#ffda6e" opacity="0.55"/>
</svg>"""
    if access == "closed":
        return """<svg class="door" viewBox="0 0 44 56" aria-hidden="true">
<rect x="7" y="4" width="26" height="48" rx="2" fill="none" stroke="#f2a43a" stroke-width="2"/>
<rect x="10" y="7" width="20" height="42" fill="#141311" stroke="#8a6030" stroke-width="1.2"/>
<circle cx="26" cy="30" r="2" fill="#f2a43a"/>
<line x1="7" y1="4" x2="33" y2="52" stroke="#f2a43a" stroke-width="1.2" opacity="0.5"/>
</svg>"""
    return """<svg class="door" viewBox="0 0 44 56" aria-hidden="true">
<rect x="7" y="4" width="26" height="48" rx="2" fill="none" stroke="#8da2be" stroke-width="2"/>
<rect x="10" y="7" width="20" height="42" fill="#0c1c30" stroke="#3a5f84" stroke-width="1.2"/>
<circle cx="26" cy="30" r="2" fill="#8da2be"/>
</svg>"""


# ---------- page assembly ----------

def rail_html(it, today):
    stops = []
    dates = sorted(it["key_dates"], key=lambda x: x["date"])
    all_past = all(parse_date(d["date"], it["id"]) < today for d in dates)
    today_placed = all_past  # if all past, TODAY caps the rail at the end
    for d in dates:
        dd = parse_date(d["date"], it["id"])
        cls = "future" if dd >= today else "past"
        if d["kind"] in ("deadline", "vote"):
            cls += " hard"
        if not today_placed and dd >= today:
            stops.append('<div class="stop now" aria-hidden="true"><span class="dot"></span>'
                         '<span class="d">TODAY</span></div>')
            today_placed = True
        stops.append(
            f'<div class="stop {cls}"><span class="dot"></span>'
            f'<span class="d">{mon_day(d["date"])}</span>'
            f'<span class="l">{esc(d["label"])}</span></div>')
    if dates and all_past:
        stops.append('<div class="stop now" aria-hidden="true"><span class="dot"></span>'
                     '<span class="d">TODAY</span></div>')
    solo = ' solo' if len(stops) == 1 else ''
    return f'<div class="rail{solo}">{"".join(stops)}</div>'


def item_html(it, today, num, prefix=""):
    """One docket entry. `prefix` is the path from the rendering page to
    /docket/, so the entry can link to that decision's own canonical page.
    Empty on the docket page itself, which already sits at /docket/."""
    r = resolve(it, today)
    chip = chip_html(r)
    srcs = " &middot; ".join(
        f'<a href="{esc(s["url"])}" rel="noopener">{esc(s["outlet"])}</a>' for s in it["sources"])
    hist = it["history"][-1] if it["history"] else None
    hist_html = (f'<div class="hist">{esc(hist["date"])} &middot; {esc(hist["note"])}</div>' if hist else "")
    act = ""
    if r["cta"]:
        # Rule 2: this label reads its own action's deadline and nothing else.
        # Rule 3: no deadline, no date. A call to action with no date is fine;
        # one with a confident wrong date is the thing being fixed here.
        when = (f' &middot; CLOSES {mon_day(r["deadline"]["date"]).upper()}'
                if r["deadline"] else "")
        act = (f'<div class="ctarow act"><a class="cta gold sm" href="{esc(it["sources"][0]["url"])}" '
               f'rel="noopener">COMMENT NOW{when}</a></div>')
    return f"""<article class="item a-{r["access"]}" id="{esc(it["id"])}" data-reveal>
  <div class="doorcol">{door_svg(r["access"])}<span class="num">{num:02d}</span></div>
  <div class="body">
    <div class="top">
      <span class="badge b-{r["access"]}">{ACCESS_LABEL[r["access"]]}</span>
      <span class="chip kind">{esc(KIND_LABEL[it["kind"]]).upper()}</span>
      {chip}
    </div>
    <h3><a class="proselink" href="{prefix}{esc(it["id"])}/">{esc(it["title"])}</a></h3>
    <div class="who">DECIDES &middot; {esc(it["decider"]).upper()}</div>
    <p>{esc(it["summary"])}</p>
    <div class="access">{esc(it["access_note"])}</div>
    {rail_html(it, today)}
    {act}
    <div class="srcs">Sources &middot; {srcs}</div>
    {hist_html}
    <div class="ctarow"><a class="cta ghost sm" href="{prefix}{esc(it["id"])}/">
      THE FULL RECORD ON THIS DECISION</a></div>
  </div>
</article>"""


def card_html(it, today, prefix=""):
    r = resolve(it, today)
    d = r["headline"]
    # Rule 3 again: with no resolved date the card keeps its headline and its
    # status and simply carries no date, rather than borrowing a nearby one.
    when = (f'<div class="big" data-days="{d["date"]}">{mon_day(d["date"])}</div>'
            f'<div class="when chip days" data-date="{d["date"]}">'
            f'{ROLE_PREFIX[d["kind"]]} {mon_day(d["date"])}</div>') if d else ""
    who = esc(d["label"]).upper() if d else esc(STATUS_LABEL[r["status"]]).upper()
    return f"""<a class="card a-{r["access"]}" href="{prefix}#{esc(it["id"])}" data-reveal>
  <div class="cardtop"><span class="badge b-{r["access"]}">{ACCESS_LABEL[r["access"]]}</span></div>
  {when}
  <h3>{esc(it["title"])}</h3>
  <div class="who">{who}</div>
</a>"""




POLARIS = ('<svg class="polaris" viewBox="-10 -10 20 20" aria-hidden="true">'
           '<path d="M0,-9 L2.2,-2.2 L9,0 L2.2,2.2 L0,9 L-2.2,2.2 L-9,0 L-2.2,-2.2 Z" fill="#ffc72c"/></svg>')




def main():
    # This module is the shared library: projection, date roles, docket
    # components, house style and the gates. It builds no page of its own.
    # The retired single-page build() lived here with its own CSS and JS,
    # 290 lines forked from the live ones and drifted, so a maintainer could
    # edit the wrong stylesheet and change nothing on the site. Deleted; the
    # CLI has delegated to site_build since, and still does.
    import site_build
    site_build.main()


if __name__ == "__main__":
    main()
