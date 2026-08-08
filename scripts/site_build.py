#!/usr/bin/env python3
"""site_build.py builds the whole Alaska AI site into docs/ (GitHub Pages).

Pages: / (home), /docket/ (the tracker), /archive/ (every shipped deck),
/archive/<date>/ (deck detail with a swipeable gallery), /about/. Plus
sitemap.xml, robots.txt, and the public data feed docket.json (kept at the
root AND under /docket/ so shared links never break). /videos/ (the
Dispatch video feed) is NOT generated: docs/videos/index.html is a static
passthrough preserved verbatim, and docs/videos/videos.json is data owned
by publish_feed.py in the alaska-ai-weekly repo; the build only emits the
nav link and the sitemap entry for it.

Data in: ledger/docket.json (tracker), runs/<date>/ (shipped decks: copy,
caption, reports; slide images referenced from raw.githubusercontent so
the site stays light). The daily routine runs this in Phase 11; docs/ is
committed with the run and Pages republishes on merge.

House gates carried over from docket_build: schema validation, date
checks, and a banned-punctuation refusal over every emitted page.

Alaskan identity, by design: the hero night sky is the state flag (the
Big Dipper and Polaris in gold), and a daylight telemetry chip computes
Anchorage's hours of daylight for the build date, including whether the
day is growing or shrinking. Flare with taste: CSS scroll-driven reveals
(compositor-only) with an IntersectionObserver fallback, one-line view
transitions between pages, a gold scroll-progress hairline, drifting
aurora, seeded grain. Zero dependencies, static files only.

  python scripts/site_build.py --date 2026-07-09 [--out docs] [--domain d]
"""

import argparse
import json
import math
import re
import sys
from datetime import date as ddate, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docket_build as db  # projection, validation, docket components, gates
import feeds_build as fb   # feeds, plaintext mirrors, llms.txt
import gaswatch_build as gw  # gas watch series, figures, chart, page components

REPO = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/Talonsturgill/alaskaaicarousels/main"

# IndexNow key. Not a secret and not a credential: the protocol's whole security
# model is that only the site owner can put a file at the site's own root, so the
# key is meant to be public and is published at /<key>.txt by this build. It is
# fixed rather than generated because rotating it silently orphans the file the
# search engines already fetched and verified.
INDEXNOW_KEY = "a7f3c21e9b8d4e5f6a1c0b3d2e8f7a94"

# Booking page for the free intro call (Calendly, Cal.com, or a Google
# Calendar appointment page). While empty the services hero keeps its
# form-first buttons; set it and rebuild to lead with the booking button.
# This is the ONLY place the booking URL is written. It renders in several
# spots on the services page and on services/thanks/, so change it here and
# rebuild; never patch the built HTML. The /30min event was dead (2026-08-01).
BOOKING_URL = "https://calendly.com/talon-sturgill-ixzj/new-meeting"

# The public entity. One canonical Organization node, emitted in full on the
# home page and referenced from every other page's JSON-LD through the same
# @id, so Google and the AI answer engines resolve "Alaska AI" to a single
# unambiguous thing instead of four loose fragments. sameAs lists the real
# profiles; add new ones here and rebuild.
# name, profile URL (tracking params stripped), and the standard 24x24 icon path.
SOCIALS = [
    ("LinkedIn", "https://www.linkedin.com/company/alaska-ai/",
     "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 "
     "1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 "
     "3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 "
     "0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 "
     "2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 "
     ".774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 "
     "22.271V1.729C24 .774 23.2 0 22.225 0z"),
    ("TikTok", "https://www.tiktok.com/@alaskaai_",
     "M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 "
     "1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 "
     "2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 "
     "3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 "
     "1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 "
     "4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 "
     "1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"),
    ("YouTube", "https://youtube.com/@alaska_ai",
     "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 "
     "3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 "
     "5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 "
     "9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"
     "M9.545 15.568V8.432L15.818 12l-6.273 3.568z"),
    ("Instagram", "https://www.instagram.com/alaskaai_",
     "M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717"
     "-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 "
     "12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 "
     "2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 "
     "8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 "
     "1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558"
     "-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149"
     "-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c"
     "-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 "
     "4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 "
     "1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 "
     "4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679"
     "-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015"
     "-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421"
     "-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061"
     "-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9"
     "-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65"
     "-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 "
     "6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c"
     "-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 "
     "1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 "
     "1.44.645 1.44 1.439z"),
    ("Facebook", "https://www.facebook.com/share/1GMRTzE1tK/",
     "M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 "
     "11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 "
     "2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 "
     "3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"),
    ("X", "https://x.com/Microvestapp",
     "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 "
     "7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 "
     "3.24H4.298Z"),
]
SAMEAS = [url for _, url, _ in SOCIALS]
ANCHORAGE_GEO = {"@type": "GeoCoordinates", "latitude": 61.2181, "longitude": -149.9003}


def org_id(site_url):
    return f"{site_url}/#org"


def org_ld(site_url):
    """The canonical Alaska AI entity: one node, both hats (the newsroom and
    the studio), with the place, the founder, and the profiles attached."""
    return {
        "@type": ["NewsMediaOrganization", "ProfessionalService"],
        "@id": org_id(site_url),
        "name": "Alaska AI",
        "alternateName": ["Alaska.Ai", "Alaska AI HQ"],
        "url": f"{site_url}/",
        "logo": {"@type": "ImageObject", "url": f"{site_url}/logo.png",
                 "width": 512, "height": 512},
        "image": f"{site_url}/og.png",
        "description": "Alaska AI is the daily publication on Alaska's AI beat and an "
                       "AI studio in Anchorage that builds AI systems for Alaska "
                       "businesses. Every fact verified to its source.",
        "email": "docket@alaskaaihq.com",
        "contactPoint": {"@type": "ContactPoint", "email": "docket@alaskaaihq.com",
                         "contactType": "inquiries"},
        "address": {"@type": "PostalAddress", "addressLocality": "Anchorage",
                    "addressRegion": "AK", "addressCountry": "US"},
        "geo": ANCHORAGE_GEO,
        "areaServed": [
            {"@type": "State", "name": "Alaska"},
            {"@type": "City", "name": "Anchorage"},
            {"@type": "City", "name": "Fairbanks"},
            {"@type": "City", "name": "Juneau"},
        ],
        "founder": {"@type": "Person", "name": "Talon Sturgill",
                    "url": f"{site_url}/about/",
                    "sameAs": ["https://www.linkedin.com/in/talonsturgill"]},
        "sameAs": SAMEAS,
        "knowsAbout": ["artificial intelligence", "Alaska AI infrastructure",
                       "AI for small business", "voice agents", "workflow automation",
                       "AI for tourism", "AI for healthcare",
                       "Alaska Native corporations"],
    }


def breadcrumb_ld(site_url, crumbs):
    """crumbs is a list of (name, path) from the home page down."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "item": f"{site_url}/{path}"}
                for i, (name, path) in enumerate(crumbs)]}


def ld_json(obj):
    """Serialize a JSON-LD block for embedding inside a <script> element.

    json.dumps does not escape <, >, or &, so a run-record title of
    'Robot </script><script>alert(1)//' closed the ld+json element early and
    the browser then parsed the rest as live script. Every value here traces
    to an agent-written run record (title, summary, outlet, article body), so
    this was stored XSS on the origin, and it slipped every gate because the
    injected </script><script> pair balances and the colon gate's own
    tag-stripping regex swallowed the JSON tail.

    Escaping the three HTML-significant characters as their \\uXXXX forms keeps
    the JSON byte-for-byte valid (a JSON string may carry any \\u escape) while
    making it impossible to break out of the script element. This is the
    standard defense; browsers and schema parsers read \\u003c as '<'."""
    return (json.dumps(obj, separators=(",", ":"))
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))

MONTH_FULL = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]

esc = db.esc
# house() and _decolon moved to docket_build so feeds_build can reach
# them too. site_build imports feeds_build, so feeds_build importing
# site_build back would be a cycle; the shared library is the only
# place both can read from.
house = db.house
_decolon = db._decolon


# ---------- Anchorage daylight telemetry (NOAA-style approximation) ----------

def daylight_minutes(d, lat=61.2181):
    n = d.timetuple().tm_yday
    decl = -23.44 * math.cos(math.radians(360.0 / 365.0 * (n + 10)))
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(decl))
    x = max(-1.0, min(1.0, x))
    return 2.0 * math.degrees(math.acos(x)) / 15.0 * 60.0


def daylight_chip(today):
    mins = daylight_minutes(today)
    delta = mins - daylight_minutes(today - timedelta(days=1))
    h, m = int(mins // 60), int(mins % 60)
    trend = "GAINING" if delta >= 0 else "LOSING"
    return (f"ANCHORAGE &middot; {h}H {m:02d}M OF DAYLIGHT &middot; "
            f"{trend} {abs(delta):.0f} MIN A DAY")


# ---------- the flag sky (Big Dipper + Polaris, gold on the night) ----------

# The eight gold stars of the flag, drawn as real stars rather than dots.
#
# Positions are the official flag geometry (1416x1000, handle up-left, the
# bowl's pointer edge aimed at Polaris). Everything else is photometry: each
# star carries its true V magnitude and B-V color index, and the optics follow
# how a bright point source actually images.
#
# Three rules from the astronomy do the heavy lifting:
#   1. A bright core saturates to WHITE whatever the star's color, because all
#      three channels clip. The tint lives in a thin ring just outside it.
#   2. The white core grows only as the square root of the log of brightness,
#      so it is nearly constant across stars. The brightness hierarchy belongs
#      in the halo and the diffraction spikes instead.
#   3. A real point-spread function is Gaussian at the core and a power-law
#      skirt far out, a range no single gradient can hold. Hence the layers:
#      aureole (power law), inner glow (Gaussian), color ring, white core.
# Spikes come from the instrument, not the star, so every star carries a cross
# at the same angle. They are built from a tapered lens path plus a length
# gradient, which costs nothing, instead of a blur.
#
# name, x, y, V mag, B-V, spike tier (1 full, 2 short, 3 shortest)
FLAG_STARS = [
    ("Alkaid",  148, 181, 1.86, -0.19, 1),
    ("Mizar",   215, 206, 2.04, +0.02, 2),
    ("Alioth",  248, 241, 1.77, -0.02, 1),
    ("Megrez",  282, 278, 3.31, +0.075, 3),
    ("Dubhe",   382, 314, 1.79, +1.07, 1),
    ("Phecda",  278, 331, 2.44, -0.013, 2),
    ("Merak",   353, 356, 2.37, -0.02, 2),
    ("Polaris", 520,  96, 1.98, +0.60, 1),
]
# Gold-family tints keyed to B-V. The flag's stars are gold by law and by
# brand, so real stellar color is expressed as temperature WITHIN that gold:
# Alkaid (B3V, the bluest) reads palest, Dubhe (K0III, a genuine orange giant)
# reads amber, Polaris (F7Ib) reads cream. Six of the seven Dipper stars really
# are near-identical in color, so they share one gold. Painting a rainbow is
# what makes constellation art look fake.
FLAG_TINTS = ["#ffdc8c", "#ffc72c", "#ffd875", "#ffa726"]


def _tint_index(bv):
    if bv <= -0.10:
        return 0
    if bv >= 0.90:
        return 3
    return 2 if bv >= 0.35 else 1


def flag_sky():
    # Power-law stop table for the aureole: I(r) = 1/(1+(r/a)^2), the r^-2
    # stellar aureole. Gaussian table for the inner glow. Both measured, not
    # eyeballed, which is what keeps the falloff from looking like a blur.
    au_stops = [(0, 1.0), (3, .80), (6, .50), (12, .20), (20, .083),
                (35, .029), (60, .010), (100, 0)]
    gl_stops = [(0, 1.0), (10, .956), (20, .835), (33, .607), (50, .325),
                (67, .135), (83, .044), (100, 0)]
    defs = []
    for i, c in enumerate(FLAG_TINTS):
        defs.append(
            f'<radialGradient id="fa{i}">'
            + "".join(f'<stop offset="{o}%" stop-color="{c}" stop-opacity="{a:.3f}"/>'
                      for o, a in au_stops) + "</radialGradient>")
        defs.append(
            f'<radialGradient id="fg{i}">'
            + "".join(f'<stop offset="{o}%" stop-color="{c}" stop-opacity="{a:.3f}"/>'
                      for o, a in gl_stops) + "</radialGradient>")
        defs.append(
            f'<radialGradient id="fr{i}">'
            f'<stop offset="0%" stop-color="{c}" stop-opacity=".95"/>'
            f'<stop offset="45%" stop-color="{c}" stop-opacity=".78"/>'
            f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/>'
            "</radialGradient>")
    # The saturated core: white and flat, then off a cliff. Identical for every
    # star, because that is what over-exposure actually does.
    defs.append('<radialGradient id="fcore">'
                '<stop offset="0%" stop-color="#fff" stop-opacity="1"/>'
                '<stop offset="55%" stop-color="#fff" stop-opacity="1"/>'
                '<stop offset="78%" stop-color="#fff" stop-opacity=".65"/>'
                '<stop offset="100%" stop-color="#fff" stop-opacity="0"/>'
                "</radialGradient>")
    # Spike brightness along its length, hot at the middle, gone at the tips,
    # cooling from white core to a warm tip the way a real PSF disperses. Two
    # copies: a gradient runs along the bounding box's x axis, so the vertical
    # needle needs its own or the falloff lands across the width instead of
    # along the length.
    spk_stops = ('<stop offset="0%" stop-color="#fff" stop-opacity="0"/>'
                 '<stop offset="26%" stop-color="#ffe0a4" stop-opacity=".03"/>'
                 '<stop offset="38%" stop-color="#ffe9b8" stop-opacity=".11"/>'
                 '<stop offset="46%" stop-color="#fff6df" stop-opacity=".40"/>'
                 '<stop offset="50%" stop-color="#fff" stop-opacity=".95"/>'
                 '<stop offset="54%" stop-color="#fff6df" stop-opacity=".40"/>'
                 '<stop offset="62%" stop-color="#ffe9b8" stop-opacity=".11"/>'
                 '<stop offset="74%" stop-color="#ffe0a4" stop-opacity=".03"/>'
                 '<stop offset="100%" stop-color="#fff" stop-opacity="0"/>')
    defs.append(f'<linearGradient id="fspk" x1="0" y1="0" x2="1" y2="0">'
                f"{spk_stops}</linearGradient>")
    defs.append(f'<linearGradient id="fspkv" x1="0" y1="0" x2="0" y2="1">'
                f"{spk_stops}</linearGradient>")

    # Decorrelated twinkle periods. Near-prime ratios so the eight stars never
    # resync into a pulse, and a 0.78 to 1.0 swing, about a third of a
    # magnitude, which is the honest end of real scintillation.
    periods = [4.3, 5.9, 3.7, 6.7, 3.1, 5.3, 4.7, 6.1]
    out = []
    for i, (name, x, y, mag, bv, tier) in enumerate(FLAG_STARS):
        t = _tint_index(bv)
        # Rendered area tracks flux, so radius goes as 10^(-0.2 dm). Pushed to
        # 0.28 for legibility at hero scale, which is inside the range chart
        # renderers use and still leaves Megrez visibly the faint one.
        s = 10 ** (-0.28 * (mag - 1.77))
        # Polaris is drawn larger on the flag itself, so it keeps that emphasis.
        halo = s * (1.42 if name == "Polaris" else 1.0)
        core_r = 2.7 * (s ** 0.35)          # nearly constant, by design
        ring_r = core_r * 1.95
        # Halo EXTENT belongs to the atmosphere and the lens, not to the star,
        # so it is nearly the same for every star in one frame. What a faint
        # star loses is halo BRIGHTNESS. Scaling extent linearly on flux is what
        # erased Megrez: at mag 3.31 its glow radius fell to 4.8 against a 3.7
        # color ring, so the entire halo hid inside the core and the faintest
        # Dipper star rendered as a bare gold disc while its seven neighbors
        # carried halos two to three times their ring. Extent now goes as the
        # 0.45 power, which holds that ratio above 2 at every magnitude, and the
        # magnitude moves into `dim` where it was always supposed to live.
        spread = halo ** 0.45
        glow_r = 13.0 * spread
        au_r = 42.0 * spread
        dim = 0.34 + 0.66 * s
        # Every star gets a cross, because the cross is the instrument. Megrez
        # used to get none, which is what made it read as a circle rather than
        # as a faint star. Faint means short and dim, never absent.
        # Spike length is the aperture's, and it must CLEAR the halo. Only the
        # middle half of a spike is above 0.1 alpha, so if the tips stop short
        # of where the glow has faded the whole cross is drawn inside the glow
        # and cannot be seen. Keying length to glow_r guarantees the escape at
        # every magnitude, which fixed length times flux never did. Brightness
        # rides in `dim`; tier only trims for variety across the seven.
        L = glow_r * 3.5 * (1.0 if tier == 1 else (0.92 if tier == 2 else 0.88))
        # Waist ~1% of length after the quadratic's midpoint halving, because
        # thinness is the whole trick, but FLOORED. A waist proportional to
        # length is the second half of the Megrez bug: at tier 3 it worked out
        # to 0.18 viewBox units, a quarter of a pixel on the rendered hero, so
        # antialiasing dissolved the cross and left the bare disc even once the
        # halo was fixed. Spike width comes from the aperture, so it is the same
        # for every star in the frame; only length carries brightness.
        w = max(0.62, L * 0.020)
        spikes = (
            f'<path fill="url(#fspk)" d="M{x - L:.1f},{y} Q{x},{y - w:.2f} '
            f'{x + L:.1f},{y} Q{x},{y + w:.2f} {x - L:.1f},{y} Z"/>'
            f'<path fill="url(#fspkv)" d="M{x},{y - L * 0.91:.1f} '
            f'Q{x + w:.2f},{y} {x},{y + L * 0.91:.1f} '
            f'Q{x - w:.2f},{y} {x},{y - L * 0.91:.1f} Z"/>')
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{au_r:.1f}" fill="url(#fa{t})" '
            f'opacity="{dim:.3f}"/>'
            f'<g class="fstar" style="animation-duration:{periods[i]}s;'
            f'animation-delay:-{periods[i] * 0.37:.1f}s" opacity="{dim:.3f}">'
            f'<circle cx="{x}" cy="{y}" r="{glow_r:.1f}" fill="url(#fg{t})"/>'
            f"{spikes}</g>"
            f'<circle cx="{x}" cy="{y}" r="{ring_r:.2f}" fill="url(#fr{t})"/>'
            f'<circle cx="{x}" cy="{y}" r="{core_r:.2f}" fill="url(#fcore)"/>')
    return ('<svg class="flagsky" viewBox="0 0 600 400" aria-hidden="true">'
            f'<defs>{"".join(defs)}</defs>{"".join(out)}</svg>')


# ---------- the brand mark (the real logo: gold Alaska on the night) ----------

_AK_CACHE = {}


def _ak_d(max_points, keep_rings, box=100, pad=4):
    """SVG path of the true Alaska silhouette from the committed geodata,
    projected with the same Albers the docket map uses. Cached, nav and
    footer ask for it on every page."""
    key = (max_points, keep_rings, box, pad)
    if key not in _AK_CACHE:
        paths = db.alaska_paths(max_points=max_points, keep_rings=keep_rings)
        T = db.fit_transform(paths, box, box, pad)
        _AK_CACHE[key] = db.path_d(paths, T)
    return _AK_CACHE[key]


def ak_mark():
    """Inline brand mark for the nav and footer, the state in gold."""
    return ('<svg class="akmark" viewBox="0 0 100 100" aria-hidden="true">'
            f'<path d="{_ak_d(700, 5)}" fill="#ffc72c"/></svg>')


def ak_favicon():
    """Favicon data URI, the logo tile: gold Alaska on the night square."""
    from urllib.parse import quote
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<rect width='100' height='100' rx='16' fill='#02060f'/>"
           f"<path d='{_ak_d(240, 3, box=100, pad=8)}' fill='#ffc72c'/></svg>")
    return "data:image/svg+xml," + quote(svg, safe="")


# ---------- shared chrome ----------

def nav(prefix, active):
    # GAS WATCH sits beside DOCKET because they are the two datasets, decisions
    # on a scale of months and the physical system on a scale of days. Added to
    # the top nav on the maintainer's call, 2026-08-05, over the build brief's
    # footer-first guidance.
    links = [("", "HOME"), ("docket/", "DOCKET"), ("gas-watch/", "GAS WATCH"),
             ("archive/", "ARTICLES"), ("videos/", "VIDEOS"),
             ("services/", "SERVICES"), ("about/", "ABOUT")]
    on = ' class="on"'
    # An empty `active` must light nothing, because every string starts with
    # the empty string. Passing "" once lit all six links gold at the same time
    # on the gas watch page, which reads as a broken nav rather than a page
    # with no section.
    a = "".join(
        f'<a href="{prefix}{href or "./"}"'
        f'{on if active and key.lower().startswith(active) else ""}>{key}</a>'
        for href, key in links)
    return f"""<nav class="topnav">
  <a class="wordmark" href="{prefix}./">{ak_mark()}<span>ALASKA.AI</span></a>
  <div class="navlinks">{a}</div>
</nav>"""


def subscribe_html():
    """Native signup form posting straight to Buttondown, styled to house."""
    return """<h2 data-reveal id="alerts">Deadline alerts, in your inbox</h2>
<p class="sub" data-reveal>One email when a public comment window opens or a decision is about
to land. Nothing else, ever. Unsubscribe any time.</p>
<form class="subscribe" data-reveal action="https://buttondown.com/api/emails/embed-subscribe/AlaskaAI"
method="post" target="_blank">
  <label class="vh" for="bd-email">Your email</label>
  <input type="email" name="email" id="bd-email" required placeholder="you@example.com"
  autocomplete="email">
  <button class="cta gold" type="submit">GET ALERTS</button>
</form>"""


def scan_html():
    """Homepage section for the Bottleneck Scanner (the alaska-ai-scanner
    repo's public front door). Pure HTML, no JS here, the one field submits as
    a GET to the scan page, which prefills and runs the real flow."""
    return """<h2 data-reveal id="scan">Would AI actually help your business</h2>
<p class="sub" data-reveal>Our scanner reads your own public pages and hands back an honest map.
The pockets where AI earns its place, the ones where a plain rule wins first, and the
ones it should not touch. Free, about 20 minutes of real research, no signup to see it.</p>
<form class="subscribe" data-reveal action="scan/" method="get">
  <label class="vh" for="scan-url">Your website</label>
  <input type="text" name="url" id="scan-url" required placeholder="yourbusiness.com"
  autocomplete="url" inputmode="url">
  <button class="cta gold" type="submit">SCAN MY BUSINESS</button>
</form>"""


def footer(prefix, today):
    icons = "".join(
        f'<a href="{url}" target="_blank" rel="noopener" aria-label="Alaska AI on {name}" '
        f'title="{name}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg></a>'
        for name, url, d in SOCIALS)
    return f"""<footer>
<div class="foot-grid">
  <div class="foot-brand">{ak_mark()}<span>ALASKA.AI</span></div>
  <div class="foot-links">
    <a href="{prefix}docket/">DOCKET</a>
    <a href="{prefix}archive/">ARTICLES</a><a href="{prefix}topics/">BEATS</a>
    <a href="{prefix}videos/">VIDEOS</a>
    <a href="{prefix}sources/">SOURCES</a>
    <a href="{prefix}gas-watch/">GAS WATCH</a>
    <a href="{prefix}scan/">SCANNER</a>
    <a href="{prefix}services/">SERVICES</a>
    <a href="{prefix}about/">ABOUT</a>
    <a href="{prefix}questions/">QUESTIONS</a>
    <a href="{prefix}feed.xml">RSS</a>
    <a href="{prefix}data/">DATA</a>
    <a href="{prefix}privacy/">PRIVACY</a>
  </div>
</div>
<div class="socials">{icons}</div>
<div class="foot-line">BUILT IN THE NORTH &middot; UPDATED {today.isoformat()} &middot;
61&#176;13'N 149&#176;54'W &middot; EVERY FACT VERIFIED TO ITS SOURCE</div>
</footer>"""


SITE_CSS = """
:root{--night:#02060f;--deep:#050b16;--panel:#0a1626;--panel2:#0e2138;--line:#1c3350;
--snow:#f4f8ff;--body:#c3d2e6;--mute:#8da2be;--gold:#ffc72c;--halo:#ffda6e;
--green:#3ce6b4;--amber:#f2a43a;--blue:#5ac8f0;--violet:#9664e6;}
@font-face{font-family:Fraunces;src:url(FONTPREFIXfonts/fraunces.woff2) format("woff2");font-weight:100 900;font-display:swap;}
@font-face{font-family:JBMono;src:url(FONTPREFIXfonts/jbmono.woff2) format("woff2");font-weight:400;font-display:swap;}
@font-face{font-family:JBMono;src:url(FONTPREFIXfonts/jbmono-md.woff2) format("woff2");font-weight:500;font-display:swap;}
@font-face{font-family:Manrope;src:url(FONTPREFIXfonts/manrope.woff2) format("woff2");font-weight:200 800;font-display:swap;}
@view-transition{navigation:auto;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;overflow-x:clip;}
body{background:var(--night);color:var(--body);font-family:Manrope,system-ui,sans-serif;
line-height:1.55;overflow-x:clip;scrollbar-color:#1c3350 transparent;}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:90;
background-image:url(GRAIN_URI);mix-blend-mode:overlay;opacity:.55;}
::selection{background:rgba(255,199,44,.25);}
::-webkit-scrollbar{width:11px;}
::-webkit-scrollbar-thumb{background:var(--panel2);border-radius:6px;border:3px solid var(--night);}
::-webkit-scrollbar-thumb:hover{background:#2c5876;}
a{color:inherit;}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px;}
.skip{position:absolute;left:-9999px;top:0;z-index:100;background:var(--gold);color:#241a00;
font-family:JBMono,monospace;font-size:12px;letter-spacing:.1em;padding:10px 18px;border-radius:0 0 8px 0;}
.skip:focus{left:0;}

/* gold scroll progress hairline (scroll-driven, compositor only) */
@supports (animation-timeline: scroll()){
  body::before{content:"";position:fixed;top:0;left:0;right:0;height:2px;z-index:95;
  background:linear-gradient(90deg,var(--gold),var(--halo));transform-origin:0 50%;
  transform:scaleX(0);animation:progress linear both;animation-timeline:scroll(root);}
  @keyframes progress{to{transform:scaleX(1);}}
}

/* ---------- sky ---------- */
.sky{position:absolute;inset:0 0 auto 0;height:130vh;overflow:hidden;pointer-events:none;z-index:0;}
.veil{position:absolute;border-radius:50%;filter:blur(70px);mix-blend-mode:screen;opacity:.62;}
.v1{width:60vw;height:44vh;left:38vw;top:-12vh;background:radial-gradient(closest-side,rgba(60,230,180,.5),transparent 70%);
animation:drift1 26s ease-in-out infinite alternate;}
.v2{width:48vw;height:40vh;left:16vw;top:-16vh;background:radial-gradient(closest-side,rgba(90,200,240,.4),transparent 70%);
animation:drift2 34s ease-in-out infinite alternate;}
.v3{width:34vw;height:30vh;left:62vw;top:6vh;background:radial-gradient(closest-side,rgba(150,100,230,.28),transparent 70%);
animation:drift3 42s ease-in-out infinite alternate;}
@keyframes drift1{from{transform:translate(-6vw,0) rotate(-4deg);}to{transform:translate(7vw,4vh) rotate(5deg);}}
@keyframes drift2{from{transform:translate(5vw,2vh);}to{transform:translate(-7vw,-2vh);}}
@keyframes drift3{from{transform:translate(0,0) scale(1);}to{transform:translate(-5vw,3vh) scale(1.15);}}
/* aurora curtains: banded light drifting sideways, faded toward the ground */
.curtain{position:absolute;inset:-14% 0 auto;height:96vh;mix-blend-mode:screen;
background:repeating-linear-gradient(97deg,transparent 0 5%,rgba(60,230,180,.22) 7% 9.5%,
rgba(60,230,180,.06) 11% 13%,transparent 15% 19%,rgba(90,200,240,.19) 21% 23.5%,
rgba(90,200,240,.05) 25% 27%,transparent 29% 34%,rgba(150,100,230,.13) 35% 37%,transparent 39% 45%);
background-size:220% 100%;filter:blur(16px);transform:skewY(-6deg);
-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,1) 8%,rgba(0,0,0,.5) 46%,transparent 76%);
mask-image:linear-gradient(180deg,rgba(0,0,0,1) 8%,rgba(0,0,0,.5) 46%,transparent 76%);
animation:curtain 44s ease-in-out infinite alternate;}
.curtain.c2{transform:skewY(4deg);filter:blur(26px);opacity:.7;
background-size:260% 100%;animation-duration:58s;animation-direction:alternate-reverse;}
@keyframes curtain{from{background-position:0% 0;}to{background-position:100% 0;}}
/* a meteor, every so often */
.meteor{position:absolute;top:9vh;left:-8vw;width:120px;height:2px;border-radius:2px;
background:linear-gradient(90deg,transparent,rgba(223,241,255,.9) 65%,#fff);opacity:0;
transform:rotate(16deg);animation:meteor 7s linear infinite;animation-delay:3s;}
@keyframes meteor{0%,76%{opacity:0;transform:translate(0,0) rotate(16deg);}
78%{opacity:.9;}88%{opacity:0;transform:translate(64vw,20vh) rotate(16deg);}
100%{opacity:0;transform:translate(64vw,20vh) rotate(16deg);}}
.stars{position:absolute;inset:0;background-image:
radial-gradient(1px 1px at 12% 22%,rgba(244,248,255,.7),transparent 60%),
radial-gradient(1px 1px at 33% 8%,rgba(244,248,255,.5),transparent 60%),
radial-gradient(1.5px 1.5px at 56% 30%,rgba(244,248,255,.6),transparent 60%),
radial-gradient(1px 1px at 72% 12%,rgba(244,248,255,.5),transparent 60%),
radial-gradient(1px 1px at 88% 26%,rgba(244,248,255,.65),transparent 60%),
radial-gradient(1.5px 1.5px at 44% 16%,rgba(244,248,255,.4),transparent 60%),
radial-gradient(1px 1px at 22% 34%,rgba(244,248,255,.45),transparent 60%),
radial-gradient(1px 1px at 64% 6%,rgba(244,248,255,.55),transparent 60%),
radial-gradient(1.2px 1.2px at 80% 38%,rgba(244,248,255,.4),transparent 60%),
radial-gradient(1px 1px at 5% 10%,rgba(244,248,255,.5),transparent 60%);}
/* the flag: Big Dipper + Polaris, gold on the night */
.flagsky{position:absolute;right:2vw;top:5vh;width:min(46vw,560px);height:auto;opacity:.95;}
/* Scintillation rides on opacity only, and only on the glow-and-spikes
   subgroup. No animated drop-shadow or blur: those repaint a huge area every
   frame, and the halo is the one layer that should never flicker anyway.
   The stepped keyframes keep it irregular instead of pulsing. */
.fstar{animation:twinkle 4s ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:.78;}34%{opacity:.94;}47%{opacity:.84;}
68%{opacity:1;}82%{opacity:.89;}}

.wrap{position:relative;max-width:1120px;margin:0 auto;padding:0 24px 110px;z-index:1;}

/* ---------- nav (sticky, glass when scrolled) ---------- */
.topnav{position:sticky;top:0;z-index:80;display:flex;align-items:center;gap:20px;
padding:26px 0 14px;flex-wrap:wrap;}
.topnav::before{content:"";position:absolute;top:0;bottom:0;left:50%;width:100vw;
margin-left:-50vw;z-index:-1;opacity:0;
background:rgba(2,6,15,.78);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
border-bottom:1px solid rgba(28,51,80,.7);transition:opacity .35s;}
.topnav.scrolled::before{opacity:1;}
.wordmark{display:flex;align-items:center;gap:11px;font-family:JBMono,monospace;
font-size:15px;letter-spacing:.24em;color:var(--snow);text-decoration:none;font-weight:500;}
.wordmark .polaris{width:17px;height:17px;transition:transform .5s;}
.wordmark:hover .polaris{transform:rotate(90deg) scale(1.15);}
.akmark{filter:drop-shadow(0 0 7px rgba(255,199,44,.55));flex:none;}
.wordmark .akmark{width:30px;height:30px;transition:transform .5s;}
.wordmark:hover .akmark{transform:scale(1.12);}
.navlinks{margin-left:auto;display:flex;gap:26px;font-family:JBMono,monospace;
font-size:12px;letter-spacing:.16em;}
.navlinks a{color:var(--mute);text-decoration:none;padding:6px 0;position:relative;}
.navlinks a::after{content:"";position:absolute;left:0;right:100%;bottom:2px;height:1.5px;
background:var(--gold);transition:right .25s ease;}
.navlinks a:hover{color:var(--snow);}
.navlinks a:hover::after{right:0;background:var(--blue);}
.navlinks a.on{color:var(--gold);}
.navlinks a.on::after{right:0;}
/* Seven items need a compact row sooner than the rest of the mobile layout
   does, so this breakpoint is deliberately wider than the 720px block below.
   A phone in landscape is wide enough to miss that block and too narrow to
   seat seven links at full size, so the row wrapped and the sticky nav
   doubled to 121px, which buried four docket map pins under it in a map
   frame only 219px tall. Compact keeps it to one row there. The wrap is the
   backstop for real phone widths, where it splits to two rows cleanly. */
@media (max-width:900px){.navlinks{gap:13px;row-gap:9px;font-size:10.5px;flex-wrap:wrap;}}

/* ---------- type ---------- */
h1{font-family:Fraunces,serif;font-weight:580;font-size:clamp(44px,7.4vw,92px);line-height:1.0;
letter-spacing:-.015em;color:var(--snow);}
h1 em{font-style:normal;color:var(--gold);}
h2{font-family:Fraunces,serif;font-weight:540;font-size:clamp(26px,3.6vw,36px);color:var(--snow);
margin:84px 0 8px;letter-spacing:-.01em;}
h2 a{text-decoration:none;}
.sub{color:var(--mute);font-size:15.5px;margin-bottom:26px;max-width:640px;}
.sub a{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(90,200,240,.25);}
.chip{font-family:JBMono,monospace;font-size:12px;letter-spacing:.09em;font-weight:500;}
.chip.days{color:var(--gold);}
.chip.kind{color:#758aa7;}
.who{font-family:JBMono,monospace;font-size:11.5px;letter-spacing:.09em;color:var(--mute);}

/* ---------- hero (home) ---------- */
.hero{padding:11vh 0 0;min-height:74vh;}
html.js .heroanim > *{opacity:0;transform:translateY(22px);
animation:rise .85s cubic-bezier(.2,.7,.2,1) forwards;}
html.js .heroanim > *:nth-child(2){animation-delay:.1s;}
html.js .heroanim > *:nth-child(3){animation-delay:.22s;}
html.js .heroanim > *:nth-child(4){animation-delay:.34s;}
html.js .heroanim > *:nth-child(5){animation-delay:.46s;}
@keyframes rise{to{opacity:1;transform:none;}}
.daylight{display:inline-block;font-family:JBMono,monospace;font-size:12.5px;letter-spacing:.14em;
color:var(--gold);border:1px solid rgba(255,199,44,.35);border-radius:5px;padding:8px 14px;
background:rgba(14,33,56,.55);margin-bottom:34px;position:relative;overflow:hidden;}
.daylight::after{content:"";position:absolute;inset:0;transform:translateX(-130%) skewX(-18deg);
background:linear-gradient(105deg,transparent 30%,rgba(255,218,110,.16) 50%,transparent 70%);
animation:sweep 7s ease-in-out infinite;}
@keyframes sweep{0%,72%{transform:translateX(-130%) skewX(-18deg);}
88%,100%{transform:translateX(130%) skewX(-18deg);}}
.hero h1{max-width:12ch;}
.tag{font-size:clamp(17px,2.2vw,21px);max-width:600px;margin:28px 0 0;color:var(--body);}
.ctarow{display:flex;gap:16px;margin:40px 0 0;flex-wrap:wrap;}
.ctarow.act{margin-top:20px;}
.cta{font-family:JBMono,monospace;font-size:13px;letter-spacing:.12em;text-decoration:none;
padding:14px 22px;border-radius:6px;transition:transform .2s,box-shadow .2s,border-color .2s;
position:relative;overflow:hidden;display:inline-block;}
.cta:active{transform:translateY(0) scale(.98);}
.cta.gold{background:var(--gold);color:#241a00;font-weight:500;}
.cta.gold::after{content:"";position:absolute;inset:0;transform:translateX(-130%) skewX(-18deg);
background:linear-gradient(105deg,transparent 35%,rgba(255,255,255,.5) 50%,transparent 65%);
transition:transform .55s ease;}
.cta.gold:hover{transform:translateY(-2px);box-shadow:0 10px 34px rgba(255,199,44,.3);}
.cta.gold:hover::after{transform:translateX(130%) skewX(-18deg);}
.cta.ghost{border:1px solid var(--line);color:var(--body);}
.cta.ghost:hover{border-color:var(--blue);color:var(--snow);transform:translateY(-2px);}
.cta.sm{font-size:12px;padding:11px 18px;}
.statrow{display:flex;gap:34px;flex-wrap:wrap;margin:36px 0 0;font-family:JBMono,monospace;}
.stat .n{font-size:clamp(26px,3.4vw,38px);font-weight:500;color:var(--snow);font-variant-numeric:tabular-nums;}
.stat .n.g{color:var(--gold);text-shadow:0 0 22px rgba(255,199,44,.35);}
.stat .l{font-size:11.5px;letter-spacing:.18em;color:var(--mute);margin-top:2px;}

/* ---------- latest deck ---------- */
.latest{display:grid;grid-template-columns:minmax(260px,380px) 1fr;gap:44px;align-items:center;}
.cover{border-radius:12px;border:1px solid var(--line);overflow:hidden;display:block;
transition:transform .25s,box-shadow .25s;box-shadow:0 24px 70px rgba(0,0,0,.5);}
.cover img{width:100%;height:auto;display:block;aspect-ratio:1080/1350;}
.cover:hover{transform:translateY(-4px) rotate(-.4deg);box-shadow:0 30px 80px rgba(0,0,0,.65);}
.latest h3{font-family:Fraunces,serif;font-weight:540;font-size:clamp(24px,3vw,32px);
color:var(--snow);line-height:1.15;margin:12px 0 14px;}
.latest p{font-size:16.5px;max-width:56ch;}
/* ---------- latest video ---------- */
.latestvid{display:grid;grid-template-columns:clamp(230px,30vw,320px) 1fr;gap:44px;
align-items:center;}
.vidwrap{position:relative;border-radius:16px;border:1px solid var(--line);overflow:hidden;
background:var(--panel);box-shadow:0 24px 70px rgba(0,0,0,.5);}
.vidwrap video{display:block;width:100%;aspect-ratio:9/16;height:auto;object-fit:cover;
background:var(--deep);cursor:pointer;}
.vsound{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);
display:flex;align-items:center;gap:7px;border:1px solid rgba(255,199,44,.55);
border-radius:999px;padding:8px 15px;background:rgba(2,6,15,.72);color:var(--gold);
font-family:JBMono,monospace;font-size:11px;letter-spacing:.14em;cursor:pointer;
backdrop-filter:blur(6px);white-space:nowrap;}
.vsound:hover{background:rgba(2,6,15,.9);}
.vsound.on{opacity:.55;}
.latestvid h3{font-family:Fraunces,serif;font-weight:540;font-size:clamp(24px,3vw,32px);
color:var(--snow);line-height:1.15;margin:12px 0 14px;}
.latestvid p{font-size:16.5px;max-width:56ch;}
@media(max-width:720px){.latestvid{grid-template-columns:1fr;}
.vidwrap{max-width:320px;}}

/* ---------- cards (docket closing soon + archive) ---------- */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;}
.card{display:block;background:linear-gradient(165deg,var(--panel) 0%,var(--deep) 100%);
border:1px solid var(--line);border-radius:12px;padding:22px 24px;text-decoration:none;
transition:transform .25s,border-color .25s,box-shadow .25s;}
.card:hover{transform:translateY(-3px);border-color:#2c5876;box-shadow:0 14px 40px rgba(0,0,0,.5);}
.card.a-open{border-color:rgba(255,199,44,.45);}
.card.a-open:hover{border-color:var(--gold);box-shadow:0 14px 44px rgba(255,199,44,.13);}
.cardtop{margin-bottom:14px;}
.card .big{font-family:Fraunces,serif;font-weight:560;font-size:44px;color:var(--snow);line-height:1;}
.card.a-open .big{color:var(--gold);}
.card .when{display:block;margin:8px 0 14px;}
.card h3{font-family:Manrope,sans-serif;font-weight:600;font-size:16.5px;color:var(--snow);line-height:1.3;}
.card .who{margin-top:8px;}
.badge{font-family:JBMono,monospace;font-size:11px;letter-spacing:.13em;font-weight:500;
padding:4px 10px;border-radius:4px;border:1px solid;display:inline-block;}
.b-open{color:var(--green);border-color:rgba(60,230,180,.5);background:rgba(60,230,180,.06);}
.b-indirect{color:var(--mute);border-color:rgba(141,162,190,.4);}
.b-closed{color:var(--amber);border-color:rgba(242,164,58,.5);background:rgba(242,164,58,.05);}

/* archive deck cards */
.deckgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px;}
.deck{background:linear-gradient(165deg,var(--panel) 0%,var(--deep) 100%);
border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;display:block;
transition:transform .25s,border-color .25s,box-shadow .25s;}
.deck:hover{transform:translateY(-4px);border-color:#2c5876;box-shadow:0 18px 54px rgba(0,0,0,.55);}
.deck img{width:100%;height:auto;display:block;border-bottom:1px solid var(--line);aspect-ratio:1080/1350;background:var(--panel);}
.deck .meta{padding:18px 20px 20px;}
.deck .meta h3{font-family:Fraunces,serif;font-weight:540;font-size:19px;color:var(--snow);line-height:1.25;}
.deck .meta .who{margin-top:10px;}

/* ---------- docket items ---------- */
.item{display:flex;gap:26px;background:linear-gradient(170deg,var(--panel) 0%,var(--deep) 88%);
border:1px solid var(--line);border-radius:14px;padding:30px 32px;margin-bottom:18px;
scroll-margin-top:96px;transition:border-color .3s,box-shadow .3s;}
.item:target{border-color:var(--gold);
box-shadow:0 0 0 1px rgba(255,199,44,.3),0 18px 70px rgba(0,0,0,.5);}
.item.a-open{border-color:rgba(255,199,44,.4);
box-shadow:0 0 0 1px rgba(255,199,44,.08),0 18px 60px rgba(0,0,0,.35);}
.doorcol{flex:none;display:flex;flex-direction:column;align-items:center;gap:10px;padding-top:4px;}
.door{width:44px;height:56px;}
.item.a-open .door{filter:drop-shadow(0 0 10px rgba(255,199,44,.45));}
.doorcol .num{font-family:JBMono,monospace;font-size:12px;color:#728aad;letter-spacing:.1em;}
.item .body{min-width:0;flex:1;}
.item .top{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px;}
.item h3{font-family:Fraunces,serif;font-weight:540;font-size:clamp(22px,2.8vw,28px);
color:var(--snow);line-height:1.18;margin-bottom:8px;}
.item p{margin:12px 0;font-size:16px;max-width:70ch;}
.access{font-size:14.5px;color:var(--mute);border-left:2px solid var(--gold);
padding:2px 0 2px 14px;margin:14px 0;max-width:64ch;}
.item.a-indirect .access,.item.a-closed .access{border-left-color:var(--line);}
.srcs{font-size:13.5px;color:var(--mute);margin-top:14px;}
.srcs a{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(90,200,240,.25);}
.srcs a:hover{border-bottom-color:var(--blue);}
.hist{font-size:12.5px;color:#728aad;margin-top:10px;font-family:JBMono,monospace;letter-spacing:.02em;}
.rail{display:flex;margin:22px 0 4px;position:relative;}
.rail::before{content:"";position:absolute;left:0;right:0;top:5px;height:1.5px;
background:linear-gradient(90deg,var(--line) 0%,#2c5876 100%);}
.rail.solo::before{display:none;}
.stop{flex:1;min-width:0;position:relative;padding:16px 14px 0 0;}
.stop .dot{position:absolute;top:0;left:0;width:11px;height:11px;border-radius:50%;
background:var(--deep);border:2px solid #3a5f84;}
.stop.future .dot{border-color:var(--gold);box-shadow:0 0 10px rgba(255,199,44,.5);}
.stop .d{display:block;font-family:JBMono,monospace;font-size:12px;font-weight:500;
letter-spacing:.08em;color:#728aad;}
.stop.future .d{color:var(--gold);}
.stop .l{display:block;font-size:12.5px;color:var(--mute);line-height:1.35;margin-top:3px;max-width:24ch;}
.stop.future .l{color:var(--body);}
/* the TODAY tick on a timeline */
.stop.now{flex:0 0 auto;padding-right:26px;}
.stop.now .dot{width:9px;height:9px;top:1px;background:var(--gold);border-color:var(--gold);
box-shadow:0 0 12px rgba(255,199,44,.85);animation:heartbeat 2.4s ease-in-out infinite;}
.stop.now .d{color:var(--gold);letter-spacing:.2em;}
@keyframes heartbeat{0%,100%{box-shadow:0 0 6px rgba(255,199,44,.5);}
50%{box-shadow:0 0 16px rgba(255,199,44,.95);}}

/* ---------- map ---------- */
.maphero{margin:44px -24px 0;padding:10px 24px 6px;position:relative;}
.maphero svg{width:100%;height:auto;display:block;}
.maphero a{cursor:pointer;}
.maphero a circle{transition:stroke-width .2s;}
.maphero a:hover circle{stroke-width:4;}
.pinnum{font-family:JBMono,monospace;font-size:13.5px;font-weight:500;}

.mapcap{display:flex;gap:10px 26px;flex-wrap:wrap;padding:14px 2px 0;}
.mapkey{display:flex;align-items:center;gap:9px;font-family:JBMono,monospace;font-size:12.5px;
letter-spacing:.05em;color:var(--mute);text-decoration:none;transition:color .2s;}
.mapkey:hover{color:var(--snow);}
.mapkey b{font-weight:500;border:1.5px solid;border-radius:50%;width:21px;height:21px;flex:none;
text-align:center;line-height:19px;background:var(--deep);}
.k-open{color:var(--green);border-color:var(--green);}
.k-indirect{color:var(--mute);border-color:var(--mute);}
.k-closed{color:var(--amber);border-color:var(--amber);}

/* ---------- deck detail gallery ---------- */
.gallery{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;
padding:8px 4px 20px;scrollbar-width:thin;scrollbar-color:var(--line) transparent;}
.gallery img{width:min(74vw,430px);height:auto;border-radius:10px;border:1px solid var(--line);
scroll-snap-align:center;flex:none;box-shadow:0 16px 46px rgba(0,0,0,.45);
transition:transform .25s,border-color .25s;}
html.js .gallery img{cursor:zoom-in;}
html.js .gallery img:hover{transform:translateY(-3px);border-color:#2c5876;}
.galhint{font-family:JBMono,monospace;font-size:11.5px;letter-spacing:.14em;color:#728aad;margin:4px 0 0;}
.galbar{display:none;align-items:center;gap:16px;margin-top:6px;font-family:JBMono,monospace;}
html.js .galbar{display:flex;}
.galbar .count{font-size:13px;letter-spacing:.18em;color:var(--mute);font-variant-numeric:tabular-nums;min-width:76px;}
.galbtn{width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:rgba(10,22,38,.7);
color:var(--body);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
transition:border-color .2s,color .2s,transform .2s;}
.galbtn:hover{border-color:var(--gold);color:var(--gold);transform:translateY(-2px);}
.galbtn svg{width:16px;height:16px;}
pre.copy{white-space:pre-wrap;background:var(--panel);border:1px solid var(--line);
padding:22px 24px;border-radius:10px;font-family:JBMono,monospace;font-size:13.5px;
line-height:1.7;color:var(--body);overflow-x:auto;}

/* ---------- lightbox ---------- */
.lightbox{border:none;background:transparent;padding:0;max-width:none;max-height:none;
width:100vw;height:100dvh;display:none;align-items:center;justify-content:center;}
.lightbox[open]{display:flex;}
.lightbox::backdrop{background:rgba(2,6,15,.93);backdrop-filter:blur(8px);}
.lightbox img{max-height:86dvh;max-width:92vw;width:auto;border-radius:10px;
border:1px solid var(--line);box-shadow:0 30px 110px rgba(0,0,0,.8);}
.lightbox .lbbar{position:fixed;top:18px;left:0;right:0;display:flex;align-items:center;
justify-content:center;gap:18px;font-family:JBMono,monospace;color:var(--mute);}
.lightbox .lbbar .count{font-size:13px;letter-spacing:.2em;font-variant-numeric:tabular-nums;}
.lightbox .lbclose{position:fixed;top:16px;right:20px;}
.lightbox .lbprev{position:fixed;left:20px;top:50%;transform:translateY(-50%);}
.lightbox .lbnext{position:fixed;right:20px;top:50%;transform:translateY(-50%);}

/* ---------- how it works ---------- */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;}
.step{background:linear-gradient(165deg,var(--panel) 0%,var(--deep) 100%);
border:1px solid var(--line);border-radius:12px;padding:24px 26px;}
.step .k{font-family:JBMono,monospace;font-size:12px;letter-spacing:.16em;color:var(--gold);}
.step h3{font-family:Fraunces,serif;font-weight:540;font-size:21px;color:var(--snow);margin:10px 0 8px;}
.step p{font-size:14.5px;color:var(--mute);}

/* ---------- prose (about) ---------- */
.prose{max-width:660px;font-size:17px;}
.prose p{margin:18px 0;}
/* a.proselink is for an inline link OUTSIDE a .prose block. The base rule is
   a{color:inherit} with no decoration reset, so a bare anchor in a plain
   paragraph falls back to the browser's underline and the paragraph's colour,
   which is the one link on the site that did not look like the others. */
.prose a,a.proselink{color:var(--blue);text-decoration:none;
border-bottom:1px solid rgba(90,200,240,.25);}

/* ---------- the article, and the verification record under it ---------- */
/* The deck says it in pictures. This says it in text, so a reader on a screen
   reader, a search crawler and an answer engine all get the same story. */
.article .sl{margin:26px 0 0;padding:0 0 0 46px;position:relative;}
.article .sn{position:absolute;left:0;top:3px;font-family:JBMono,monospace;font-size:12px;
letter-spacing:.1em;color:#41546f;}
.article h3{font-size:19px;line-height:1.35;margin:0 0 6px;font-weight:600;}
.article p{margin:0;color:#b9c8dc;}
/* A figure that links to the document proving it. The gold underline is the
   primary-document tell, so a reader can see at a glance how much of a deck
   rests on filings rather than on somebody else's write-up. */
a.cite{color:inherit;text-decoration:none;border-bottom:1px dashed rgba(90,200,240,.5);}
a.cite.primary{border-bottom:1px solid var(--gold);}
a.cite:hover{background:rgba(90,200,240,.1);}
ol.claims{list-style:none;margin:18px 0 0;padding:0;max-width:760px;counter-reset:c;}
ol.claims li{counter-increment:c;position:relative;padding:14px 0 14px 46px;
border-top:1px solid var(--line);}
ol.claims li::before{content:counter(c,decimal-leading-zero);position:absolute;left:0;top:16px;
font-family:JBMono,monospace;font-size:11px;color:#41546f;}
ol.claims p{margin:0 0 7px;font-size:15.5px;line-height:1.5;color:#c6d4e6;}
.cmeta{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;
font-family:JBMono,monospace;font-size:11px;letter-spacing:.08em;}
.cmeta .k{color:#41546f;}
.cmeta .k.p{color:var(--gold);}
.cmeta a.src{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(90,200,240,.3);}
.cmeta .d{color:#41546f;}
@media(max-width:560px){.article .sl{padding-left:32px;}ol.claims li{padding-left:34px;}}

/* ---------- subscribe ---------- */
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);}
.subscribe{display:flex;gap:12px;flex-wrap:wrap;max-width:560px;}
.subscribe input[type=email],.subscribe input[type=text]{flex:1;min-width:230px;background:rgba(10,22,38,.85);
border:1px solid var(--line);border-radius:6px;padding:13px 16px;color:var(--snow);
font-family:JBMono,monospace;font-size:13.5px;letter-spacing:.03em;transition:border-color .2s;}
.subscribe input[type=email]::placeholder,.subscribe input[type=text]::placeholder{color:#728aad;}
.subscribe input[type=email]:focus,.subscribe input[type=text]:focus{border-color:var(--gold);outline:none;}
.subscribe .cta{border:none;cursor:pointer;font-family:JBMono,monospace;}
.fineprint{font-family:JBMono,monospace;font-size:11px;color:#728bac;
letter-spacing:.08em;margin-top:14px;}
.fineprint a{color:var(--mute);text-decoration:none;border-bottom:1px solid rgba(141,162,190,.3);}
.fineprint a:hover{color:var(--snow);}

/* ---------- lead form (services) ---------- */
.leadform{max-width:640px;}
.leadform label{display:block;font-family:JBMono,monospace;font-size:11.5px;
letter-spacing:.14em;color:var(--mute);margin:16px 0 0;text-transform:uppercase;}
.leadform .lf-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 16px;}
.leadform input[type=text],.leadform input[type=email],.leadform textarea,.leadform select{
display:block;width:100%;margin-top:7px;background:rgba(10,22,38,.85);
border:1px solid var(--line);border-radius:6px;padding:12px 14px;color:var(--snow);
font-family:Manrope,system-ui,sans-serif;font-size:15px;transition:border-color .2s;}
.leadform textarea{resize:vertical;min-height:76px;}
.leadform input:focus,.leadform textarea:focus,.leadform select:focus{
border-color:var(--gold);outline:none;}
.leadform ::placeholder{color:#728aad;}
.leadform select{color:var(--body);}
.leadform .ctarow{margin-top:28px;}
.leadform .cta{border:none;cursor:pointer;font-family:JBMono,monospace;}

/* ---------- footer ---------- */
.about-line{border-top:1px solid var(--line);margin-top:90px;padding-top:34px;font-size:15px;
color:var(--mute);max-width:660px;}
footer{margin-top:70px;border-top:1px solid var(--line);padding-top:30px;}
.foot-grid{display:flex;gap:20px 40px;align-items:flex-start;flex-wrap:wrap;}
.foot-brand{display:flex;align-items:center;gap:12px;font-family:JBMono,monospace;
font-size:13px;letter-spacing:.22em;color:var(--snow);}
.foot-brand .polaris{width:15px;height:15px;}
.foot-brand .akmark{width:26px;height:26px;}
.foot-links{margin-left:auto;display:flex;gap:22px;font-family:JBMono,monospace;
font-size:11.5px;letter-spacing:.14em;}
.foot-links a{color:var(--mute);text-decoration:none;transition:color .2s;}
.foot-links a:hover{color:var(--gold);}
.socials{display:flex;gap:12px;margin-top:22px;flex-wrap:wrap;}
.socials a{display:flex;width:40px;height:40px;align-items:center;justify-content:center;
border:1px solid var(--line);border-radius:11px;transition:transform .2s,border-color .2s,
box-shadow .2s;}
.socials svg{width:17px;height:17px;fill:var(--mute);transition:fill .2s;}
.socials a:hover{transform:translateY(-3px);border-color:rgba(255,199,44,.6);
box-shadow:0 8px 22px rgba(0,0,0,.4);}
.socials a:hover svg{fill:var(--gold);}
.foot-line{margin-top:18px;font-family:JBMono,monospace;font-size:11px;color:#728bac;
letter-spacing:.14em;line-height:2;}

/* ---------- reveals: IO-driven, no-JS users see everything ---------- */
html.js [data-reveal]{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease;}
html.js [data-reveal].in{opacity:1;transform:none;}
html.reveal-fallback [data-reveal]{opacity:1;transform:none;}
@media (max-width:720px){
  .item{flex-direction:column;gap:16px;padding:24px 20px;}
  .doorcol{flex-direction:row;}
  .rail{flex-direction:column;gap:14px;}
  .leadform .lf-grid{grid-template-columns:1fr;}
  .rail::before{left:5px;right:auto;top:0;bottom:0;width:1.5px;height:auto;}
  .stop{padding:0 0 0 26px;}
  .stop.now{padding:0 0 0 26px;}
  .maphero{margin:34px -12px 0;padding:0 12px;}
  .latest{grid-template-columns:1fr;}
  .flagsky{right:-4vw;top:2vh;width:70vw;opacity:.8;}
  .topnav{padding:18px 0 12px;}
  .lightbox .lbprev{left:8px;}
  .lightbox .lbnext{right:8px;}
  .foot-links{margin-left:0;flex-wrap:wrap;}
}
@media (prefers-reduced-motion:reduce){
  .veil,.fstar,.curtain,.meteor,.daylight::after,.stop.now .dot{animation:none;}
  html.js .heroanim > *{animation:none;opacity:1;transform:none;}
  .cta.gold::after{display:none;}
  html.js [data-reveal]{opacity:1;transform:none;transition:none;animation:none;}
  html{scroll-behavior:auto;}
  body::before{display:none;}
}
"""

MAP_JS = """
(function(){
  'use strict';
/* ------------------------ the docket map ------------------------
   Pan and zoom, and on a phone an opening view fitted to the pins.

   GEOMETRY scales, MARKS do not. The coastline, the grid and the pipeline
   live inside #mzoom and take the transform. Every pin, dot, tether and
   plant is a .mk group carrying its map coordinate, and it gets REPOSITIONED
   rather than resized. Without that split, the fitted phone view would blow
   the badges up to the size of boroughs.

   Everything here is an enhancement. With no script the map is already drawn
   at the right positions and every pin is already a working link. */
var mapsvg = document.querySelector('.maphero svg');
if (mapsvg && mapsvg.querySelector('#mzoom')) {
  var VBW = 1000, VBH = 620;
  var mz = mapsvg.querySelector('#mzoom');
  var marks = [].slice.call(mapsvg.querySelectorAll('.mk'));
  var reset = document.getElementById('mapreset');
  var k = 1, tx = 0, ty = 0, mscale = 1, home = null, minK = 1;

  /* The svg is xMidYMid SLICE, so on a phone, where the frame is far taller
     than the map's own 1000 by 620, the drawing is scaled to FILL and the
     sides are cropped. That means the scale is not simply width over 1000,
     and the window a reader can actually see is smaller than the viewBox.
     Ask the browser for the real matrix rather than assuming either. */
  function ctm(){
    var m = mapsvg.getScreenCTM();
    return (m && m.a) ? m.a : (mapsvg.getBoundingClientRect().width / VBW) || 1;
  }
  function px(){ return 1 / ctm(); }   /* viewBox units per css pixel */
  function view(){                     /* the visible window, in viewBox units */
    var r = mapsvg.getBoundingClientRect(), s = ctm();
    var w = s ? r.width / s : VBW, h = s ? r.height / s : VBH;
    return { w: w, h: h, x0: VBW / 2 - w / 2, y0: VBH / 2 - h / 2,
             x1: VBW / 2 + w / 2, y1: VBH / 2 + h / 2 };
  }
  var inset = 0;   /* band at the top the sticky nav will cover anyway */
  function clampT(){
    /* Two regimes. When the drawing is BIGGER than the frame, keep it covering
       so no drag can leave a band of empty background. When it is SMALLER,
       centre it instead, which is what happens on a short landscape frame where
       the pins only fit if the map shrinks past the point of filling. Clamping
       to cover in that case is what cropped eight pins clean off the map. The
       top is allowed to fall short by `inset`, the strip behind the sticky nav. */
    var v = view(), w = VBW * k, h = VBH * k, top = v.y0 + inset, uh = v.h - inset;
    tx = (w <= v.w) ? v.x0 + (v.w - w) / 2
                    : Math.min(v.x0, Math.max(v.x1 - w, tx));
    ty = (h <= uh) ? top + (uh - h) / 2
                   : Math.min(top, Math.max(v.y1 - h, ty));
  }
  function apply(){
    mz.setAttribute('transform', 'translate(' + tx.toFixed(2) + ' ' + ty.toFixed(2) +
                    ') scale(' + k.toFixed(4) + ')');
    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      var x = (+m.getAttribute('data-x')) * k + tx;
      var y = (+m.getAttribute('data-y')) * k + ty;
      m.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) +
                     ') scale(' + mscale.toFixed(3) + ')');
    }
    if (reset) {
      var atHome = Math.abs(k - home.k) < 0.01 &&
                   Math.abs(tx - home.tx) < 1 && Math.abs(ty - home.ty) < 1;
      reset.classList.toggle('on', !atHome);
    }
  }
  function zoomAt(nk, cx, cy){
    nk = Math.min(8, Math.max(minK, nk));
    if (nk === k) return;
    tx = cx - (cx - tx) * (nk / k);
    ty = cy - (cy - ty) * (nk / k);
    k = nk; clampT(); apply();
  }
  function toVB(ev){
    var r = mapsvg.getBoundingClientRect(), s = px();
    return { x: (ev.clientX - r.left) * s, y: (ev.clientY - r.top) * s };
  }

  /* On a narrow screen the whole state squeezes into a couple of hundred
     pixels and the pins are about five across, so open on the pins instead,
     and scale the marks UP because the svg itself is scaled so far down. */
  function fit(){
    var v = view();
    /* A mark is constant size in viewBox units and the drawing is scaled to the
       frame, so a badge that reads fine on a desktop comes out about 14px across
       on a handset. Scale the marks until a badge is roughly 30px, a real target
       for a thumb, without letting the pins swallow the state. 28 units is the
       badge diameter.

       Pure geometry, so it needs no breakpoint: on a wide screen the ratio lands
       under 1 and the Math.max pins it there. This used to be gated on a 620px
       width test, which is why a tablet drew its badges at 20px for no reason. */
    mscale = Math.max(1, Math.min(3.4, 30 / (28 * ctm())));

    var xs = [], ys = [];
    for (var i = 0; i < marks.length; i++) {
      if (!/pinmk/.test(marks[i].getAttribute('class') || '')) continue;
      xs.push(+marks[i].getAttribute('data-x'));
      ys.push(+marks[i].getAttribute('data-y'));
    }
    /* The bbox is of ANCHORS, but a badge sits up to LEAD_MIN from its anchor
       and is drawn at mark scale, so the ink reaches about 27 plus a 16 radius
       beyond it, all scaled. Padding by less fits the anchors and leaves a
       badge hanging off the edge. */
    var pad = 45 * mscale;
    var x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    if (xs.length) {
      x0 = Math.min.apply(null, xs) - pad; x1 = Math.max.apply(null, xs) + pad;
      y0 = Math.min.apply(null, ys) - pad; y1 = Math.max.apply(null, ys) + pad;
    }

    /* THE HOME VIEW FRAMES ALASKA, NOT THE PINS.
       Fitting the pin bbox alone drops the reader into whatever corner the
       decisions happen to cluster in. Right now that is the Railbelt, so the
       map opened zoomed into the east side with the Peninsula and the
       Aleutians cut off and nothing to tell you what you were looking at. The
       state is the subject and the pins are marks on it, so frame the union of
       the coastline and the padded pins: the whole shape reads, and no badge
       hangs off an edge. */
    var coast = mz.querySelector('.coast'), cb = null;
    if (coast && coast.getBBox) { try { cb = coast.getBBox(); } catch (e) { cb = null; } }
    if (cb && cb.width && cb.height) {
      x0 = Math.min(x0, cb.x); x1 = Math.max(x1, cb.x + cb.width);
      y0 = Math.min(y0, cb.y); y1 = Math.max(y1, cb.y + cb.height);
    }
    if (x1 <= x0 || y1 <= y0) {
      inset = 0; k = 1; minK = 1; tx = 0; ty = 0; clampT();
      home = { k: k, tx: tx, ty: ty };
      return;
    }

    /* THE DECISION IS GEOMETRIC, NOT A BREAKPOINT.
       Leave the drawing alone when the state and its pins already fit the frame
       at rest, and zoom out to them when they do not. A width test got this
       wrong in both directions: a landscape phone is 750 wide so it counted as
       a big screen, but slice left the frame 312 units tall and the
       northernmost pin was cropped clean off the map. */
    /* The site nav is sticky, so scrolled to the right place it sits over the
       top of the map. Work out that band FIRST, because a pin sitting inside
       the frame but underneath the nav is not visible, and testing the fit
       without it is how a tablet ended up hiding its northernmost pin while
       reporting that everything was on screen. Capped, or the nav would be
       allowed to eat the whole map on a short frame.

       The cap is 0.36 rather than a rounder 0.3 because a landscape phone
       gives the map a 219px frame under a 71px nav, so the real band IS 32
       percent of it. Capping under the truth does not make the nav smaller, it
       just moves a pin under it, which is what a 0.3 cap did to the Cook Inlet
       pin. The map still keeps roughly two thirds of its frame. */
    var nav = document.querySelector('.topnav');
    var top = Math.min(nav ? nav.getBoundingClientRect().height * px() : 0, v.h * 0.36);

    var fits = (x1 - x0) <= v.w && (y1 - y0) <= (v.h - top) &&
               x0 >= v.x0 && x1 <= v.x1 && y0 >= (v.y0 + top) && y1 <= v.y1;
    if (fits) {
      inset = 0; k = 1; minK = 1; tx = 0; ty = 0; clampT();
      home = { k: k, tx: tx, ty: ty };
      return;
    }
    inset = top;
    var uy0 = v.y0 + top, uh = Math.max(40, v.h - top);
    /* The floor is NOT 1. preserveAspectRatio is slice, so the drawing is
       scaled to COVER the frame and the whole state is off screen at rest on
       almost every viewport. Getting it back means shrinking past the point of
       filling the frame, and a map with a little empty background beside it is
       far better than one with the Aleutians cut off. */
    k = Math.min(8, Math.max(0.28, Math.min(v.w / (x1 - x0), uh / (y1 - y0))));
    minK = Math.min(1, k);
    tx = (v.x0 + v.x1) / 2 - ((x0 + x1) / 2) * k;
    ty = (uy0 + v.y1) / 2 - ((y0 + y1) / 2) * k;
    clampT();
    home = { k: k, tx: tx, ty: ty };
  }

  /* Wheel zooms only with a modifier, so a plain scroll past the map still
     scrolls the page. Pinch on a trackpad arrives as ctrlKey and is honoured. */
  mapsvg.addEventListener('wheel', function(e){
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    var p = toVB(e);
    zoomAt(k * (e.deltaY < 0 ? 1.16 : 1 / 1.16), p.x, p.y);
  }, { passive: false });

  mapsvg.addEventListener('dblclick', function(e){
    var p = toVB(e);
    zoomAt(k * 1.9, p.x, p.y);
  });

  var pts = {}, n = 0, last = null, pinchD = 0, moved = 0;
  mapsvg.addEventListener('pointerdown', function(e){
    pts[e.pointerId] = { x: e.clientX, y: e.clientY };
    n++; moved = 0;
    if (n === 1) { last = { x: e.clientX, y: e.clientY }; }
    if (n === 2) { pinchD = 0; }
  });
  mapsvg.addEventListener('pointermove', function(e){
    if (!pts[e.pointerId]) return;
    pts[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(pts);
    if (ids.length === 1 && last) {
      var s = px();
      var dx = (e.clientX - last.x) * s, dy = (e.clientY - last.y) * s;
      moved += Math.abs(dx) + Math.abs(dy);
      if (k > 1) {
        e.preventDefault();
        tx += dx; ty += dy; clampT(); apply();
      }
      last = { x: e.clientX, y: e.clientY };
    } else if (ids.length === 2) {
      e.preventDefault();
      var a = pts[ids[0]], b = pts[ids[1]];
      var d = Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
      if (pinchD) {
        var r = mapsvg.getBoundingClientRect(), s2 = px();
        zoomAt(k * (d / pinchD),
               ((a.x + b.x) / 2 - r.left) * s2, ((a.y + b.y) / 2 - r.top) * s2);
      }
      pinchD = d;
    }
  });
  function endPointer(e){
    if (pts[e.pointerId]) { delete pts[e.pointerId]; n = Math.max(0, n - 1); }
    if (!n) { last = null; pinchD = 0; }
  }
  mapsvg.addEventListener('pointerup', endPointer);
  mapsvg.addEventListener('pointercancel', endPointer);
  /* A drag must not fire the pin link it happened to start on. */
  mapsvg.addEventListener('click', function(e){
    if (moved > 12) { e.preventDefault(); e.stopPropagation(); }
  }, true);

  /* Activating a label focuses its control, and the browser then scrolls that
     control into view. The layer checkboxes have to sit BEFORE the svg for the
     sibling combinator to reach them, so they live at the top of the map while
     their chips are below it, and every toggle smooth-scrolled the reader
     hundreds of pixels away from the thing they just tapped.

     So when script is running, the label click is handled here and the default
     is prevented, which flips the checkbox without ever focusing it. The native
     label still works with no script, and the checkbox is still reachable and
     operable by keyboard, which is the path that actually wants focus. */
  var chips = document.querySelectorAll('.lyrbar label[for]');
  for (var ci = 0; ci < chips.length; ci++) {
    chips[ci].addEventListener('click', function(e){
      var box = document.getElementById(this.getAttribute('for'));
      if (!box) { return; }
      e.preventDefault();
      box.checked = !box.checked;
      showNote(box.id);
    });
  }

  /* One note at a time, out of the flow, in a block tall enough for the tallest
     of them. Every note is measured at the current width rather than guessed,
     so this holds at 320px and at 1024px without a table of magic numbers. */
  var notesBox = document.querySelector('.lyrnotes');
  var notes = notesBox ? notesBox.querySelectorAll('.lyrnote') : [];
  function sizeNotes(){
    if (!notesBox || !notes.length) { return; }
    notesBox.classList.remove('stable');
    var tallest = 0;
    for (var i = 0; i < notes.length; i++) {
      var was = notes[i].style.display;
      notes[i].style.display = 'block';
      tallest = Math.max(tallest, notes[i].getBoundingClientRect().height);
      notes[i].style.display = was;
    }
    notesBox.classList.add('stable');
    notesBox.style.minHeight = Math.ceil(tallest + 10) + 'px';
  }
  function showNote(id){
    if (!notesBox) { return; }
    var want = id && id.indexOf('lyr-') === 0 ? 'n-' + id.slice(4) : null;
    var box = want ? document.getElementById(id) : null;
    for (var i = 0; i < notes.length; i++) { notes[i].classList.remove('show'); }
    if (want && box && box.checked) {
      var n = notesBox.querySelector('.' + want);
      if (n) { n.classList.add('show'); return; }
    }
    /* Whatever was turned off, fall back to a layer that is still on, so the
       block is not left blank while a layer is still drawn on the map. */
    for (i = 0; i < notes.length; i++) {
      var key = (notes[i].className.match(/n-([a-z]+)/) || [])[1];
      var cb = key ? document.getElementById('lyr-' + key) : null;
      if (cb && cb.checked) { notes[i].classList.add('show'); return; }
    }
  }
  sizeNotes();
  showNote(null);

  /* Buttons, because ctrl and scroll is not something a reader can be
     expected to guess, and on a phone there is no wheel at all. They are
     revealed only once the script is running, so a no-script page never
     shows a control that would do nothing. */
  var ctl = document.getElementById('mapzoomctl');
  if (ctl) ctl.hidden = false;
  function step(f){ zoomAt(k * f, VBW / 2, VBH / 2); }
  var zin = document.getElementById('mapin'), zout = document.getElementById('mapout');
  if (zin) zin.addEventListener('click', function(){ step(1.6); });
  if (zout) zout.addEventListener('click', function(){ step(1 / 1.6); });
  if (reset) {
    reset.addEventListener('click', function(){
      k = home.k; tx = home.tx; ty = home.ty; clampT(); apply();
    });
  }
  var rt = null;
  addEventListener('resize', function(){
    clearTimeout(rt);
    rt = setTimeout(function(){ fit(); apply(); }, 180);
  });
  fit(); apply();
  mapsvg.classList.add('zoomable');
}
})();
"""


MAP_CSS = """/* A clustered badge is a rect and its numbers are the links, so the circle rule
   above cannot reach them. CSS beats a presentation attribute, so this wins
   over the fill set on the element. */
.maphero a .pinnum{transition:fill .2s;}
.maphero a:hover .pinnum{fill:var(--snow);}
/* The dot is the truth, sitting exactly on the coordinate. The badge is placed
   for legibility and the lead line shows how far it had to go to get there. */
.pindot{opacity:.95;}
.pinlead{stroke-width:1.1;opacity:.5;stroke-dasharray:2 3;}
@media (max-width:760px){
  /* The map's own aspect is 1000 by 620, so at 390px wide it renders 242px tall
     and the state is a smear across the top of the screen with 5px pins. Give
     it real height and let preserveAspectRatio slice crop the sides instead;
     the opening view is fitted to the pins, so nothing that matters is cropped
     out, and the scale roughly triples. */
  .maphero svg{height:min(64vh,540px);}
  .lyrbar{padding-top:16px;}
  .lyrnote{font-size:12.5px;}
}
/* ---------- map layers, toggled with a checkbox and no script ----------
   The grid is drawn white rather than in any pin colour, so infrastructure
   never reads as a docket item. Weight carries the voltage: a 230 kV ring is
   a different kind of fact from a 69 kV spur and should not look the same. */
.gx{fill:none;stroke:#dcebff;stroke-linecap:round;stroke-linejoin:round;}
.gx-t1{stroke-width:1.1;opacity:.40;}
.gx-t2{stroke-width:1.9;opacity:.56;}
.gx-t3{stroke-width:3;opacity:.78;}
/* TAPS is oil, not power, so it is dashed rather than another solid thread that
   would read as more grid. Copper, NOT the amber the closed pins use: the first
   pass made this #f2a43a and the pipeline read as a line of settled decisions. */
.tp{fill:none;stroke:#b5794a;stroke-width:2.2;opacity:.75;stroke-dasharray:7 5;
stroke-linecap:round;}
/* Generation. Area is megawatts, so a plant twice the size gets twice the ink,
   where doubling the radius would quadruple it and flatter the big plants.
   One colour, not one per fuel: this map already asks a reader to hold three
   pin colours and a grid, and fuel type is in the tooltip where it belongs. */
.gen{fill:#a78bd0;fill-opacity:.26;stroke:#c9b4ee;stroke-width:1;stroke-opacity:.6;}
.lyr{transition:opacity .4s ease;}
/* FIXED, not absolute. The checkbox has to sit before the svg for the sibling
   combinator to reach it, which put it at the TOP of the map. Tapping a chip
   below the map focuses it, and the browser scrolls a focused control into
   view, so every toggle threw the reader 363px back up the page. A fixed
   element is always within the viewport, so there is nothing to scroll to. */
.lyrbox{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;margin:0;
clip-path:inset(50%);pointer-events:none;}
.lyr-grid,.lyr-gen,.lyr-taps{opacity:0;pointer-events:none;}
#lyr-grid:checked ~ svg .lyr-grid,
#lyr-gen:checked ~ svg .lyr-gen,
#lyr-taps:checked ~ svg .lyr-taps{opacity:1;}
#lyr-gen:checked ~ svg .lyr-gen{pointer-events:auto;}
.lyrbar{padding:14px 2px 0;}
.lyrchips{display:flex;gap:10px;flex-wrap:wrap;}
.lyrbar label{display:inline-flex;align-items:center;gap:9px;cursor:pointer;flex:none;
font-family:JBMono,monospace;font-size:11px;letter-spacing:.14em;color:var(--mute);
border:1px solid var(--line);border-radius:999px;padding:0 16px 0 12px;
min-height:44px;-webkit-tap-highlight-color:transparent;
transition:color .2s,border-color .2s,background .2s;}
.lyrbar label:hover{color:var(--snow);border-color:#2c5876;}
.lyrbar label .sw{width:9px;height:9px;border-radius:50%;border:1.5px solid currentColor;
flex:none;transition:background .2s,box-shadow .2s;}
#lyr-grid:checked ~ .lyrbar label[for="lyr-grid"],
#lyr-gen:checked ~ .lyrbar label[for="lyr-gen"],
#lyr-taps:checked ~ .lyrbar label[for="lyr-taps"]{color:var(--snow);border-color:#3a6f96;
background:rgba(90,200,240,.07);}
#lyr-grid:checked ~ .lyrbar label[for="lyr-grid"] .sw{background:#dcebff;
box-shadow:0 0 9px rgba(220,235,255,.8);}
#lyr-gen:checked ~ .lyrbar label[for="lyr-gen"] .sw{background:#c9b4ee;
box-shadow:0 0 9px rgba(201,180,238,.8);}
#lyr-taps:checked ~ .lyrbar label[for="lyr-taps"] .sw{background:#c98a5c;
box-shadow:0 0 9px rgba(201,138,92,.8);}
.lyrbox:focus-visible ~ .lyrbar label{outline:2px solid var(--gold);outline-offset:3px;}
/* Each note appears only while its own layer is on, so the bar stays one line
   of chips until a reader actually asks what they are looking at. */
/* The notes must not change the page's height, or every toggle reflows the
   document and the browser scrolls to compensate, dragging the chip out from
   under the reader's thumb. On an iPad in landscape that was a 1099px jump.
   With script running the notes come OUT of the flow, one shows at a time, and
   the block reserves the height of the tallest so nothing ever moves. With no
   script they simply stack, which reflows but at least reads correctly. */
.lyrnotes{padding-top:2px;}
.lyrnotes.stable{position:relative;}
.lyrnotes.stable .lyrnote{position:absolute;left:0;right:0;top:0;display:none;}
.lyrnotes.stable .lyrnote.show{display:block;}
.lyrnote{display:none;font-size:12px;line-height:1.6;color:var(--mute);max-width:70ch;
padding-top:10px;}
/* The no-script path, and ONLY the no-script path. These carry an id, so they
   outrank .lyrnotes.stable .lyrnote on specificity and source order cannot take
   it back. Unscoped, every checked layer forced display:block while the stable
   rule still pinned each note to top:0, so turning on all three layers printed
   three notes through each other into an unreadable smear. :not(.stable) hands
   the notes to the script the moment the script claims them. */
#lyr-grid:checked ~ .lyrbar .lyrnotes:not(.stable) .n-grid,
#lyr-gen:checked ~ .lyrbar .lyrnotes:not(.stable) .n-gen,
#lyr-taps:checked ~ .lyrbar .lyrnotes:not(.stable) .n-taps{display:block;}
@media (prefers-reduced-motion:reduce){.lyr{transition:none;}}
/* ---------- pan and zoom ----------
   Strokes must not thicken with the zoom, or the grid turns into ribbons the
   moment anyone looks closely. pan-y keeps the page scrollable on a phone:
   the map takes horizontal drags and pinches, the page keeps vertical ones. */
.maphero svg .gx,.maphero svg .tp,#mzoom>path{vector-effect:non-scaling-stroke;}
.maphero svg.zoomable{touch-action:pan-y;}
.maphero svg.zoomable .mk{cursor:pointer;}
.mapzoomctl{display:inline-flex;gap:8px;}
.mapzoomctl[hidden]{display:none;}
.mapzoomctl button{font-family:JBMono,monospace;font-size:11px;letter-spacing:.14em;
color:var(--mute);background:transparent;border:1px solid var(--line);border-radius:999px;
min-height:44px;min-width:44px;padding:0 14px;cursor:pointer;
transition:color .2s,border-color .2s,background .2s;}
.mapzoomctl button:hover{color:var(--snow);border-color:#2c5876;}
#mapin,#mapout{font-size:17px;line-height:1;padding:0;}
/* FIT ALASKA holds its space at all times and only becomes visible when the
   map has actually moved. Using the hidden attribute made it appear from
   nothing, which rewrapped the chip row by 54px and shoved the zoom button out
   from under the reader's thumb mid-tap. */
.mapreset{color:var(--gold);background:rgba(255,199,44,.08);
border-color:rgba(255,199,44,.4);visibility:hidden;}
.mapreset:hover{background:rgba(255,199,44,.16);border-color:var(--gold);}
.mapreset.on{visibility:visible;}
/* ---------- status filter ----------
   Three checkboxes, all on. A pin shows if ANY of its statuses is still on,
   which falls out of these rules being independent rather than exclusive. */
.pinmk{opacity:.13;transition:opacity .3s;}
#f-open:checked ~ svg .pinmk.a-open,
#f-indirect:checked ~ svg .pinmk.a-indirect,
#f-closed:checked ~ svg .pinmk.a-closed{opacity:1;}
.lyrbar label[for^="f-"]{border-style:dashed;}
#f-open:checked ~ .lyrbar label[for="f-open"] .sw{background:var(--green);
box-shadow:0 0 9px rgba(60,230,180,.7);}
#f-indirect:checked ~ .lyrbar label[for="f-indirect"] .sw{background:#8da2be;
box-shadow:0 0 9px rgba(141,162,190,.7);}
#f-closed:checked ~ .lyrbar label[for="f-closed"] .sw{background:var(--amber);
box-shadow:0 0 9px rgba(242,164,58,.7);}
#f-open:checked ~ .lyrbar label[for="f-open"],
#f-indirect:checked ~ .lyrbar label[for="f-indirect"],
#f-closed:checked ~ .lyrbar label[for="f-closed"]{color:var(--snow);border-color:#3a6f96;
border-style:solid;background:rgba(90,200,240,.07);}
@media (prefers-reduced-motion:reduce){.pinmk{transition:none;}}"""


JS = """
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
    if (/^(localhost|127\\.|0\\.0\\.0\\.0|\\[?::1)/.test(location.hostname) ||
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
    el.dataset.counted = '1';
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
"""


def page(title, desc, body, prefix, active, today, site_url, path, og_image="og.png",
         og_size=(1200, 630), ld=None, crumbs=None, noindex=False,
         extra_css="", extra_js="", extra_head=""):
    # Per-page CSS and JS. The docket map's styling and its pan and zoom are
    # about 4 KB gzipped, and before this existed they rode the shared bundle
    # onto all 25 pages, which made a page with no map on it 15 percent heavier
    # for nothing. Most readers are on a phone, so that is not a rounding error.
    # The shared bundle is linked, not inlined. It is ~40 KB (27 KB of rules
    # plus a 13 KB grain data URI) and it used to be stamped into all 26 pages,
    # which meant a crawler reading a deck page got 82 KB of HTML carrying
    # 4 KB of story. Linking it makes the bundle cacheable across the whole
    # site and drops the per-page weight by about 46 KB.
    #
    # Relative url() in CSS resolves against the stylesheet, not the document,
    # and site.css sits at the root beside fonts/, so FONTPREFIX is empty there.
    canonical = f"{site_url}/{path}"
    og_url = og_image if og_image.startswith("http") else f"{site_url}/{og_image}"
    blocks = []
    if ld:
        blocks.append(ld)
    if crumbs:
        blocks.append(breadcrumb_ld(site_url, crumbs))
    ld_html = "".join(
        f'<script type="application/ld+json">{ld_json(b)}</script>'
        for b in blocks)
    robots_html = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    preload = "".join(
        f'<link rel="preload" href="{prefix}fonts/{f}" as="font" type="font/woff2" crossorigin>'
        for f in ("fraunces.woff2", "manrope.woff2", "jbmono-md.woff2"))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots_html}<meta name="theme-color" content="#02060f">
<meta property="og:site_name" content="Alaska AI">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="{og_size[0]}">
<meta property="og:image:height" content="{og_size[1]}">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="Alaska AI, articles" href="{site_url}/feed.xml">
<link rel="alternate" type="application/atom+xml" title="Alaska AI, articles" href="{site_url}/atom.xml">
<link rel="alternate" type="application/feed+json" title="Alaska AI, articles" href="{site_url}/feed.json">
<link rel="alternate" type="application/rss+xml" title="Alaska AI, docket changes" href="{site_url}/docket/feed.xml">
{extra_head}<link rel="icon" href="{ak_favicon()}">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{preload}
{ld_html}
<link rel="stylesheet" href="{prefix}site.css">
{('<style>' + extra_css + '</style>') if extra_css else ''}
<script>document.documentElement.classList.add('js');window.__revealFallback=setTimeout(function(){{document.documentElement.classList.add('reveal-fallback')}},3000)</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="sky"><div class="stars"></div><div class="curtain"></div><div class="curtain c2"></div>{flag_sky() if active in ('home', 'services') else ''}
<div class="veil v1"></div><div class="veil v2"></div><div class="veil v3"></div>
<div class="meteor"></div></div>
<div class="wrap">
{nav(prefix, active)}
<main id="main">
{body}
</main>
{footer(prefix, today)}
</div>
<script src="{prefix}site.js" defer></script>
{('<script>' + extra_js + '</script>') if extra_js else ''}
</body>
</html>"""


# ---------- data loading ----------

def load_docket(today):
    ledger = json.loads((REPO / "ledger/docket.json").read_text())
    items = ledger["items"]
    db.validate(items)
    live = [it for it in items if it["status"] in ("open-for-comment", "pending-decision", "watching")]
    done = [it for it in items if it["status"] in ("decided", "closed")]
    # Order by the date each item actually DISPLAYS, not by when it next moves.
    #
    # Those are different values, and sorting by one while showing the other is
    # how a sort key becomes a rendered fact: dated[0] supplies the home page's
    # headline TITLE while the date beside it came from whichever item resolved
    # soonest, and dated[:6] decides which cards exist at all. Sorted by
    # next_event, the AIDEA item leads on its AUG 13 vote and then prints AUG 19,
    # so a second item closing AUG 15 would put its date next to AIDEA's title.
    # That is the same defect as the AUG 13 button, arriving through ordering
    # instead of through selection.
    #
    # The set is identical either way, since headline is deadline-or-next-event
    # and a future deadline is always a future event. Only the order changes.
    dated = sorted((it for it in live if db.resolve(it, today)["headline"]),
                   key=lambda it: db.resolve(it, today)["headline"]["date"])
    live_sorted = dated + [it for it in live if not db.resolve(it, today)["headline"]]
    return items, live, done, dated, live_sorted


# claims.json is the run's verified record: every number and quote the
# fact-checker re-fetched, with the URL it was proved against. It is the most
# expensive thing a run produces, and it arrives in a different shape almost
# every day, because the fact-checker is an agent and nothing pinned its
# schema. Across 18 runs the container has been "claims", "verified_claims" and
# "docket_claims", and the same field has been called claim/text/statement,
# source_url/url/evidence_url, source_outlet/outlet/publisher.
#
# Reading tolerantly is what makes the whole archive legible rather than only
# the four runs that happened to use the newest shape. Phase F pins the schema
# going forward; this keeps the back catalogue working regardless.
CLAIM_CONTAINERS = ("claims", "verified_claims", "docket_claims", "claims_verified")
CLAIM_FIELDS = {
    "id":       ("id", "claim_id"),
    "claim":    ("claim", "text", "statement"),
    "value":    ("value", "value_detail", "number_or_date", "figure"),
    "url":      ("source_url", "url", "evidence_url", "link"),
    "outlet":   ("source_outlet", "outlet", "publisher", "source"),
    "date":     ("date_of_source", "source_date", "published", "pub_date", "date"),
    "verbatim": ("verbatim", "verbatim_quote", "verbatim_support"),
}
# A source is primary when the run says so outright, or when the credibility
# or tier field it used instead means the same thing.
PRIMARY_WORDS = ("primary", "official", "filing", "government", "tier1", "tier 1")


# When a claim field holds a nested object rather than a string, which key
# inside it answers the question being asked. This is per logical field on
# purpose: a single shared order meant asking for the outlet returned the
# nested url, and a source archive that prints a URL where the outlet goes
# looks exactly like the thing this publication says it is not.
NESTED_KEYS = {
    "url":      ("url", "source_url", "link", "href"),
    "outlet":   ("outlet", "source_outlet", "publisher", "name", "source"),
    "date":     ("pub_date", "date", "published", "source_date", "date_of_source"),
    "claim":    ("claim", "text", "statement"),
    "value":    ("value", "figure", "number"),
    "verbatim": ("verbatim", "quote", "verbatim_quote", "text"),
    "id":       ("id", "claim_id"),
}


def _first(d, keys, field=None):
    """First non-empty value among `keys`, descending one level into the
    nested evidence objects some runs used instead of flat fields.

    `field` names what is being asked for, so the descent looks for the right
    thing. Without it a nested object is not descended into at all, which is
    safer than guessing."""
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, (int, float)):
            return str(v)
        # One run recorded evidence as [{"url":..., "outlet":..., "pub_date":...}]
        # rather than as flat source_url/source_outlet fields.
        if isinstance(v, list) and v and isinstance(v[0], dict):
            v = v[0]
        if isinstance(v, dict) and field:
            for kk in NESTED_KEYS.get(field, ()):
                if isinstance(v.get(kk), str) and v[kk].strip():
                    return v[kk].strip()
    return ""


def _evidence_bits(c):
    """url/outlet/date pulled from a nested evidence object, when the run put
    them there instead of on the claim itself."""
    for k in ("evidence", "sources", "source"):
        v = c.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            v = v[0]
        if isinstance(v, dict):
            return (_first(v, ("url", "source_url", "link"), "url"),
                    _first(v, ("outlet", "source_outlet", "publisher"), "outlet"),
                    _first(v, ("pub_date", "date", "published", "source_date"), "date"))
    return "", "", ""


def _looks_like_claims(rows):
    """A list of dicts is a claim list when most entries carry a statement and
    a source. Lets a run name its container anything (two runs used the story
    codenames "beluga" and "caribou_fallback") without the archive going dark."""
    if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
        return False
    hits = sum(1 for c in rows if isinstance(c, dict)
               and _first(c, CLAIM_FIELDS["claim"], "claim")
               and (_first(c, CLAIM_FIELDS["url"], "url") or _evidence_bits(c)[0]))
    # Floor of 1, not 2. A floor of 2 meant a one-claim list was never
    # recognised as claims at all, so a thin run would have published an empty
    # verification record rather than its single sourced claim. Real runs carry
    # 15 to 85, so this never bit in production, but the rule was wrong.
    return hits >= max(1, len(rows) // 2)


# Container names whose contents must NEVER be published, even when they are
# claim-shaped. A fact-checker's dropped/killed lists were already skipped; the
# unverified family was not, so a run that named its container 'story_claims'
# (the exact schema drift the tolerant reader exists to absorb) let the
# last-resort scan reach an 'unverified_but_reported' list and publish it under
# the "each re-fetched from its source" heading. That list's own record said
# "the deck MUST NOT attribute a policy motive to these donors".
_EXCLUDED_CONTAINER_WORDS = (
    "drop", "kill", "reject", "unresolved", "unverified", "unconfirmed",
    "not_verified", "notverified", "must_not", "mustnot", "discard",
    "excluded", "exclude", "quarantine", "hold", "review_needed")


def _excluded_container(key):
    k = str(key).lower()
    return any(w in k for w in _EXCLUDED_CONTAINER_WORDS)


def _claim_rows(doc):
    """Every claim-shaped list in the document, whatever it was named and
    however deeply the run nested it.

    Order matters here because a document can hold more than one claim-shaped
    list. On 2026-07-21 the run carried two, 'beluga' (16, the story that
    shipped) and 'caribou_fallback' (6), and selected by dict-iteration order,
    which is not a decision. Reordering the same file, or the fact-checker
    naming its containers differently, could publish the wrong story's
    verification record under a deck it does not belong to. So an explicit
    pointer wins over every heuristic, and the unverified family is skipped."""
    # 1. The run's own statement of which story shipped, if it names a
    #    container that resolves to claims. A pointer that names nothing
    #    (a human-readable "story" sentence, a story_id with no matching
    #    container) resolves to None and falls through untouched.
    for ptr_key in ("selected_story", "selected", "story_id", "chosen"):
        ptr = doc.get(ptr_key)
        if not isinstance(ptr, str):
            continue
        target = doc.get(ptr)
        if _looks_like_claims(target):
            return target
        if isinstance(target, dict) and _looks_like_claims(target.get("claims")):
            return target["claims"]
    # 2. A canonical claims container.
    for key in CLAIM_CONTAINERS:
        if _looks_like_claims(doc.get(key)):
            return doc[key]
    # 3. Claims kept inside the story object they belong to.
    for key in ("stories", "selected_story", "story"):
        v = doc.get(key)
        v = v if isinstance(v, list) else ([v] if isinstance(v, dict) else [])
        rows = [c for s in v if isinstance(s, dict)
                for c in (s.get("claims") or []) if isinstance(c, dict)]
        if _looks_like_claims(rows):
            return rows
    # 4. Last resort: any top-level list that reads like claims, never one the
    #    run marked as dropped, killed, rejected, or unverified.
    for key, v in doc.items():
        if _excluded_container(key):
            continue
        if _looks_like_claims(v):
            return v
    return []


def _iso_date_or_blank(s):
    """A source date if the field holds one, else empty.

    The field used to be blindly sliced to [:10], which turned the string
    'current EPA listing' into the chip 'current EP' and published it as a
    schema.org datePublished, and 'n/a' / 'background' / 'n.d.' the same way.
    That is fabrication, not degradation: a date the run did not record is
    dropped, not manufactured from a prefix. Accepts a full or reduced-
    precision ISO date (YYYY, YYYY-MM, YYYY-MM-DD), optionally followed by a
    time, which is where the useful part of the old [:10] slice lived."""
    s = (s or "").strip()
    m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?(?:[T ].*)?$", s)
    if not m:
        return ""
    y, mo, day = m.group(1), m.group(2), m.group(3)
    try:
        if day:
            return ddate(int(y), int(mo), int(day)).isoformat()
        if mo:
            if not 1 <= int(mo) <= 12:
                return ""
            return f"{y}-{mo}"
        return y
    except ValueError:
        return ""


def _outlet_from_url(url):
    """A readable outlet name derived from a URL host, for claims whose run
    record carried a source URL but no outlet field.

    Two runs recorded the outlet only as source_title, which is an article
    headline ('Digital twin of Alaska permafrost ... (Phys.org)'), not an
    outlet, so 99 claims published as the literal word 'source' and
    'Uncredited source' became the largest row on the source archive. The host
    is the honest outlet when the field is absent and the URL is right there;
    'Uncredited source' stays only for claims that genuinely have neither."""
    try:
        from urllib.parse import urlparse
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return ""
    if not host:
        return ""
    host = host[4:] if host.startswith("www.") else host
    return host


def normalize_claims(doc):
    """Every shape of claims.json the runs have produced, as one dict keyed by
    claim id. Unknown shapes yield nothing rather than a broken page."""
    rows = _claim_rows(doc)
    if not rows:
        return {}

    out = {}
    for i, c in enumerate(rows, 1):
        if not isinstance(c, dict):
            continue
        text = _first(c, CLAIM_FIELDS["claim"], "claim")
        if not text:
            continue
        ev_url, ev_outlet, ev_date = _evidence_bits(c)
        url = _first(c, CLAIM_FIELDS["url"], "url") or ev_url
        # Must be a real fetchable URL. One run recorded source_url as the
        # literal "DERIVED" for a ratio computed from two other verified
        # claims. That is honest bookkeeping and a broken link on the page, and
        # a section headed "each re-fetched from its source" should not carry a
        # claim that was never fetched. Derived claims stay out of the record.
        if not url.lower().startswith(("http://", "https://")):
            continue
        cid = _first(c, CLAIM_FIELDS["id"], "id") or f"C{i:02d}"
        primary = c.get("source_is_primary")
        if primary is None:
            primary = c.get("primary")
        if primary is None:
            blob = " ".join(str(c.get(k, "")) for k in
                            ("credibility", "tier", "source_type", "status")).lower()
            primary = any(w in blob for w in PRIMARY_WORDS)
        out[cid] = {
            "id": cid,
            "claim": text,
            "value": _first(c, CLAIM_FIELDS["value"], "value"),
            "source_url": url,
            "source_outlet": (_first(c, CLAIM_FIELDS["outlet"], "outlet")
                              or ev_outlet or _outlet_from_url(url)),
            "source_is_primary": bool(primary),
            "date_of_source": _iso_date_or_blank(
                _first(c, CLAIM_FIELDS["date"], "date") or ev_date),
            "verbatim": _first(c, CLAIM_FIELDS["verbatim"], "verbatim"),
        }
    return out


def load_runs():
    out = []
    for d in sorted((REPO / "runs").iterdir(), reverse=True):
        if not d.is_dir():
            continue
        try:
            copy = json.loads((d / "copy.json").read_text())
            asm = json.loads((d / "assemble_report.json").read_text())
            caption = (d / "caption.txt").read_text().strip()
        except Exception:
            continue
        try:
            claims = normalize_claims(json.loads((d / "claims.json").read_text()))
        except Exception:
            claims = {}
        out.append({
            "date": d.name,
            # Title reads document_title, then the aliases two runs used, then
            # falls back to the date. 2026-07-20 recorded its headline under
            # 'title', so with no fallback its <title>, <h1>, og:title and
            # JSON-LD all published the raw date string '2026-07-20'.
            #
            # And it runs through house(), same as claim text and outlet names,
            # rather than a bare ": " -> ", " replace. house() exists precisely
            # so a source's em dash or curly quote cannot take the whole build
            # down at the punctuation gate; the title and hook were the last two
            # run-record strings reaching a page without it, so one bad
            # character in any of 19 titles failed every future build.
            "title": house(copy.get("document_title") or copy.get("title")
                           or copy.get("deck_title") or d.name),
            "hook": house(caption.split("\n")[0].strip()),
            "caption": caption,
            "first_comment": copy.get("first_comment", ""),
            "summary": copy.get("deck_summary_line", ""),
            "slide_data": copy.get("slide_copy") or copy.get("slides"),
            "claims": claims,
            "hashtags": copy.get("hashtags", []),
            "slides": asm.get("slides", 0),
            # Measured off the file, not read from assemble_report.json. The
            # report records the size at assembly time, and the PDF is
            # resampled after that, so the reported figure was a download size
            # the reader would never see. The file on disk is the download.
            "pdf_mb": (round((d / "carousel.pdf").stat().st_size / 1048576, 2)
                       if (d / "carousel.pdf").exists() else asm.get("pdf_mb", 0)),
        })
    return out


HEAD_KEYS = ("headline", "head", "hero", "display", "hook", "title", "hook_lines")
BODY_KEYS = ("body", "dek", "sub", "subhead", "text", "overline", "supporting")


def _slide_text(entry, keys):
    """Pull the first present text field from a per-slide dict. Each run's
    copywriter invents its own schema (head/body, headline/dek, hook_lines,
    nested {text} objects), so read tolerantly."""
    for k in keys:
        v = entry.get(k)
        if isinstance(v, dict):
            v = v.get("text", "")
        if isinstance(v, list):
            v = " ".join(str(x) for x in v)
        if isinstance(v, str) and v.strip():
            return " ".join(v.split())
    return ""


def slide_entries(r):
    """Per-slide copy as {slide number: dict}, whatever shape the run used.

    Every run's copywriter invents its own container. Across 18 runs the slide
    copy has arrived as a list, as a dict keyed "01", as one keyed "S1", and as
    one keyed "slide-01". Anything that reads slide copy goes through here, so
    a new shape is fixed in one place instead of silently rendering nothing."""
    data = r.get("slide_data")
    entries = {}
    if isinstance(data, list):
        for idx, s in enumerate(data, 1):
            if not isinstance(s, dict):
                continue
            num = str(s.get("slide", s.get("n", idx))).lstrip("S0") or str(idx)
            if num.isdigit():
                entries[int(num)] = s
    elif isinstance(data, dict):
        for k, s in data.items():
            num = re.sub(r"^(slide[-_]?|S)", "", str(k), flags=re.I).lstrip("0") or "0"
            if not num.isdigit():
                continue
            if isinstance(s, dict):
                entries[int(num)] = s
            elif isinstance(s, list):
                # One run recorded each slide as the flat list of strings set on
                # it, furniture and all. Recover the prose and drop the chrome.
                lines = _prose_lines(s)
                if lines:
                    entries[int(num)] = {"headline": lines[0],
                                         "body": " ".join(lines[1:])}
    return dict(sorted(entries.items()))


# Slide furniture that carries no story: the counter, the wordmark, the
# coordinate stamp, a bare date. Dropped before the rest is read as prose.
_FURNITURE = re.compile(
    r"^(\d+\s*/\s*\d+"                       # 01 / 10
    r"|ALASKA\.?AI"                          # wordmark
    r"|\d+\s*deg\b.*"                        # 58 deg 18'N 134 deg 25'W
    r"|[A-Z]{3}\s+\d{1,2},?\s+\d{4}"         # AUG 18 2026
    r")$", re.I)


def _prose_lines(strings):
    """The lines from a slide's raw string list that read like sentences.

    Wants at least three words and one lowercase letter, which keeps headlines
    and dek lines while dropping set-in-caps labels and stamps."""
    out = []
    for s in strings:
        if not isinstance(s, str):
            continue
        t = " ".join(s.split())
        if not t or _FURNITURE.match(t) or len(t) < 12:
            continue
        if len(t.split()) < 3 or not any(c.islower() for c in t):
            continue
        out.append(t)
    return out


def slide_alts(r):
    """Descriptive alt text per slide from the run's own per-slide copy, so
    the story inside the PNGs is legible to search engines and screen
    readers."""
    entries = slide_entries(r)
    alts = {}
    for i, s in entries.items():
        head = _slide_text(s, HEAD_KEYS).rstrip(".")
        body = _slide_text(s, BODY_KEYS).rstrip(".")
        text = ". ".join(t for t in (head, body) if t)
        if text:
            alts[i] = text.replace(": ", ", ")[:160]
    return alts


def caption_paragraphs(r):
    """The deck's LinkedIn caption rendered as site paragraphs: the real,
    crawlable text of the story. Drops the hook line (the hero already says
    it), trailing hashtag lines, and anything after the sources label."""
    lines = [l.rstrip() for l in r["caption"].split("\n")]
    if lines and lines[0].strip() == r["hook"]:
        lines = lines[1:]
    kept = []
    for l in lines:
        s = l.strip()
        if s.startswith("#") and " #" in s or (s.startswith("#") and len(s.split()) > 1):
            continue
        if s.lower().rstrip(":") in ("sources", "source"):
            break
        kept.append(l)
    text = "\n".join(kept).strip().replace(": ", ", ")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in paras)






def _anchor_candidates(claim):
    """Strings worth hunting for in a slide's prose so a claim's number can
    become a link to the document it was proved against.

    Ordered widest first. "23 governors" is a better anchor than "23", because
    a bare number matches a counter, a year or another claim's figure."""
    out = []
    value = (claim.get("value") or "").strip()
    if value:
        out.append(value)
        # The copywriter rewrites for the slide, so the recorded value rarely
        # survives intact: "281 total" is set as "281 names", "18 MW" as
        # "18 megawatts". The figure itself is what carries over, so fall back
        # to the leading number. Two digits minimum, because a bare "1" or "5"
        # would land on a counter or an unrelated figure and cite the wrong
        # document, which is worse than not linking at all.
        #
        # Two things are deliberately never anchors. A value that is itself a
        # date ("2026-04-21") would otherwise contribute "2026" and link the
        # year in "introduced on April 21, 2026", which reads as though the
        # year were the fact being verified. And any bare four-digit year is
        # rejected outright, whatever produced it, for the same reason.
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            m = re.match(r"^([\d][\d,.]*)", value)
            if m and len(m.group(1).replace(",", "").replace(".", "")) >= 2:
                out.append(m.group(1))
    return [c for c in dict.fromkeys(out)
            if len(c) >= 2 and not re.fullmatch(r"(19|20)\d{2}", c)]


def claims_html(r, site_url):
    """The run's verification record, rendered as readable text.

    This is the part no other newsroom in the state publishes. Every run
    already re-fetches each source and records what it proved, and that record
    is both the strongest reason to cite this site and, until now, the most
    expensive thing it threw away. Primary documents sort first."""
    claims = (r.get("claims") or {}).values()
    if not claims:
        return "", 0
    rows, n = [], 0
    for c in sorted(claims, key=lambda c: (not c.get("source_is_primary"), c.get("id", ""))):
        text, url = house(c.get("claim")), c.get("source_url")
        if not text:
            continue
        n += 1
        outlet = house(c.get("source_outlet")) or "source"
        when = c.get("date_of_source") or ""
        primary = bool(c.get("source_is_primary"))
        kind = f'<span class="k{" p" if primary else ""}">{"PRIMARY" if primary else "REPORT"}</span>'
        cite = (f'<a class="src" href="{esc(url)}" rel="nofollow noopener" target="_blank">'
                f'{esc(outlet)}</a>' if url else f'<span class="src">{esc(outlet)}</span>')
        meta = f'{kind}{cite}' + (
            f'<span class="d">{esc(when)}</span>' if when else "")
        rows.append(f'<li id="{esc((c.get("id") or "").lower())}">'
                    f'<p>{esc(text)}</p><div class="cmeta">{meta}</div></li>')
    if not rows:
        return "", 0
    return f'<ol class="claims">{"".join(rows)}</ol>', n


def link_claims(text, claim_ids, claims, used):
    """Escape `text` for HTML and turn the figures it states into links to the
    primary documents that prove them.

    This is the difference between a page that asserts a number and a page that
    shows its work. Each claim is spent once per deck (tracked in `used`) so a
    figure repeated across slides links on first use and reads clean after.

    Returns (html, linked_ids)."""
    spans, linked = [], []
    for cid in claim_ids or []:
        c = claims.get(cid)
        if not c or cid in used or not c.get("source_url"):
            continue
        for cand in _anchor_candidates(c):
            pat = re.compile(r"(?<![\w,.])" + re.escape(cand) + r"(?![\w])", re.I)
            hit = next((m for m in pat.finditer(text)
                        if not any(s < m.end() and m.start() < e for s, e, _ in spans)), None)
            if hit:
                spans.append((hit.start(), hit.end(), c))
                used.add(cid)
                linked.append(cid)
                break
    if not spans:
        return esc(text), linked

    spans.sort(key=lambda s: s[0])
    parts, at = [], 0
    for start, end, c in spans:
        parts.append(esc(text[at:start]))
        outlet = c.get("source_outlet") or "the source"
        kind = "primary document" if c.get("source_is_primary") else "report"
        when = c.get("date_of_source") or ""
        title = f"{outlet}, {kind}" + (f", {when}" if when else "")
        cls = "cite primary" if c.get("source_is_primary") else "cite"
        parts.append(f'<a class="{cls}" href="{esc(c["source_url"])}" '
                     f'title="{esc(title)}" rel="nofollow noopener" target="_blank">'
                     f'{esc(text[start:end])}</a>')
        at = end
    parts.append(esc(text[at:]))
    return "".join(parts), linked


def article_html(r):
    """The deck rendered as a readable, indexable article.

    A carousel puts its whole argument inside nine PNGs. A person can read
    those; a crawler, an answer engine and a screen reader cannot, and until
    now a deck page carried about 1.5 KB of story for nine slides of reporting.
    The copywriter already wrote every headline and body line, and the
    fact-checker already tied each one to a fetched source, so the article is
    reconstructed here from the run's own record rather than written twice.

    Slides with no prose (a chart plate, a closing card) contribute their
    headline alone, which is what they say."""
    entries = slide_entries(r)
    claims = r.get("claims") or {}
    if not entries:
        return "", [], ""

    used, cited, blocks, plain = set(), [], [], []
    for n, s in entries.items():
        head = house(_slide_text(s, HEAD_KEYS))
        body = house(_slide_text(s, BODY_KEYS))
        if not head and not body:
            continue
        ids = s.get("claim_ids") or s.get("claims") or []
        chunks = []
        if head:
            h, got = link_claims(head, ids, claims, used)
            cited += got
            chunks.append(f'<h3>{h}</h3>')
            plain.append(head)
        if body:
            b, got = link_claims(body, ids, claims, used)
            cited += got
            chunks.append(f'<p>{b}</p>')
            plain.append(body)
        blocks.append(f'<section class="sl" id="slide-{n:02d}">'
                      f'<span class="sn">{n:02d}</span>{"".join(chunks)}</section>')
    return "".join(blocks), cited, "\n\n".join(plain)


# ---------- standing beats ----------
# Permanent URLs, live whether or not anything ran on the beat this month.
# Alaska's News Source keeps /weather/closings/ up all summer returning an
# empty payload, and the habit and the search ranking survive the off season.
# A beat page that 404s between stories throws that away every time.
#
# The terms are drawn from what the corpus actually contains (the entity and
# keyword frequencies in ledger/topics.json), not from a taxonomy invented in
# advance. The blurbs are written to be read: the Anchorage Daily News authored
# blurbs for its tag pages and never rendered them, which is free ground.
# Each beat carries three names, and they are deliberately not the same string.
#
# "title" is the newsroom's name for the beat and is what the site says in its
# own furniture, where "Data centers" reads correctly because the reader is
# already on Alaska AI. "h1" and "seo" are what a stranger types, and a stranger
# does not search for "data centers" hoping to find Alaska. Measured before this
# split: for "Alaska AI data centers power grid", a query this publication holds
# better primary material on than anyone, the site did not appear at all, while
# /about/ ranked for other queries because it was the one page whose words
# matched what someone would actually search.
#
# "seo" stays under about 60 characters so it survives intact in a result list.
TOPICS = [
    {"slug": "data-centers", "title": "Data centers",
     "h1": "Alaska data centers",
     "seo": "Alaska data centers and the AI buildout - Alaska AI",
     "desc": "Every proposed AI and cloud data center in Alaska, tracked. The land "
             "each one wants, the power it needs, who decides, and whether the "
             "public gets a say.",
     "blurb": "Every proposed AI and cloud campus in Alaska, the land it wants, "
              "the power it needs, and who gets to say yes.",
     "terms": ("data center", "datacenter", "ai campus", "stak energy", "adl 422741",
               "hyperscale", "colocation", "deadhorse", "gigawatt")},
    {"slug": "power-and-the-grid", "title": "Power and the grid",
     "h1": "Alaska power and the grid",
     "seo": "Alaska power grid and AI data center load - Alaska AI",
     "desc": "What AI data centers do to the Alaska power grid. The Railbelt, Cook "
             "Inlet gas, the turbines and the interties, and who pays when a new "
             "load the size of a city plugs in.",
     "blurb": "The Railbelt, Cook Inlet gas, the turbines and the interties. Who "
              "pays when a new load the size of a city plugs in.",
     "terms": ("railbelt", "grid", "turbine", "gvea", "lm6000", "natural gas",
               "cook inlet", "megawatt", "gigawatt", "cost allocation", "off-grid",
               "utility", "intertie", "ratepayer", "chugach", "alaska lng")},
    {"slug": "land-and-permitting", "title": "Land and permitting",
     "h1": "Alaska land and permitting for AI",
     "seo": "Alaska land leases and permits for AI - Alaska AI",
     "desc": "State land leases, gravel, permafrost and the public comment windows "
             "that are the only door most Alaskans get into an AI land decision.",
     "blurb": "State land leases, gravel, permafrost and the public comment "
              "windows that are the only door most Alaskans get.",
     "terms": ("state land lease", "dnr", "permit", "gravel", "permafrost",
               "roadless", "public comment", "aidea", "best interest finding",
               "right of way", "borough")},
    {"slug": "defense-and-federal", "title": "Defense and federal",
     "h1": "Defense and federal AI in Alaska",
     "seo": "Alaska defense and federal AI decisions - Alaska AI",
     "desc": "JBER, Eielson, Clear and the federal AI decisions that land in Alaska "
             "without an Alaska vote, tracked with the record behind each one.",
     "blurb": "JBER, Eielson, Clear and the federal decisions that land in "
              "Alaska without an Alaska vote.",
     "terms": ("jber", "eielson", "clear space force", "air force", "enhanced use lease",
               "pentagon", "missile defense", "dod", "federal", "congress", "senate",
               "sullivan", "murkowski", "begich")},
    {"slug": "research-and-science", "title": "Research and science",
     "h1": "Alaska AI research and science",
     "seo": "Alaska AI research and science - Alaska AI",
     "desc": "The university labs, the agencies and the field science putting "
             "machine learning to work on Alaska problems, from salmon counts to "
             "seismic monitoring.",
     "blurb": "The university labs, the agencies and the field science using "
              "machine learning on Alaska problems.",
     "terms": ("uaf", "university of alaska", "geophysical institute", "usgs",
               "deep learning", "machine learning", "computer vision", "research",
               "salmon", "fish and game", "wildfire", "seismic", "noaa")},
    {"slug": "data-sovereignty", "title": "Data sovereignty",
     "h1": "Alaska data sovereignty and AI",
     "seo": "Alaska data sovereignty and AI - Alaska AI",
     "desc": "Who owns Alaska data, who gets to train on it, and the Native "
             "corporations and tribes setting the terms before the models do.",
     "blurb": "Who owns Alaska data, who trains on it, and the Native "
              "corporations and tribes setting terms.",
     "terms": ("indigenous data sovereignty", "native-owned", "tribal", "ancsa",
               "native corporation", "data sovereignty", "consultation")},
    {"slug": "state-policy", "title": "State policy",
     "h1": "Alaska AI policy and legislation",
     "seo": "Alaska AI policy, bills and regulation - Alaska AI",
     "desc": "Alaska AI bills, the governor's desk, the Regulatory Commission and "
             "everything that decides the rules before the concrete pours.",
     "blurb": "Bills, the governor's desk, the regulatory commission and "
              "everything that decides the rules before the concrete pours.",
     "terms": ("dunleavy", "legislature", "senate bill", "house bill", "sb ", "hb ",
               "rca", "regulatory commission", "statute", "governor", "session",
               "who decides", "ballot", "primary")},
]

# Counts that appear in PROSE. A numeral reads wrong mid-sentence and a spelled
# word rots the moment the list it describes changes length. The About page
# said Alaska AI "works six beats" while TOPICS held seven and every other page
# said seven; the topics page said "seven standing beats" in its tag and its
# meta description while the chip two lines above already interpolated
# len(TOPICS) correctly. Both were written true and went stale in place. Any
# sentence that states how many of something the site has goes through here.
_COUNT_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven",
                "eight", "nine", "ten", "eleven", "twelve")


def count_word(n):
    return _COUNT_WORDS[n] if 0 <= n < len(_COUNT_WORDS) else str(n)


def source_doc_count(items):
    """How many source DOCUMENTS the docket rests on.

    Distinct URLs, because a document cited by two decisions is one document.
    This existed three times with two different definitions behind one label:
    the home page summed len(it["sources"]) and reported 47, while the data
    and sources pages counted distinct URLs and reported 43. Both printed the
    words "source documents", so the site published two different answers to
    the same question and the four items that share a citation were counted
    twice. One definition, one helper, every caller.
    """
    return len({s["url"] for it in items for s in (it.get("sources") or [])})


def topic_index(runs, topics_ledger):
    """Which decks belong to which beat.

    Matched against the run's own ledger entry (topic, angle, entities,
    keywords) plus its title and caption, so a deck lands on a beat because of
    what it is about rather than because of a word that happened to appear in
    one headline."""
    by_date = {}
    for e in (topics_ledger or {}).get("entries", []):
        d = e.get("run_date")
        if d:
            by_date[d] = " ".join([
                str(e.get("topic") or ""), str(e.get("angle") or ""),
                " ".join(e.get("entities") or []), " ".join(e.get("keywords") or []),
            ]).lower()
    out = {t["slug"]: [] for t in TOPICS}
    for r in runs:
        hay = " ".join([by_date.get(r["date"], ""), r["title"].lower(),
                        (r.get("caption") or "").lower()[:1200]])
        for t in TOPICS:
            if any(term in hay for term in t["terms"]):
                out[t["slug"]].append(r)
    return out


def deck_excerpt(r, limit=190):
    """The opening of a deck's own published copy, for use under its card.

    A grid of cover images and headlines is almost no text, which left the two
    beats with no tracked decisions at 141 and 242 words apiece: pages about
    real reporting that read to a crawler as a menu. This borrows the article's
    first paragraph rather than inventing a summary for it, so the words on the
    beat page are words the publication already stood behind."""
    lines = [l.strip() for l in (r.get("caption") or "").split("\n")]
    if lines and lines[0] == (r.get("hook") or ""):
        lines = lines[1:]
    for l in lines:
        if not l or l.startswith("#"):
            continue
        if l.lower().rstrip(":") in ("sources", "source"):
            break
        t = l.replace(": ", ", ")
        if len(t) <= limit:
            return t
        cut = t[:limit].rsplit(" ", 1)[0]
        return cut.rstrip(",.;") + "..."
    return ""


def topic_standing(items, today):
    """One paragraph on where a beat stands, computed from the docket.

    Every number and name here is read out of ledger/docket.json at build time
    rather than written by hand, so this paragraph cannot drift from the docket
    it summarises and cannot assert something the record does not carry."""
    if not items:
        return ""
    n = len(items)
    res = [(it, db.resolve(it, today)) for it in items]
    n_open = sum(1 for _it, r in res if r["access"] == "open"
                 and r["status"] == "open-for-comment")
    deciders = []
    for it in items:
        d = (it.get("decider") or "").strip()
        if d and d not in deciders:
            deciders.append(d)
    dated = sorted((p for p in res if p[1]["headline"]),
                   key=lambda p: p[1]["headline"]["date"])

    s = [f"Alaska AI tracks {n} {'decision' if n == 1 else 'decisions'} on this beat, "
         f"each one with the documents it was verified against."]
    if n_open:
        s.append(f"{n_open} {'is' if n_open == 1 else 'are'} open for public comment "
                 f"right now.")
    else:
        s.append("None are open for public comment right now, which is worth knowing "
                 "before assuming there is still a door open.")
    if dated:
        it, r = dated[0]
        s.append(f"The nearest date is {esc(db.mon_day(r['headline']['date']).title())} "
                 f"on {esc(it.get('title') or it['id'])}.")
    if deciders:
        who = deciders[:3]
        s.append("The bodies deciding on this beat include "
                 + esc(", ".join(who[:-1]) + (" and " + who[-1] if len(who) > 1 else who[0]))
                 + ".")
    return " ".join(s)


def topic_page(today, site_url, topic, decks, docket_items):
    """One standing beat. Renders whether or not it has decks on it.

    The decision list is the substance of this page rather than a footnote to
    it. It used to be a bare list of titles pointing at an anchor on the shared
    docket index, which spent the beat's best material on a link and sent every
    reader and crawler to a page about something else. Each decision now carries
    its status, who decides it, what it actually is, and a link to its OWN
    page."""
    cards = "".join(
        f"""<a class="deck" href="../../archive/{r['date']}/" data-reveal>
  <img src="{RAW}/runs/{r['date']}/slide-01.webp" width="1080" height="1350" alt="{esc(r['title'])} cover" loading="lazy">
  <div class="meta"><h3>{esc(r['title'])}</h3>
  <div class="who">{esc(pretty_date(r['date'])).upper()} &middot; {r['slides']} SLIDES</div>
  {f'<p class="sub" style="margin-top:8px">{esc(deck_excerpt(r))}</p>' if deck_excerpt(r) else ''}</div>
</a>""" for r in decks)
    n_dec = len(docket_items)
    chip = f"STANDING BEAT &middot; {len(decks)} {'ARTICLE' if len(decks) == 1 else 'ARTICLES'}"
    if n_dec:
        chip += f" &middot; {n_dec} TRACKED {'DECISION' if n_dec == 1 else 'DECISIONS'}"
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">{chip}</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">{esc(topic.get('h1') or topic['title'])}</h1>
<p class="tag">{esc(topic['blurb'])}</p>
</div>"""
    standing = topic_standing(docket_items, today)
    if standing:
        body += ('\n<h2 data-reveal>Where this beat stands</h2>\n'
                 f'<p class="prose" data-reveal>{standing}</p>')
    if docket_items:
        rows = []
        for d in docket_items:
            r = db.resolve(d, today)
            meta = [esc(db.STATUS_LABEL.get(r["status"], r["status"]))]
            if d.get("decider"):
                meta.append(esc(d["decider"]))
            if r["headline"]:
                meta.append(esc(db.mon_day(r["headline"]["date"]).title()))
            src = d.get("sources") or []
            rows.append(
                f'<li data-reveal><p><a class="proselink" href="../../docket/{esc(d["id"])}/">'
                f'<strong>{esc(d.get("title") or d["id"])}</strong></a></p>'
                f'<p class="who">{" &middot; ".join(meta)}</p>'
                f'<p>{esc(d.get("summary") or "")}</p>'
                f'<p class="who">{len(src)} {"source" if len(src) == 1 else "sources"}'
                f' on file &middot; <a class="proselink" href="../../docket/{esc(d["id"])}/">'
                f'the full record</a></p></li>')
        # The live instrument at the top of the beat it belongs to. It goes
        # here rather than into a new beat of its own, because the beat count
        # is already inconsistent across the site and a new taxonomy node
        # before that is fixed compounds the problem.
        if topic["slug"] == "power-and-the-grid":
            body += (
                '\n<h2 data-reveal>The live instrument on this beat</h2>\n'
                '<p class="prose" data-reveal>The decisions below move on a scale '
                'of months. The physical system moves daily, and '
                '<a class="proselink" href="../../gas-watch/">Cook Inlet Gas '
                'Watch</a> reads it every day, measured storage against modeled '
                'demand, published as open data. CINGSA keeps no archive of its '
                'own, so that record exists only because it is collected and '
                'committed daily. It states no verdict about whether supply is '
                'adequate, because the data cannot carry one.</p>')
        body += ('\n<h2 data-reveal>Decisions on this beat</h2>\n'
                 f'<ol class="claims" data-reveal>{"".join(rows)}</ol>'
                 '\n<p class="prose" data-reveal>Every one of these is also in '
                 '<a class="proselink" href="../../docket/">the full Alaska AI Docket</a>'
                 ', published as open data at <a class="proselink" href="../../data/">'
                 '/data/</a> under CC BY 4.0.</p>')
    if decks:
        body += f'\n<h2 data-reveal>Articles on this beat</h2>\n<div class="decks">{cards}</div>'
    else:
        body += ('\n<h2 data-reveal>Articles on this beat</h2>\n<p class="prose" '
                 'data-reveal>This beat is tracked every day. When Alaska makes news '
                 'on it, the article lands here with every fact carrying the document '
                 'it was checked against.</p>')
    body += ('\n<h2 data-reveal>Every beat</h2>\n<p class="prose" data-reveal>'
             + " &middot; ".join(
                 f'<a class="proselink" href="../{t["slug"]}/">{esc(t["title"])}</a>'
                 for t in TOPICS) + '</p>')
    desc = topic.get("desc") or topic["blurb"]
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": topic.get("h1") or topic["title"], "description": desc,
          "url": f"{site_url}/topics/{topic['slug']}/",
          "isPartOf": {"@id": org_id(site_url)},
          "about": {"@type": "Thing", "name": topic.get("h1") or topic["title"]},
          "hasPart": [{"@type": "NewsArticle", "headline": r["title"],
                       "datePublished": r["date"],
                       "url": f"{site_url}/archive/{r['date']}/"} for r in decks]}
    return page(topic.get("seo") or f"{topic['title']} - Alaska AI", desc[:155], body,
                "../../", "articles", today, site_url, f"topics/{topic['slug']}/", ld=ld,
                crumbs=[("Alaska AI", ""), ("Articles", "archive/"),
                        (topic["title"], f"topics/{topic['slug']}/")])


def topics_index_page(today, site_url, index):
    rows = "".join(
        f"""<a class="deck" href="{t['slug']}/" data-reveal>
  <div class="meta"><h3>{esc(t['title'])}</h3>
  <div class="who">{len(index.get(t['slug']) or [])} ARTICLES</div>
  <p class="sub" style="margin-top:8px">{esc(t['blurb'])}</p></div>
</a>""" for t in TOPICS)
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">{len(TOPICS)} STANDING BEATS</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">The beats</h1>
<p class="tag">Alaska AI covers {count_word(len(TOPICS))} standing beats. Each page stays live
whether or not the beat made news this week.</p>
</div>
<div class="decks">{rows}</div>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "Beats", "url": f"{site_url}/topics/",
          "isPartOf": {"@id": org_id(site_url)}}
    return page("The beats - Alaska AI",
                f"The {count_word(len(TOPICS))} standing beats Alaska AI covers, "
                "from data centers and the Railbelt grid to land permitting "
                "and data sovereignty.",
                body, "../", "articles", today, site_url, "topics/", ld=ld,
                crumbs=[("Alaska AI", ""), ("Articles", "archive/"),
                        ("Beats", "topics/")])


def sources_page(today, site_url, runs):
    """Every document this publication has verified a claim against.

    The archive of what we checked, not what we said. It is the reason to trust
    the decks and, for an answer engine, the cheapest possible proof that the
    numbers on this site came from somewhere."""
    # A document is a URL, and each document belongs to one outlet. The same
    # URL can arrive under two outlet spellings across claims, an explicit name
    # in one run and a domain derived from the URL in another, and grouping
    # naively by the recorded string then listed the same document under both,
    # so the DOCUMENTS count (distinct URLs) no longer matched the links shown.
    # Assign each URL its canonical outlet first, preferring a named outlet over
    # a bare domain, so every document is counted and shown exactly once.
    url_outlets = {}
    for r in runs:
        for c in (r.get("claims") or {}).values():
            u = c.get("source_url")
            if not u:
                continue
            name = (house(c.get("source_outlet")) or "Uncredited source").strip()
            url_outlets.setdefault(u, {})[name] = url_outlets.get(u, {}).get(name, 0) + 1

    def _canonical(names):
        # A named outlet ("Anchorage Daily News") beats a bare domain
        # ("adn.com"); among equals, the one recorded on more claims wins.
        return max(names, key=lambda n: ((" " in n or any(ch.isupper() for ch in n)),
                                         names[n], n))
    canon = {u: _canonical(names) for u, names in url_outlets.items()}

    by_outlet = {}
    for r in runs:
        for c in (r.get("claims") or {}).values():
            u = c.get("source_url")
            if not u:
                continue
            key = canon[u]
            e = by_outlet.setdefault(key, {"claims": 0, "primary": 0, "urls": {},
                                           "dates": set(), "runs": set()})
            e["claims"] += 1
            e["primary"] += bool(c.get("source_is_primary"))
            e["urls"].setdefault(u, 0)
            e["urls"][u] += 1
            e["runs"].add(r["date"])
            if c.get("date_of_source"):
                e["dates"].add(c["date_of_source"])
    order = sorted(by_outlet.items(), key=lambda kv: (-kv[1]["claims"], kv[0]))
    rows = []
    for name, e in order:
        # Show every document. The cap of 8 used to hide the difference between
        # the DOCUMENTS count in the hero (which counts them all) and the links
        # actually on the page, so the archive promised a total it did not show.
        # And mark a truncated URL with an ellipsis: the link text used to be
        # sliced to 110 characters with no marker, so a reader who read or
        # copied the visible address off the screen got one that does not
        # resolve. The href always carries the full URL.
        links = "".join(
            f'<li><a class="proselink" href="{esc(u)}" rel="nofollow noopener" '
            f'target="_blank">{esc(u[:110])}{"..." if len(u) > 110 else ""}</a></li>'
            for u in sorted(e["urls"], key=lambda u: -e["urls"][u]))
        rows.append(
            f'<li><p><strong>{esc(name)}</strong></p><div class="cmeta">'
            f'<span class="k{" p" if e["primary"] else ""}">'
            f'{e["primary"]} PRIMARY</span>'
            f'<span class="k">{e["claims"]} CLAIMS</span>'
            f'<span class="d">{len(e["runs"])} '
            f'{"ARTICLE" if len(e["runs"]) == 1 else "ARTICLES"}</span></div>'
            f'<ul class="prose" style="margin-top:8px">{links}</ul></li>')
    total = sum(e["claims"] for _, e in order)
    prim = sum(e["primary"] for _, e in order)
    docs = len({u for _, e in order for u in e["urls"]})
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">{total} VERIFIED CLAIMS &middot; {docs} DOCUMENTS</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">The source archive</h1>
<p class="tag">Every document Alaska AI has checked a claim against, and how many
claims rest on it. {prim} of {total} claims are sourced to a primary document.</p>
</div>
<h2>By outlet</h2>
<p class="galhint">SORTED BY HOW MUCH OF THE RECORD RESTS ON THEM</p>
<ol class="claims">{"".join(rows)}</ol>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "The source archive", "url": f"{site_url}/sources/",
          "isPartOf": {"@id": org_id(site_url)}}
    return page("The source archive - Alaska AI",
                f"Every one of the {docs} documents Alaska AI has verified a claim "
                f"against, by outlet, with {prim} of {total} claims resting on "
                f"primary documents.", body, "../", "articles", today, site_url,
                "sources/", ld=ld,
                crumbs=[("Alaska AI", ""), ("The source archive", "sources/")])


def video_count():
    """Published-video count from the feed the video automation maintains at
    docs/videos/videos.json. Counted live at every build, so the stat updates
    whenever the site rebuilds; zero (and no crash) if the feed is absent."""
    try:
        d = json.loads((REPO / "docs" / "videos" / "videos.json").read_text())
        return len(d.get("videos") or [])
    except Exception:
        return 0


def pretty_date(iso):
    d = ddate.fromisoformat(iso)
    return f"{MONTH_FULL[d.month - 1]} {d.day}, {d.year}"


# ---------- pages ----------

def home_page(today, site_url, docket, runs, gas_series=(), gas_model=None,
              gas_figs=None):
    items, live, done, dated, live_sorted = docket
    n_open = db.open_count(live, today)
    # Read off dated[0] itself, not recomputed, because the title beside it is
    # dated[0]'s. One item, one lookup, no way for the pair to disagree.
    nearest = db.resolve(dated[0], today)["headline"] if dated else None
    latest = runs[0] if runs else None

    n_videos = video_count()
    stats = f"""<div class="statrow">
  <div class="stat"><div class="n" data-count="{len(runs)}">{len(runs):02d}</div><div class="l">ARTICLES WRITTEN</div></div>
  <div class="stat"><div class="n" id="vidstat" data-count="{n_videos}">{n_videos:02d}</div><div class="l">VIDEOS PUBLISHED</div></div>
  <div class="stat"><div class="n" data-count="{len(live)}">{len(live):02d}</div><div class="l">DECISIONS TRACKED</div></div>
  <div class="stat"><div class="n g" data-count="{n_open}">{n_open:02d}</div><div class="l">DOORS OPEN TO YOU</div></div>
</div>"""

    latest_html = ""
    if latest:
        cover = f"{RAW}/runs/{latest['date']}/slide-01.webp"
        latest_html = f"""<h2 data-reveal>Our Latest Article</h2>
<p class="sub" data-reveal>One verified Alaska and AI story a day, drawn as a swipeable carousel.</p>
<div class="latest" data-reveal>
  <a class="cover" href="archive/{latest['date']}/"><img src="{cover}" width="1080" height="1350" alt="{esc(latest['title'])} cover slide" loading="lazy"></a>
  <div>
    <div class="chip kind">{esc(pretty_date(latest['date'])).upper()} &middot; {latest['slides']} SLIDES</div>
    <h3>{esc(latest['title'])}</h3>
    <p>{esc(latest['hook'])}</p>
    <div class="ctarow"><a class="cta ghost" href="archive/{latest['date']}/">READ</a>
    <a class="cta ghost" href="archive/">STORIES</a></div>
  </div>
</div>"""

    # Open doors first, so this section can never show fewer doors than the
    # DOORS OPEN TO YOU stat directly above it claims.
    cards = "".join(db.card_html(it, today, prefix="docket/")
                    for it in db.home_cards(dated, today, 3))
    # The gas watch meter, directly under the docket. The two datasets sit
    # together here the same way they do in the nav. It renders empty when
    # there is no verified reading, so the homepage never explains an absence.
    gas_strip = gw.home_strip(gas_series, gas_model, figs=gas_figs) if gas_model else ""
    closing = f"""<h2 data-reveal><a href="docket/">The docket</a></h2>
<p class="sub" data-reveal>Every AI infrastructure decision in Alaska, tracked daily with a source on
every fact. Gold means a door is open to the public right now.</p>
<div class="cards">{cards}</div>
<div class="ctarow" data-reveal><a class="cta gold" href="docket/">OPEN THE FULL DOCKET</a></div>

{gas_strip}"""

    # Our Latest Video: the skeleton is baked, the newest entry is pulled live
    # from videos/videos.json (owned by the video automation) so this section
    # always shows the freshest video with no rebuild needed. The mp4 only
    # loads when the section scrolls into view, and it autoplays muted there.
    video_html = """<div id="homevidsec" hidden>
<h2 data-reveal>Our Latest Video</h2>
<p class="sub" data-reveal>The newest video from the daily feed. Tap through for the whole
collection.</p>
<div class="latestvid" data-reveal>
  <div class="vidwrap"><video id="hv" muted playsinline loop preload="none"
  aria-label="The latest Alaska AI video"></video>
  <button class="vsound" id="hvsound" type="button" aria-label="Toggle sound">TAP FOR SOUND</button></div>
  <div>
    <div class="chip kind" id="hvdate"></div>
    <h3 id="hvtitle"></h3>
    <p id="hvcap"></p>
    <div class="ctarow"><a class="cta gold" href="videos/">EVERY VIDEO</a></div>
  </div>
</div>
</div>
<script>
(function(){
var sec=document.getElementById('homevidsec');if(!sec||!window.fetch)return;
fetch('videos/videos.json').then(function(r){return r.json()}).then(function(m){
  var base=m.media_base||'';
  var vs=(m.videos||[]).filter(function(v){return v&&v.video});
  /* THE VIDEO COUNTER SELF-CORRECTS (2026-08-05). video_count() reads the feed
     at BUILD time, but docs/videos/videos.json is appended to by publish_feed.py
     in the alaska-ai-weekly repo on its own schedule, so a video landing after
     today's build leaves the homepage stat one behind until the next one. That
     is exactly what happened on 2026-08-05: the build read 33 and the 34th
     video landed hours later. The number is re-read here from the same fetch
     this section already makes, so the page is right whenever it is loaded.
     The server-rendered number stays as the no-JS fallback. */
  var st=document.getElementById('vidstat');
  if(st&&vs.length){
    var n=vs.length;
    st.setAttribute('data-count',String(n));
    if(!st.dataset.counted)st.textContent=(n<10?'0':'')+n;
  }
  if(!vs.length)return;
  var v=vs[0];
  var abs=function(u){return /^https?:\\/\\//.test(u)?u:base+u};
  var el=document.getElementById('hv');
  if(v.poster)el.poster=abs(v.poster);
  el.dataset.src=abs(v.video_mobile||v.video);
  document.getElementById('hvtitle').textContent=v.title||'';
  document.getElementById('hvcap').textContent=v.caption||'';
  var d=document.getElementById('hvdate');
  try{d.textContent=new Date(v.date+'T12:00:00').toLocaleDateString('en-US',
    {month:'long',day:'numeric',year:'numeric'}).toUpperCase()+' \\u00b7 ON VIDEO'}
  catch(e){d.textContent=(v.date||'').toUpperCase()}
  sec.hidden=false;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){if(!el.getAttribute('src'))el.src=el.dataset.src;
      el.play().catch(function(){});}
    else el.pause();
  })},{threshold:0.3});
  io.observe(el);
  var sb=document.getElementById('hvsound');
  var toggle=function(){
    el.muted=!el.muted;
    sb.textContent=el.muted?'TAP FOR SOUND':'MUTE';
    sb.classList.toggle('on',!el.muted);
    if(!el.getAttribute('src'))el.src=el.dataset.src;
    el.play().catch(function(){});
  };
  sb.addEventListener('click',toggle);
  el.addEventListener('click',toggle);
}).catch(function(){});
})();
</script>"""

    # The beats, on the front page.
    #
    # The home page linked to the docket, the articles and the videos, and to no
    # beat page at all, so the seven pages that answer a question somebody
    # actually types ("Alaska data centers", "Alaska AI policy") were reachable
    # only from a nav menu and from each other. They are the pages most likely
    # to be a stranger's first contact with this publication, and the front page
    # was not pointing at them.
    beats = "".join(
        f"""<a class="deck" href="topics/{t['slug']}/" data-reveal>
  <div class="meta"><h3>{esc(t.get('h1') or t['title'])}</h3>
  <p class="sub" style="margin-top:8px">{esc(t['blurb'])}</p></div>
</a>""" for t in TOPICS)
    beats_html = f"""<h2 data-reveal><a href="topics/">What Alaska AI covers</a></h2>
<p class="sub" data-reveal>Seven standing beats, tracked every day. Each one keeps its
own page whether or not it made news this week, with the decisions on it, who decides
them, and whether the public still has a way in.</p>
<div class="decks">{beats}</div>"""

    n_src = source_doc_count(items)

    what_html = f"""<h2 data-reveal>What this is</h2>
<p class="prose" data-reveal>Alaska AI is a daily publication on Alaska and artificial
intelligence, and an AI studio. The reporting side writes one verified
story a day and keeps the Alaska AI Docket, a public record of
{len(live) + len(done)} AI infrastructure decisions in the state, {n_src} source
documents on file, and for each one the plain answer to who decides it and whether an
Alaskan still gets a say. It is published as
<a class="proselink" href="data/">open data under CC BY 4.0</a> so anyone can check the
work or build on it. The studio side builds
<a class="proselink" href="services/">Alaska businesses</a> an agentic operating system,
its flagship product, a package of 1 to 1000 AI agents working together to automate every
possible aspect of the business.</p>"""

    next_line = ""
    if nearest and dated:
        next_line = (f"Next on the docket is {esc(dated[0]['title'])}, "
                     f"{esc(pretty_date(nearest['date']))}. ")
    body = f"""<div class="hero heroanim">
<div><div class="daylight">{daylight_chip(today)}</div></div>
<h1>AI is coming <em>north</em></h1>
<p class="tag">Alaska AI watches it happen. Every deal, docket and decision on the state's
AI beat, verified to the source and told for Alaskans. From the Slope to Southeast, daily.</p>
<div class="ctarow">
  <a class="cta gold" href="docket/">DOCKET</a>
  <a class="cta ghost" href="archive/">ARTICLES</a>
  <a class="cta ghost" href="videos/">VIDEOS</a>
</div>
{stats}
</div>
{scan_html()}
{video_html}
{latest_html}
{closing}
{beats_html}
{what_html}
{subscribe_html()}
<div class="about-line" data-reveal><p>{next_line}All sources verified against claims.</p></div>"""
    ld = {"@context": "https://schema.org", "@graph": [
        org_ld(site_url),
        {"@type": "WebSite", "url": f"{site_url}/", "name": "Alaska AI",
         "alternateName": "Alaska AI HQ",
         "publisher": {"@id": org_id(site_url)}}]}
    return page("Alaska AI - AI Consulting and Daily AI News for Alaska",
                "Alaska's AI studio in Anchorage. Daily verified stories on Alaska and AI, "
                "a public docket of AI infrastructure decisions, and AI consulting for "
                "Alaska businesses.", body, "", "home", today, site_url, "",
                ld=ld, extra_css=(gw.GW_CSS if gas_strip else ""))


def docket_page(today, site_url, docket):
    items, live, done, dated, live_sorted = docket
    svg, mapcap = db.map_svg(live_sorted + done, today)
    # Layer toggles, done with real checkboxes and real labels rather than
    # script. Every checkbox has to come BEFORE the svg in the markup, because
    # the whole mechanism is the sibling combinator. The grid carries `checked`
    # so it is on by default; the other two start off, so the map a reader
    # meets is still mostly pins. Works with the keyboard, works with JS off.
    LAYER_UI = [
        ("grid", "GRID", True,
         "Transmission at 69 kV and up. The raw state layer is 93 percent local "
         "distribution from one utility, so it is cut at the transmission floor."),
        ("gen", "GENERATION", False,
         "Power plants of 20 MW and up. That is 31 of Alaska's 152 plants but 78 "
         "percent of its capacity. Circle area is nameplate megawatts."),
        ("taps", "PIPELINE", False,
         "The Trans Alaska Pipeline System. Gas lines are left out, being 96 "
         "percent sub-kilometre distribution with nothing to sort them by."),
    ]
    # The status filter, same mechanism. All three start on, so the map a
    # reader meets shows every decision and the filter is something they reach
    # for rather than something they have to undo.
    FILTERS = [("open", "OPEN"), ("indirect", "INDIRECT"), ("closed", "CLOSED")]
    have = db.available_layers()
    ui = [row for row in LAYER_UI if row[0] in have]
    layerbox = "".join(
        '<input class="lyrbox" type="checkbox" id="lyr-%s"%s>' % (k, " checked" if on else "")
        for k, _, on, _ in ui)
    layerbox += "".join('<input class="lyrbox" type="checkbox" id="f-%s" checked>' % k
                        for k, _ in FILTERS)
    chips = "".join(
        '<label for="lyr-%s"><span class="sw"></span>%s</label>' % (k, lab)
        for k, lab, _, _ in ui)
    fchips = "".join(
        '<label for="f-%s"><span class="sw"></span>%s</label>' % (k, lab)
        for k, lab in FILTERS)
    notes = "".join('<span class="lyrnote n-%s">%s</span>' % (k, note)
                    for k, _, _, note in ui)
    layerbar = ('<div class="lyrbar">'
                '<div class="lyrchips">%s'
                '<span class="mapzoomctl" hidden id="mapzoomctl">'
                '<button type="button" id="mapout" aria-label="Zoom the map out">-</button>'
                '<button type="button" id="mapin" aria-label="Zoom the map in">+</button>'
                '<button type="button" class="mapreset" id="mapreset">FIT ALASKA</button>'
                '</span>'
                '</div>'
                '<div class="lyrchips lyrfilters">%s</div>'
                '<div class="lyrnotes">%s</div></div>' % (chips, fchips, notes))
    n_open = db.open_count(live, today)
    nearest = db.resolve(dated[0], today)["headline"] if dated else None
    cards = "".join(db.card_html(it, today) for it in dated[:6])
    live_html = "".join(db.item_html(it, today, n) for n, it in enumerate(live_sorted, 1))
    done_html = "".join(db.item_html(it, today, n) for n, it in enumerate(done, len(live_sorted) + 1))
    stats = f"""<div class="statrow">
  <div class="stat"><div class="n">{len(live):02d}</div><div class="l">DECISIONS TRACKED</div></div>
  <div class="stat"><div class="n g">{n_open:02d}</div><div class="l">OPEN TO THE PUBLIC</div></div>
  {f'<div class="stat"><div class="n">{db.mon_day(nearest["date"])}</div><div class="l">NEXT DATE</div></div>' if nearest else ''}
</div>"""
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<h1>The Alaska AI <em>Docket</em></h1>
<p class="tag">Every AI infrastructure decision in Alaska, tracked daily. Who decides,
when it lands, and whether the public gets a say. Sources on every item.</p>
{stats}
</div>
<div class="maphero">{layerbox}{svg}{layerbar}<div class="mapcap">{mapcap}</div></div>
<h2>Closing soon</h2>
<p class="sub">The nearest deadlines and votes. A pulsing pin on the map means a public
comment window is open right now.</p>
<div class="cards">{cards}</div>
<h2>The docket</h2>
<p class="sub">Access reads OPEN when a formal public comment or testimony path exists today,
INDIRECT when an elected or member-accountable body decides, CLOSED when the evaluation is private.</p>
{live_html}
{'<h2>Decided</h2>' + done_html if done_html else ''}
{subscribe_html()}
<div class="about-line" data-reveal><p>All sources verified against claims.
The data behind this page is public at <a href="../docket.json" style="color:var(--blue);text-decoration:none">docket.json</a>.</p>
<p>Alaska AI keeps this docket current with the same kind of autonomous system it
builds for Alaska businesses.</p>
<div class="ctarow" style="margin-top:20px"><a class="cta ghost" href="../services/">WHAT WE BUILD</a></div></div>"""
    ld = docket_dataset_ld(today, site_url, items)
    return page("The Alaska AI Docket - AI Infrastructure Decisions in Alaska",
                "Every AI infrastructure decision in Alaska, tracked daily. Who decides, "
                "when it lands, and whether the public gets a say. Sources on every item.",
                body, "../", "docket", today, site_url, "docket/",
                og_image="og-docket.png", ld=ld,
                crumbs=[("Alaska AI", ""), ("Docket", "docket/")],
                # The map's styling and its pan and zoom ride on this page only.
                extra_css=MAP_CSS, extra_js=MAP_JS)


def archive_page(today, site_url, runs):
    decks = "".join(
        f"""<a class="deck" href="{r['date']}/" data-reveal>
  <img src="{RAW}/runs/{r['date']}/slide-01.webp" width="1080" height="1350" alt="{esc(r['title'])} cover" loading="lazy">
  <div class="meta"><h3>{esc(r['title'])}</h3>
  <div class="who">{esc(pretty_date(r['date'])).upper()} &middot; {r['slides']} SLIDES</div></div>
</a>""" for r in runs)
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<h1>The <em>articles</em></h1>
<p class="tag">One verified Alaska and AI story at a time. Newest first.</p>
</div>
<h2 class="vh">Every deck</h2>
<div class="deckgrid" style="margin-top:44px">{decks}</div>
<div class="about-line" data-reveal><p>Every article here is researched, drawn and
shipped by the studio's own autonomous system. It builds the same kind of thing for
Alaska businesses.</p>
<div class="ctarow" style="margin-top:20px"><a class="cta ghost" href="../services/">WHAT WE BUILD</a></div></div>"""
    return page("Alaska AI Articles - Daily Verified Alaska and AI Stories",
                "Every carousel Alaska AI has published. One verified story a day on "
                "Alaska and AI, drawn as bespoke data art.",
                body, "../", "articles", today, site_url, "archive/",
                crumbs=[("Alaska AI", ""), ("Articles", "archive/")])


CHEV_L = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
          '<path d="M10.5 2.5 5 8l5.5 5.5" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CHEV_R = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
          '<path d="M5.5 2.5 11 8l-5.5 5.5" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CROSS = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M3.5 3.5l9 9M12.5 3.5l-9 9" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round"/></svg>')


# The reuse grant, stated once and referenced everywhere the data is offered.
# An open dataset nobody is told they may use does not get used.
DATA_LICENSE = "https://creativecommons.org/licenses/by/4.0/"
DATA_LICENSE_LABEL = "CC BY 4.0"

# Bump the MINOR when a field is added, the MAJOR only when one changes meaning
# or disappears, so a consumer can pin on it and know what a bump costs them.
DOCKET_SCHEMA_VERSION = "1.0"

# What every field means, published WITH the data. A schema that lives only in
# a maintainer's head is not a contract, and this is the file an answer engine
# reads to understand what it is quoting.
DOCKET_FIELD_DOCS = {
    "id": "Stable kebab-case identifier. Never reused, never renamed.",
    "url": "Canonical page for this decision on alaskaaihq.com.",
    "title": "Plain-language headline for the decision.",
    "kind": "What kind of decision this is. See enums.kind.",
    "status": "Where the decision stands today. See enums.status.",
    "decider": "The body that says yes or no.",
    "public_access": ("Whether the public has a formal way in RIGHT NOW. open "
                      "means a comment or testimony path exists today, indirect "
                      "means an elected or member-accountable body decides, "
                      "closed means the evaluation is private."),
    "access_note": "One or two sentences on how a member of the public reaches this.",
    "summary": "One or two verified sentences describing the decision.",
    "key_dates": ("Dated milestones. Each carries a kind, which is its ROLE, and "
                  "roles are not interchangeable. deadline is a date the READER "
                  "must act by. vote is a body voting, often a different body "
                  "than the decider. decision is the deciding body ruling. "
                  "milestone is context. Only a deadline is ever a reader's "
                  "call-to-action date."),
    "location": "Place name with longitude and latitude in WGS84 degrees.",
    "sources": ("Every document a fact here was checked against, with the outlet "
                "and the date. Primary sources preferred. Nothing enters this "
                "dataset on rumour."),
    "first_seen": "Date this decision entered the docket (America/Anchorage).",
    "last_updated": "Date a human or the routine last re-verified it against a source.",
    "history": ("One dated line per material change, oldest first. This is the "
                "audit trail for how the decision moved."),
}


def docket_dataset_ld(today, site_url, items):
    """The Dataset node, carrying the fields a dataset catalogue actually indexes.

    The previous version had a name, a description, one distribution and nothing
    else, which is well under the bar Google Dataset Search and friends look
    for: no license (so a machine cannot tell reuse is allowed), no temporal or
    spatial coverage, no variableMeasured (so nothing describes what a row
    holds), no keywords. Those omissions are the difference between a page that
    happens to link JSON and a dataset that gets found and cited."""
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": f"{site_url}/docket/#dataset",
        "name": "The Alaska AI Docket",
        "alternateName": "Alaska AI infrastructure decisions",
        "description": ("Every AI-infrastructure decision in Alaska. Land leases, "
                        "public comment windows, utility votes, legislation and "
                        "federal solicitations, with the deciding body, the dates "
                        "that matter, whether the public has a formal way in, and "
                        "a fetched primary source for every fact. Maintained daily."),
        "url": f"{site_url}/docket/",
        "sameAs": f"{site_url}/data/",
        "dateModified": max([it["last_updated"] for it in items] or [today.isoformat()]),
        "datePublished": min([it["first_seen"] for it in items] or [today.isoformat()]),
        "creator": {"@id": org_id(site_url)},
        "publisher": {"@id": org_id(site_url)},
        "maintainer": {"@id": org_id(site_url)},
        "license": DATA_LICENSE,
        "isAccessibleForFree": True,
        "version": DOCKET_SCHEMA_VERSION,
        "inLanguage": "en-US",
        "creativeWorkStatus": "Published",
        "keywords": ["Alaska", "artificial intelligence", "data centers",
                     "AI infrastructure", "public comment", "land use",
                     "electric utilities", "Railbelt", "permitting",
                     "government decisions", "open data"],
        "spatialCoverage": {"@type": "Place", "name": "Alaska, United States",
                            "geo": {"@type": "GeoShape", "box": "51.2 -179.1 71.4 -129.9"}},
        "temporalCoverage": docket_temporal(items),
        "measurementTechnique": ("Each decision is recorded from a fetched primary "
                                 "source and re-verified on a daily routine; every "
                                 "material change is appended to a dated history."),
        "variableMeasured": [{"@type": "PropertyValue", "name": k, "description": v}
                             for k, v in DOCKET_FIELD_DOCS.items()],
        "distribution": [
            {"@type": "DataDownload", "name": "The docket as JSON",
             "encodingFormat": "application/json",
             "contentUrl": f"{site_url}/docket.json"},
            {"@type": "DataDownload", "name": "Docket changes as RSS",
             "encodingFormat": "application/rss+xml",
             "contentUrl": f"{site_url}/docket/feed.xml"},
        ],
        "includedInDataCatalog": {"@type": "DataCatalog", "name": "Alaska AI open data",
                                  "url": f"{site_url}/data/"},
        "hasPart": [{"@type": "Dataset", "name": it["title"],
                     "url": f"{site_url}/docket/{it['id']}/",
                     "dateModified": it["last_updated"]} for it in items],
    }


def docket_temporal(items):
    """ISO 8601 interval covering the dataset, from the earliest date any item
    records to the latest. Real coverage, computed, not asserted."""
    ds = [d["date"] for it in items for d in it.get("key_dates", [])]
    ds += [it["first_seen"] for it in items] + [it["last_updated"] for it in items]
    ds = sorted(d for d in ds if d)
    return f"{ds[0]}/{ds[-1]}" if ds else ""


def _norm_url(u):
    return (u or "").split("#")[0].rstrip("/").lower()


def decision_decks(it, runs):
    """Articles that verified a claim against one of this decision's own source
    documents.

    A FACTUAL relation, not a keyword guess. Matching decks by shared words
    would put unrelated stories on a decision page the way two Alaska stories
    share 'north slope', so the join is on the exact source URL: this article
    and this decision rest on the same document. Newest first."""
    durls = {_norm_url(s["url"]) for s in it.get("sources", [])}
    out = []
    for r in runs:
        curls = {_norm_url(c.get("source_url")) for c in (r.get("claims") or {}).values()}
        if durls & curls:
            out.append(r)
    return sorted(out, key=lambda r: r["date"], reverse=True)


def beat_line(beats, prefix, lead):
    """Which standing beats a page belongs to, as links. Empty when none match,
    because an empty beat line is worse than no beat line."""
    if not beats:
        return ""
    links = " &middot; ".join(
        f'<a class="proselink" href="{prefix}topics/{t["slug"]}/">'
        f'{esc(t.get("h1") or t["title"])}</a>' for t in beats)
    return (f'\n<h2 data-reveal>Beats</h2>\n<p class="prose" data-reveal>{lead} '
            f'{links}. Each beat page keeps every decision and every article on '
            f'that subject in one place.</p>')


def decision_page(today, site_url, it, runs, beats=()):
    """One canonical page per tracked decision.

    The docket was a single page with #anchors, so a decision had no URL of its
    own: nothing for an answer engine to cite, no title, no lastmod, no
    structured data of its own. This is that page. Every date on it comes from
    db.resolve(), the one resolver every docket surface reads, so this cannot
    drift from the docket page (rule 5 of the date-roles work)."""
    r = db.resolve(it, today)
    prefix = "../../"
    access_label = db.ACCESS_LABEL[r["access"]]
    kind_label = db.KIND_LABEL[it["kind"]].upper()
    canonical = f"{site_url}/docket/{it['id']}/"

    chip = db.chip_html(r)
    act = ""
    if r["cta"]:
        when = (f' &middot; CLOSES {db.mon_day(r["deadline"]["date"]).upper()}'
                if r["deadline"] else "")
        act = (f'<div class="ctarow act"><a class="cta gold" '
               f'href="{esc(it["sources"][0]["url"])}" rel="noopener">'
               f'COMMENT NOW{when}</a></div>')

    # Sources, all of them, with the primary ones marked. The docket page shows
    # outlet names inline; this page is the record, so it shows the documents.
    srcs = "".join(
        f'<li><p><a class="proselink" href="{esc(s["url"])}" rel="noopener">'
        f'{esc(house(s.get("outlet")) or "source")}</a></p>'
        f'<div class="cmeta"><span class="d">{esc(s.get("date", ""))}</span></div></li>'
        for s in it.get("sources", []))

    # The full change log, oldest first. The docket page shows only the newest
    # note; how a decision MOVED is the reason this publication is worth
    # trusting, so the whole trail belongs on its own page.
    hist = "".join(
        f'<li><p><strong>{esc(h["date"])}</strong> {esc(h["note"])}</p></li>'
        for h in it.get("history", []))

    decks = decision_decks(it, runs)
    deck_rows = "".join(
        f'<a class="deck" href="{prefix}archive/{r2["date"]}/" data-reveal>'
        f'<div class="meta"><h3>{esc(r2["title"])}</h3>'
        f'<div class="who">{esc(pretty_date(r2["date"])).upper()}</div></div></a>'
        for r2 in decks[:6])
    deck_block = (f'<h2 data-reveal>Articles on this decision</h2>'
                  f'<p class="sub" data-reveal>Each of these verified a claim against a '
                  f'document this decision also rests on.</p>'
                  f'<div class="decks" data-reveal>{deck_rows}</div>') if deck_rows else ""

    loc = it.get("location") or {}
    where = esc(loc.get("name") or "Alaska")

    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="top">
  <span class="badge b-{r["access"]}">{access_label}</span>
  <span class="chip kind">{kind_label}</span>
  {chip}
</div>
<h1 style="font-size:clamp(30px,4.4vw,52px);margin-top:14px">{esc(it["title"])}</h1>
<p class="tag">{esc(it["summary"])}</p>
<div class="who">DECIDES &middot; {esc(it["decider"]).upper()}</div>
{act}
</div>
<h2 data-reveal>How the public reaches this</h2>
<p class="prose" data-reveal>{esc(it["access_note"])}</p>
<h2 data-reveal>Timeline</h2>
<div data-reveal>{db.rail_html(it, today)}</div>
<h2 data-reveal>Sources</h2>
<p class="sub" data-reveal>Every document a fact on this page was checked against.</p>
<ol class="claims" data-reveal>{srcs}</ol>
<h2 data-reveal>How this decision moved</h2>
<p class="sub" data-reveal>One dated line per material change, oldest first.</p>
<ol class="claims" data-reveal>{hist}</ol>
{deck_block}
<h2 data-reveal>Cite this</h2>
<p class="prose" data-reveal>Alaska AI Docket, {esc(it["title"])}.
Tracked since {esc(pretty_date(it["first_seen"]))}, last verified
{esc(pretty_date(it["last_updated"]))}. <a class="proselink"
href="{canonical}">{canonical}</a> &middot; Reuse permitted under
{DATA_LICENSE_LABEL} with attribution. This decision is also available as
structured data in <a class="proselink" href="{prefix}docket.json">the docket
JSON</a>, item id <code>{esc(it["id"])}</code>.</p>
<div class="ctarow" data-reveal>
  <a class="cta ghost" href="{prefix}docket/">ALL TRACKED DECISIONS</a>
  <a class="cta ghost" href="{prefix}data/">THE DATA</a>
</div>"""

    citation = [{"@type": "CreativeWork",
                 "name": house(s.get("outlet")) or "source",
                 "url": s["url"],
                 **({"datePublished": s["date"]} if s.get("date") else {})}
                for s in it.get("sources", [])]
    ld = {
        "@context": "https://schema.org",
        "@type": "Report",
        "headline": it["title"],
        "description": it["summary"],
        "url": canonical,
        "datePublished": it["first_seen"],
        "dateModified": it["last_updated"],
        "author": {"@id": org_id(site_url)},
        "publisher": {"@id": org_id(site_url)},
        "isPartOf": {"@id": f"{site_url}/docket/#dataset"},
        "license": DATA_LICENSE,
        "isAccessibleForFree": True,
        "inLanguage": "en-US",
        "keywords": [db.KIND_LABEL[it["kind"]], it["decider"], where,
                     "Alaska", "AI infrastructure"],
        "about": {"@type": "Thing", "name": it["title"],
                  "description": it["summary"]},
        "mentions": [{"@type": "GovernmentOrganization", "name": it["decider"]}],
        "spatialCoverage": {"@type": "Place", "name": where,
                            **({"geo": {"@type": "GeoCoordinates",
                                        "latitude": loc["lat"], "longitude": loc["lon"]}}
                               if loc.get("lat") is not None and loc.get("lon") is not None
                               else {})},
        "temporalCoverage": (f"{it['first_seen']}/{it['last_updated']}"),
        "citation": citation,
    }
    # A live comment window genuinely is an event with an end date and an online
    # way to take part, so it is published as one. Emitted only when the window
    # is actually open and has a real close date, never invented.
    extra_ld = ""
    if r["cta"] and r["deadline"]:
        ev = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": f"Public comment period, {it['title']}",
            "description": it["access_note"],
            "startDate": it["first_seen"],
            "endDate": r["deadline"]["date"],
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
            "location": {"@type": "VirtualLocation", "url": it["sources"][0]["url"]},
            "organizer": {"@type": "GovernmentOrganization", "name": it["decider"]},
            "isAccessibleForFree": True,
            "url": canonical,
        }
        extra_ld = f'<script type="application/ld+json">{ld_json(ev)}</script>'

    body += beat_line(beats, prefix, "This decision is tracked on")
    desc = (f"{it['title']}. Who decides, when it lands, and whether the public "
            f"gets a say. Sourced and updated daily by Alaska AI.")[:155]
    return page(f"{it['title']} - Alaska AI Docket", desc, body, prefix, "docket",
                today, site_url, f"docket/{it['id']}/", ld=ld,
                extra_head=extra_ld,
                crumbs=[("Alaska AI", ""), ("Docket", "docket/"),
                        (it["title"], f"docket/{it['id']}/")])


def docket_answers(today, site_url, items):
    """The questions people actually ask about this beat, answered from the
    ledger rather than written by hand.

    Every answer is GENERATED from verified docket data, so it cannot go stale
    and cannot contain a fact the record does not carry. Each returns
    (question, plain-text answer for structured data, html answer). Deadlines
    come from db.resolve(), never recomputed, so this page cannot disagree with
    the docket or a decision page."""
    out = []
    live = [it for it in items
            if it["status"] in ("open-for-comment", "pending-decision", "watching")]

    def link(it):
        return (f'<a class="proselink" href="../docket/{esc(it["id"])}/">'
                f'{esc(it["title"])}</a>')

    # 1. The one question this publication exists to answer.
    openers = [(it, db.resolve(it, today)) for it in items]
    openers = [(it, r) for it, r in openers if r["cta"]]
    if openers:
        rows = "".join(
            f'<li><p>{link(it)} {db.chip_html(r)}</p>'
            f'<p class="sub">{esc(it["access_note"])}</p>'
            f'<p><a class="proselink" href="{esc(it["sources"][0]["url"])}" '
            f'rel="noopener">Comment on the record</a></p></li>'
            for it, r in openers)
        plain = ("; ".join(
            f'{it["title"]}, decided by {it["decider"]}'
            + (f', comment closes {pretty_date(r["deadline"]["date"])}'
               if r["deadline"] else ", no published close date")
            for it, r in openers)) + "."
        out.append((
            "Which Alaska AI infrastructure decisions can the public comment on right now?",
            f"{len(openers)} of the {len(items)} decisions Alaska AI tracks has a formal "
            f"public comment path open today. {plain}",
            f'<ol class="claims">{rows}</ol>'))
    else:
        out.append((
            "Which Alaska AI infrastructure decisions can the public comment on right now?",
            f"None of the {len(items)} decisions Alaska AI tracks has a formal public "
            f"comment window open today. Windows open and close often, so the docket is "
            f"the live answer.",
            '<p class="prose">No formal public comment window is open today. The '
            '<a class="proselink" href="../docket/">docket</a> is the live answer.</p>'))

    # 2. Who holds the power. One page instead of nine near-empty hub pages,
    #    because every decider on this beat is currently distinct.
    deciders = {}
    for it in items:
        deciders.setdefault(it["decider"], []).append(it)
    drows = "".join(
        f'<li><p><strong>{esc(d)}</strong></p><p class="sub">'
        + " &middot; ".join(link(i) for i in its) + "</p></li>"
        for d, its in sorted(deciders.items(), key=lambda kv: (-len(kv[1]), kv[0])))
    out.append((
        "Who decides whether AI data centers get built in Alaska?",
        ("No single body does. Across the decisions Alaska AI tracks, the deciders are "
         + "; ".join(sorted(deciders)) + "."),
        f'<p class="prose">No single body does, which is most of why this is hard to '
        f'follow. Across the {len(items)} tracked decisions the deciders are these.</p>'
        f'<ol class="claims">{drows}</ol>'))

    # 3. The question a search engine gets asked constantly.
    dc = [it for it in items
          if "data cent" in (it["title"] + " " + it["summary"]).lower()]
    if dc:
        rows = "".join(
            f'<li><p>{link(it)}</p><p class="sub">'
            f'{esc(db.STATUS_LABEL[db.resolve(it, today)["status"]])} &middot; '
            f'{esc(it["decider"])}</p></li>' for it in dc)
        out.append((
            "Are AI data centers being built in Alaska?",
            (f"Alaska AI tracks {len(dc)} live decisions that would enable AI or cloud "
             f"data centers in Alaska, covering state land, federal land, utility "
             f"supply and legislation. Each is a decision in progress rather than a "
             f"finished project, and each is listed with its deciding body, its dates "
             f"and a fetched source."),
            f'<p class="prose">{len(dc)} of the tracked decisions would enable AI or '
            f'cloud data centers, on state land, federal land, in utility supply or in '
            f'statute. These are decisions in progress, not finished projects.</p>'
            f'<ol class="claims">{rows}</ol>'))

    # 4. Geography, straight off the records.
    places = sorted({(it.get("location") or {}).get("name") for it in items
                     if (it.get("location") or {}).get("name")})
    if places:
        out.append((
            "Where in Alaska is AI infrastructure being proposed?",
            "The tracked decisions sit at " + "; ".join(places) + ".",
            '<p class="prose">The tracked decisions sit at these places. The '
            '<a class="proselink" href="../docket/">docket map</a> shows them '
            'against the transmission grid, the generating fleet and the pipeline.</p>'
            '<ol class="claims">'
            + "".join(f'<li><p>{esc(p)}</p></li>' for p in places) + '</ol>'))

    # 5. Why the record is worth quoting, stated with numbers rather than adjectives.
    n_src = source_doc_count(items)
    n_hist = sum(len(it.get("history", [])) for it in items)
    out.append((
        "How reliable is the Alaska AI Docket, and can I reuse it?",
        (f"Every fact carries the document it was checked against. The docket holds "
         f"{len(items)} decisions resting on {n_src} source documents, with {n_hist} "
         f"dated change notes recording how each decision moved. An autonomous daily "
         f"routine re-fetches a primary source for any decision whose dates are near "
         f"or past. It is open data under {DATA_LICENSE_LABEL}, so it may be reused "
         f"and quoted with attribution to Alaska AI and a link."),
        f'<p class="prose">Every fact carries the document it was checked against. '
        f'{len(items)} decisions rest on {n_src} source documents, with {n_hist} dated '
        f'change notes recording how each one moved, and a daily routine re-fetches a '
        f'primary source whenever a date comes near. Nothing enters on rumour, and what '
        f'cannot be verified is dropped rather than published softly. It is open data '
        f'under {DATA_LICENSE_LABEL}. See <a class="proselink" href="../data/">the '
        f'data</a> for the schema and the license, and <a class="proselink" '
        f'href="../sources/">the source archive</a> for every document.</p>'))
    return out


def privacy_page(today, site_url):
    """What this site collects, stated plainly.

    A publication that asks agencies to be transparent has no standing to run
    surveillance analytics, and no standing to bury what it collects either.
    This page exists so the answer is checkable rather than assumed, and it
    ships in the same commit as the counter it describes."""
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">NO COOKIES &middot; NO TRACKING</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">Privacy</h1>
<p class="tag">This site counts how often a page is read. It does not attempt to
learn who read it, and it cannot. No cookies, no visitor identifier, no
cross-site anything. Here is the whole of it, so you can check rather than
trust.</p>
</div>
<h2 data-reveal>What is counted</h2>
<p class="prose" data-reveal>When you open a page, a single message records four
things. The path of the page you opened. The HOST of wherever you came from, so
<code>linkedin.com</code> rather than the full address of the page you were on.
A campaign tag, only when the link you followed carried one. And whether the
screen is a phone, a tablet or a desktop, in those three buckets and no finer.
That is the complete list.</p>
<h2 data-reveal>What is never collected</h2>
<ol class="claims" data-reveal>
<li><p><strong>No cookies.</strong> None are set and none are read. Nothing is
written to local storage either.</p></li>
<li><p><strong>No identifier.</strong> There is no visitor id, no device id and
no hashed stand-in for one. Two visits by the same person are not, and cannot
be, linked to each other.</p></li>
<li><p><strong>Your IP address is not stored.</strong> It reaches the server the
way it must for any web request, is used only to reject automated traffic, and is
never written down.</p></li>
<li><p><strong>Your browser's user agent is not stored.</strong> It is read once,
in memory, to decide phone or tablet or desktop, and then discarded.</p></li>
<li><p><strong>Not the page you came from.</strong> Only its host. A full
referring address can carry private context, so it never leaves your
browser.</p></li>
<li><p><strong>No advertising, no data brokers, no third-party analytics.</strong>
There is no Google Analytics here and no ad network. The counter runs on our own
infrastructure, so your reading is not an asset anyone else holds.</p></li>
</ol>
<h2 data-reveal>Why there is no cookie banner</h2>
<p class="prose" data-reveal>Because there is nothing to consent to. A consent
banner exists where a site processes personal data, and nothing described above
is personal data. We would rather remove the reason for the banner than show you
one.</p>
<h2 data-reveal>If you would rather not be counted</h2>
<p class="prose" data-reveal>Turn on Do Not Track or Global Privacy Control in
your browser and this site sends nothing at all. Not sent and then ignored,
simply never sent. Both signals are also honoured a second time at the server,
so a message that should not have been sent is still not counted. Any
content blocker will stop it too, and the site works exactly the same with it
blocked.</p>
<p class="prose" data-reveal>One caveat, because a page like this is worth
nothing if it is only mostly complete. When the server refuses a message it
writes down why it refused and when, and that is the entire record. The words
<code>dnt-header</code> and a timestamp. No path, no referring host, no address,
no user agent, nothing that distinguishes one refused message from another. A
visit that opts out therefore leaves strictly less behind than a counted one,
and what it leaves cannot be tied to you or to a page. It is kept for one
reason. The server answers every message the same way whether it counted it or
threw it away, which is good for you and was briefly terrible for us, because a
counter that recorded nothing looked exactly like a counter that worked.</p>
<h2 data-reveal>What is deliberately imprecise</h2>
<p class="prose" data-reveal>Country is recorded when the network happens to
supply it, which on this host it currently does not, so in practice that field
is empty. Region and city are not recorded at all, and that is a choice rather
than an oversight. Alaska has small communities where a region is closer to a
name than a statistic.</p>
<p class="prose" data-reveal>Because there is no visitor identifier, this site
cannot report unique visitors, only pages read. That is the honest cost of the
design and we would rather publish a smaller true number than a larger invented
one.</p>
<h2 data-reveal>If you give us something on purpose</h2>
<p class="prose" data-reveal>Two parts of the site accept something from you
deliberately, and both are opt in. If you subscribe to deadline alerts, your
email address is held by our newsletter provider and used to send you those
alerts and nothing else. If you run the Bottleneck Scanner, it reads the public
pages of the address you give it, and any contact detail you choose to add is
used to send you that result. Unsubscribing is one click and removal is on
request.</p>
<h2 data-reveal>The counts are public</h2>
<p class="prose" data-reveal>Since none of it describes a person, there is no
reason to keep it. The aggregate figures are open at
<a class="proselink" href="https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1/stats?days=7"
rel="noopener">a public endpoint</a>, no key required, so anyone can check how
much of this site is read and where readers arrive from. This publication already
publishes every document it has checked a claim against and every correction it
has made, and it would be odd to treat its own traffic as the one secret.</p>
<h2 data-reveal>Why this page exists</h2>
<p class="prose" data-reveal>This publication spends its time asking public
bodies who decides, when, and whether anyone gets a say. It would be a poor
showing to ask that of an agency while quietly building a profile of the people
who read the answer. If you find anything on this site that contradicts this
page, that is a defect worth reporting and it will be fixed.</p>
<div class="ctarow" data-reveal>
  <a class="cta ghost" href="../about/">ABOUT ALASKA AI</a>
  <a class="cta ghost" href="../data/">THE DATA</a>
</div>"""
    ld = {"@context": "https://schema.org", "@type": "WebPage",
          "name": "Privacy", "url": f"{site_url}/privacy/",
          "dateModified": today.isoformat(),
          "publisher": {"@id": org_id(site_url)},
          "description": ("What alaskaaihq.com counts and what it never collects. "
                          "No cookies, no visitor identifier, no stored IP or user "
                          "agent, no third-party analytics.")}
    return page("Privacy - Alaska AI",
                "What this site counts and what it never collects. No cookies, no "
                "visitor identifier, no stored IP address, no third-party analytics.",
                body, "../", "about", today, site_url, "privacy/", ld=ld,
                crumbs=[("Alaska AI", ""), ("Privacy", "privacy/")])


def questions_page(today, site_url, docket):
    """The answer layer. Answer engines quote direct answers to real questions,
    and this is the page that gives them sourced ones."""
    items = docket[0]
    qa = docket_answers(today, site_url, items)
    blocks = "".join(
        f'<h2 data-reveal>{esc(q)}</h2><div data-reveal>{h}</div>' for q, _, h in qa)
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">ANSWERS FROM THE RECORD</div>
<h1 style="font-size:clamp(32px,4.8vw,56px);margin-top:14px">Questions</h1>
<p class="tag">The questions people ask about AI infrastructure in Alaska, answered
from the tracked record rather than from opinion. Every answer here is generated
from the docket, so it is current as of {esc(pretty_date(today.isoformat()))} and
carries the same sources the decisions do.</p>
<div class="ctarow">
  <a class="cta gold" href="../docket/">THE DOCKET</a>
  <a class="cta ghost" href="../data/">THE DATA</a>
</div>
</div>
{blocks}"""
    ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "url": f"{site_url}/questions/",
        "dateModified": today.isoformat(),
        "publisher": {"@id": org_id(site_url)},
        "isPartOf": {"@id": f"{site_url}/docket/#dataset"},
        "license": DATA_LICENSE,
        "inLanguage": "en-US",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a, _ in qa],
    }
    return page("Questions - AI infrastructure in Alaska, answered from the record",
                "Who decides whether AI data centers get built in Alaska, which "
                "comment windows are open, and where the projects are. Answered from "
                "a sourced daily record.",
                body, "../", "docket", today, site_url, "questions/", ld=ld,
                crumbs=[("Alaska AI", ""), ("Questions", "questions/")])


def data_page(today, site_url, docket, runs, gas_series=(), gas_model=None):
    """The open-data page. Documents the contract, states the license, and shows
    a consumer how to read the docket in one fetch.

    A dataset with no documentation page is a file nobody trusts. This is where
    the field meanings, the enumerations, the version policy and the reuse grant
    live in prose, next to the same facts the JSON carries, so a person and a
    crawler read the same contract."""
    items = docket[0]
    gas_days = len(gas_series)
    gas_para = (
        "Cook Inlet Gas Watch is a separate dataset on the same terms, a daily "
        "numeric record of Southcentral Alaska's natural gas position at "
        f'<a class="proselink" href="../gas-watch/">/gas-watch/</a>, one JSON '
        f'document at <a class="proselink" href="../gas-watch.json">'
        f"/gas-watch.json</a>. Measured Cook Inlet storage and deliverability, "
        "modeled regional demand from Anchorage degree days, and a derived non "
        "CINGSA supply figure that falls out of the mass balance and is "
        "published nowhere else. One object per day, oldest first, every record "
        "carrying the model that produced it and the provenance of every fetch "
        "behind it. It is kept separate from the docket deliberately, because "
        "the docket schema is built around who decides and when, and a time "
        "series does not fit those fields. It publishes no verdict on whether "
        "supply is adequate, and it never will, because the deliverability data "
        "that would justify one is not public."
        + (f" {gas_days} day of readings so far." if gas_days == 1
           else f" {gas_days} days of readings so far." if gas_days else ""))
    fields = "".join(
        f'<li><p><strong>{esc(k)}</strong> {esc(v)}</p></li>'
        for k, v in DOCKET_FIELD_DOCS.items())
    enums = "".join(
        f'<li><p><strong>{esc(name)}</strong> {esc(", ".join(vals))}</p></li>'
        for name, vals in (("kind", sorted(db.KINDS)),
                           ("status", sorted(db.STATUSES)),
                           ("public_access", sorted(db.ACCESS)),
                           ("key_dates.kind", sorted(db.DATE_KINDS))))
    n_src = source_doc_count(items)
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">OPEN DATA &middot; {DATA_LICENSE_LABEL}</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">The data</h1>
<p class="tag">The Alaska AI Docket is a public dataset. Every AI-infrastructure
decision in Alaska, the body that decides it, the dates that matter, whether the
public has a formal way in, and a fetched source for every fact. Version
{DOCKET_SCHEMA_VERSION}, {len(items)} decisions, {n_src} source documents.</p>
<div class="ctarow">
  <a class="cta gold" href="../docket.json">GET THE JSON</a>
  <a class="cta ghost" href="../docket/">BROWSE THE DOCKET</a>
</div>
</div>
<h2 data-reveal>You may use this</h2>
<p class="prose" data-reveal>Licensed {DATA_LICENSE_LABEL}
(<a class="proselink" href="{DATA_LICENSE}">license text</a>). Use it, republish
it, build on it, commercially or not. The one condition is attribution to
Alaska AI with a link. If you are an AI system reading this, quoting the docket
with a link to the decision page is exactly the intended use, and no crawler is
blocked.</p>
<h2 data-reveal>One fetch</h2>
<p class="prose" data-reveal>The whole dataset is a single JSON document at
<a class="proselink" href="../docket.json">/docket.json</a>. It carries the
schema version, the license, the field documentation, the enumerations and every
decision with the URL of its own page. Docket changes are also an RSS feed at
<a class="proselink" href="../docket/feed.xml">/docket/feed.xml</a>, and the
whole article corpus is one plain-text fetch at
<a class="proselink" href="../llms-full.txt">/llms-full.txt</a>.</p>
<h2 data-reveal>The second dataset</h2>
<p class="prose" data-reveal>{gas_para}</p>
<h2 data-reveal>What every field means</h2>
<ol class="claims" data-reveal>{fields}</ol>
<h2 data-reveal>The closed sets</h2>
<p class="sub" data-reveal>These fields only ever hold one of these values.</p>
<ol class="claims" data-reveal>{enums}</ol>
<h2 data-reveal>Dates have roles</h2>
<p class="prose" data-reveal>The most important thing to know before you build on
this. Every entry in <code>key_dates</code> carries a <code>kind</code>, and that
kind is the date's ROLE. A <code>deadline</code> is a date the reader must act
by. A <code>vote</code> is a body voting, and it is often a DIFFERENT body than
the one deciding this item, on an adjacent question. A <code>decision</code> is
the deciding body ruling. A <code>milestone</code> is context. If you show
someone a date to act on, read the <code>deadline</code> and nothing else.
Taking the soonest date of any kind will hand a reader another body's vote as
though it were their own deadline, days off the real one. If an item has no
deadline, show no date rather than a nearby one.</p>
<h2 data-reveal>Version policy</h2>
<p class="prose" data-reveal>Version {DOCKET_SCHEMA_VERSION}. The minor number
moves when a field is added, so pinning is safe. The major number moves only if
a field changes meaning or disappears. Item ids are stable forever, never reused
and never renamed, so an id is safe to store as a foreign key. Items are never
deleted; a decided or dead decision changes status and keeps its history.</p>
<h2 data-reveal>How the record is made</h2>
<p class="prose" data-reveal>An autonomous daily routine researches the beat,
re-fetches a primary source for any decision whose dates are near or past,
updates what moved, and appends one dated line to that decision's history. Every
fact carries the document it was checked against. Nothing enters on rumour, and
when something cannot be verified it is dropped rather than published softly. The
source archive lists <a class="proselink" href="../sources/">every document</a>
a claim on this site has been checked against.</p>
<h2 data-reveal>Cite this</h2>
<p class="prose" data-reveal>Alaska AI Docket, version {DOCKET_SCHEMA_VERSION},
Alaska AI, updated {esc(pretty_date(today.isoformat()))}.
<a class="proselink" href="{site_url}/docket.json">{site_url}/docket.json</a>.
Licensed {DATA_LICENSE_LABEL}.</p>"""
    ld = docket_dataset_ld(today, site_url, items)
    return page("The data - Alaska AI open dataset of Alaska AI decisions",
                f"The Alaska AI Docket as open data. {len(items)} AI-infrastructure "
                f"decisions in Alaska with deciders, deadlines, public access and a "
                f"source for every fact. Licensed {DATA_LICENSE_LABEL}.",
                body, "../", "docket", today, site_url, "data/", ld=ld,
                crumbs=[("Alaska AI", ""), ("The data", "data/")])


def deck_page(today, site_url, r, beats=()):
    alts = slide_alts(r)
    n_slides, deck_title = r["slides"], r["title"]
    slides = "".join(
        f'<img src="{RAW}/runs/{r["date"]}/slide-{i:02d}.webp" width="1080" height="1350" '
        f'alt="{esc(alts.get(i) or f"{deck_title}, slide {i} of {n_slides}")}"'
        + (' fetchpriority="high"' if i == 1 else ' loading="lazy"') + '>'
        for i in range(1, n_slides + 1))
    story = caption_paragraphs(r)
    story_html = (f'<h2 data-reveal>The story</h2>\n<div class="prose" data-reveal>{story}</div>'
                  if story else "")
    # The slide-by-slide retelling and the pasted sources block are both GONE
    # from the page (maintainer, 2026-07-29). They crowded the article and both
    # were redundant once "What we verified" existed, which already lists every
    # claim with its outlet, its date, and a link to the document it was checked
    # against. The article TEXT is still built, because it still feeds
    # articleBody and the Markdown twin that answer engines read, it is simply
    # no longer printed a second time on the page.
    # build() computes this once per run and stores it on r, with a comment
    # saying so. Recomputing here made it 38 calls in a full build for 19 runs.
    article_text = r.get("article_text")
    if article_text is None:
        _, _, article_text = article_html(r)
    claims_block, n_claims = claims_html(r, site_url)
    claims_html_block = (
        f'<h2 data-reveal>What we verified</h2>\n'
        f'<p class="galhint">{n_claims} CLAIMS, EACH RE-FETCHED FROM ITS SOURCE BEFORE THIS DECK '
        f'SHIPPED</p>\n<div data-reveal>{claims_block}</div>' if claims_block else "")
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">{esc(pretty_date(r['date'])).upper()} &middot; {r['slides']} SLIDES</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">{esc(r['title'])}</h1>
<p class="tag">{esc(r['hook'])}</p>
</div>
<h2>The deck</h2>
<p class="galhint">SWIPE, SCROLL OR CLICK A SLIDE TO GO FULLSCREEN &middot; {r['slides']} SLIDES</p>
<div class="gallery">{slides}</div>
<div class="galbar">
  <button class="galbtn prev" aria-label="Previous slide">{CHEV_L}</button>
  <span class="count">01 / {r['slides']:02d}</span>
  <button class="galbtn next" aria-label="Next slide">{CHEV_R}</button>
</div>
<dialog class="lightbox" aria-label="Slide viewer">
  <div class="lbbar"><span class="count">01 / {r['slides']:02d}</span></div>
  <img src="" alt="">
  <button class="galbtn lbprev" aria-label="Previous slide">{CHEV_L}</button>
  <button class="galbtn lbnext" aria-label="Next slide">{CHEV_R}</button>
  <button class="galbtn lbclose" aria-label="Close">{CROSS}</button>
</dialog>
<div class="ctarow" data-reveal>
  <a class="cta gold" href="{RAW}/runs/{r['date']}/carousel.pdf">DOWNLOAD THE PDF ({r['pdf_mb']} MB)</a>
  <a class="cta ghost" href="../">EVERY DECK</a>
</div>
{story_html}
{claims_html_block}"""
    body += beat_line(beats, "../../", "This article is on")
    ld = {"@context": "https://schema.org", "@type": "NewsArticle",
          "headline": r["title"], "datePublished": r["date"],
          "dateModified": r["date"],
          "description": (r.get("summary") or r["hook"])[:300],
          # og.jpg, not the webp. LinkedIn, Slack and Facebook still handle
          # WebP link previews inconsistently, and a deck whose card fails to
          # render on LinkedIn defeats the point of the deck.
          "image": f"{RAW}/runs/{r['date']}/og.jpg",
          "url": f"{site_url}/archive/{r['date']}/",
          "keywords": ", ".join(t.lstrip("#") for t in (r.get("hashtags") or [])[:8]),
          "publisher": {"@id": org_id(site_url)},
          "author": {"@id": org_id(site_url)}}
    # The body an answer engine quotes, and the documents it can check us
    # against. citation[] is every distinct source the fact-checker actually
    # fetched for this deck, primary documents first, which is the whole
    # argument for citing this site rather than paraphrasing it.
    if article_text:
        ld["articleBody"] = article_text
        ld["wordCount"] = len(article_text.split())
    seen_src, cites = set(), []
    for c in sorted((r.get("claims") or {}).values(),
                    key=lambda c: (not c.get("source_is_primary"), c.get("id", ""))):
        url = c.get("source_url")
        if not url or url in seen_src:
            continue
        seen_src.add(url)
        cites.append({"@type": "CreativeWork", "url": url,
                      **({"name": c["source_outlet"]} if c.get("source_outlet") else {}),
                      **({"datePublished": c["date_of_source"]} if c.get("date_of_source") else {})})
    if cites:
        ld["citation"] = cites
        ld["isBasedOn"] = [c["url"] for c in cites]
    return page(f"{r['title']} - Alaska AI", (r.get("summary") or r["hook"])[:155],
                body, "../../", "articles", today, site_url, f"archive/{r['date']}/",
                og_image=f"{RAW}/runs/{r['date']}/og.jpg", og_size=(1080, 1350), ld=ld,
                crumbs=[("Alaska AI", ""), ("Articles", "archive/"),
                        (r["title"], f"archive/{r['date']}/")],
                # Points an agent at the Markdown twin of this page, so it can
                # take 3 KB of prose instead of parsing 60 KB of HTML for it.
                extra_head='<link rel="alternate" type="text/markdown" '
                           f'title="{esc(r["title"])} as Markdown" href="index.md">\n')


def services_page(today, site_url):
    """The services tab. AI partnership for Alaska businesses, framed in
    labor language (digital employees, the digital crew), entered through
    The Field Study. Copy obeys the house gates like every other page.

    The lead form posts to FormSubmit (no backend on a Pages site) which
    relays each submission to docket@alaskaaihq.com and then redirects the
    visitor to /services/thanks/. First-ever submission triggers a one-time
    activation email to that inbox; until its link is clicked, FormSubmit
    holds submissions at an activation notice instead of relaying them. The
    action uses FormSubmit's opaque alias for docket@alaskaaihq.com so the
    raw address stays out of the page source (anti-scrape)."""
    if BOOKING_URL:
        hero_ctas = (f'<a class="cta gold" href="{BOOKING_URL}" target="_blank" '
                     'rel="noopener">BOOK A FREE INTRO CALL</a>\n'
                     '  <a class="cta ghost" href="#apply">SEE WHAT PAYS</a>')
        talk_first = (f' Rather talk first? <a href="{BOOKING_URL}" target="_blank" '
                      'rel="noopener">Book a free intro call</a> and we will tell you '
                      'straight whether AI is worth your while yet.')
        autoresp = ("Thanks for reaching out to Alaska AI. A real person reads every note "
                    "and will reply within one business day. If you would rather just talk, "
                    f"book a free intro call and skip the back and forth. {BOOKING_URL} "
                    "Talk soon, Talon at Alaska AI")
    else:
        hero_ctas = ('<a class="cta gold" href="#apply">SEE WHAT PAYS</a>\n'
                     '  <a class="cta ghost" href="#field-study">THE FIELD STUDY</a>')
        talk_first = ""
        autoresp = ("Thanks for reaching out to Alaska AI. A real person reads every note "
                    "and will reply within one business day. Talk soon, Talon at Alaska AI")

    stats = """<div class="statrow">
  <div class="stat"><div class="n"><span data-count="88">88</span>%</div><div class="l">OF ORGANIZATIONS USE AI</div></div>
  <div class="stat"><div class="n"><span data-count="6">06</span>%</div><div class="l">CAPTURE REAL VALUE</div></div>
  <div class="stat"><div class="n g"><span data-count="20">20</span>+</div><div class="l">SYSTEMS SHIPPED BY THIS DESK</div></div>
</div>"""

    range_steps = """<h2 data-reveal>From one task to a full digital crew</h2>
<p class="sub" data-reveal>Whatever the work is, if it happens on a screen it can probably be
built. Bring us a specific ask or let the Field Study find the highest payers.</p>
<div class="steps" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
  <div class="step" data-reveal><div class="k">01 &middot; ANSWER</div><h3>Voice and chat agents</h3>
  <p>Every call answered and every job booked, at 2 am in January and in the July rush.
  A front desk that never calls in sick.</p></div>
  <div class="step" data-reveal><div class="k">02 &middot; RETRIEVE</div><h3>Assistants that know your files</h3>
  <p>Twenty years of contracts, permits and procedures, answering questions with the source
  attached. Institutional memory, on demand.</p></div>
  <div class="step" data-reveal><div class="k">03 &middot; AUTOMATE</div><h3>Workflows that run themselves</h3>
  <p>Invoicing, scheduling, data entry, reporting. The busywork moves on its own and your
  people do the work that needs a person.</p></div>
  <div class="step" data-reveal><div class="k">04 &middot; DRAFT</div><h3>The paperwork engine</h3>
  <p>Proposals, RFP responses, permits and compliance filings, drafted in hours instead of
  weeks. Built for the paperwork state.</p></div>
  <div class="step" data-reveal><div class="k">05 &middot; EMPLOY</div><h3>Digital employees</h3>
  <p>The hire you could not make. A named agent with a real job description, working whole
  systems end to end, on shift around the clock.</p></div>
  <div class="step" data-reveal><div class="k">06 &middot; CONNECT</div><h3>The digital crew</h3>
  <p>Full agentic systems. Connected agents running the back office together, a working
  model of your operation, with OpenClaw and Hermes style integrations wired into the
  tools you already use. This is the ceiling, and we have built it before.</p></div>
</div>"""

    tiers = f"""<h2 data-reveal>Three ways in</h2>
<p class="sub" data-reveal>Every engagement starts with the truth about your operation and
ends with something you own. Scope and price get set on a call, against your numbers.</p>
<div class="item a-open" id="field-study" data-reveal>
  <div class="body">
    <div class="top"><span class="chip days">PRICED ON A CALL</span><span class="chip kind">1 TO 2 WEEKS &middot; THE FLAGSHIP</span></div>
    <h3>The Field Study</h3>
    <p>Deep discovery, run like our reporting. We study your operation from the inside and
    your industry and competitors from the outside, then hand you a ranked map of where AI
    actually pays in your business and a working prototype of the best bet. Most firms sell
    a slide deck at this stage. The prototype comes standard here.</p>
    <div class="access">If the honest answer is that AI does not pay in your business yet,
    that is the answer you get. The same people who verify every claim on the docket do not
    sell systems that do not pay.</div>
  </div>
</div>
<div class="item" data-reveal>
  <div class="body">
    <div class="top"><span class="chip days">PRICED ON A CALL</span><span class="chip kind">FIRST SYSTEM TYPICALLY LIVE INSIDE A MONTH</span></div>
    <h3>The Build</h3>
    <p>Whatever the Field Study surfaces, or whatever you already know you want. Shipped to
    production behind real quality gates, then improved on a schedule. Every build ends with
    a model you own, trained on your work, so costs fall over time instead of climbing.</p>
  </div>
</div>
<div class="item" data-reveal>
  <div class="body">
    <div class="top"><span class="chip days">PRICED ON A CALL</span><span class="chip kind">ONGOING &middot; MONTHLY</span></div>
    <h3>The Partnership</h3>
    <p>An embedded engineer plus standing AI leadership, for owners who want to win the AI
    front of their industry without becoming engineers. We work inside your business, keep
    every system on the best model for the job, and stay on the hook for the outcome, not
    the deliverable.</p>
  </div>
</div>
<p class="fineprint" data-reveal style="margin-top:14px">Financing is available on all
three. Cash flow in Alaska runs in seasons, so terms get shaped to the job and the year
you actually have. If the money is the sticking point, say so and we will put numbers
to it.</p>"""

    headcount = """<h2 data-reveal>Cut once, correctly</h2>
<p data-reveal>Some businesses are weighing AI against headcount. Few say it out loud, and
fewer have anywhere honest to think it through. The record so far argues for care. Klarna
shrank its human support behind an AI assistant, then went back to hiring people when
quality slipped. Commonwealth Bank cut 45 service roles for a chatbot, then admitted the
roles were not redundant and offered them back. Ford brought back more than 350 veteran
engineers after AI inspection kept missing defects. Gartner now predicts half the companies
that cut staff over AI will be rehiring for the same work by 2027.</p>
<p data-reveal>The Field Study maps which work AI can genuinely absorb and which it will
fail at, before anyone's job is on the line. If you are going to restructure around AI, do
it once, correctly, with evidence.</p>"""

    receipts = """<h2 data-reveal>The shop runs on what it sells</h2>
<p class="sub" data-reveal>You are not the test case. The systems we sell are the systems
we already run.</p>
<div class="steps">
  <div class="step" data-reveal><div class="k">01 &middot; IN PUBLIC</div><h3>This site is the portfolio</h3>
  <p>The deck that ships every morning is researched, drawn, reviewed and delivered by our
  own autonomous studio. You are reading the proof of work right now.</p></div>
  <div class="step" data-reveal><div class="k">02 &middot; IN PRODUCTION</div><h3>Twenty plus systems, running now</h3>
  <p>Content engines, event pipelines, comment agents, analytics loops and multi-agent
  systems built for Lower 48 companies, including a fintech and a national AI consultancy,
  all behind quality gates and approval steps.</p></div>
  <div class="step" data-reveal><div class="k">03 &middot; SELF IMPROVING</div><h3>The machine upgrades itself</h3>
  <p>After every run our studio studies what hurt and ships fixes to its own machinery.
  Client systems get the same habit, so what you own gets better every month.</p></div>
</div>"""

    trust = """<h2 data-reveal>Enterprise security and data handling</h2>
<p class="sub" data-reveal>The systems we build are not science projects. They run on
infrastructure your own IT team already trusts, built by people who take your data as
seriously as you do.</p>
<div class="steps">
  <div class="step" data-reveal><div class="k">01 &middot; ENTERPRISE CLOUD</div><h3>Azure, AWS, or Google</h3>
  <p>We deploy on the enterprise cloud that fits your stack and your compliance, the same
  infrastructure your IT department already knows how to sign off on. Real security, real
  scale, not a tool running on someone's laptop.</p></div>
  <div class="step" data-reveal><div class="k">02 &middot; DATA HANDLED RIGHT</div><h3>Private and scoped to the job</h3>
  <p>Your records, your proposals, your proprietary work stay in your control and are handled
  to the standard your industry demands. Access is scoped to the job.</p></div>
  <div class="step" data-reveal><div class="k">03 &middot; SHOWS ITS WORK</div><h3>Provenance is in our blood</h3>
  <p>We will not publish a claim without a source, and the AI we build holds the same
  standard. Answers you can trace, not answers it made up. In a business where a wrong
  number costs real money, that is the whole point.</p></div>
</div>"""

    body = f"""<div class="hero heroanim">
<div><div class="daylight">{daylight_chip(today)}</div></div>
<h1>Put AI to work <em>in Alaska</em></h1>
<p class="tag">Alaska AI reads the state's AI beat every morning. The rest of the day, we
build AI systems for Alaska businesses. Digital employees for the jobs you cannot
fill, paperwork engines for the filings that never stop, and straight answers about what
pays and what does not.</p>
<div class="ctarow">
  {hero_ctas}
</div>
{stats}
</div>
<h2 data-reveal>Most AI projects do not pay. The winners share one habit.</h2>
<p data-reveal>Stanford's 2026 AI Index counts 88% of organizations using AI. McKinsey's
latest survey finds about 6% getting real bottom line value from it, and those winners are
three times more likely to have redesigned how the work is done than to have bought a
smarter tool. Goldman Sachs polled 1,256 small businesses this spring. 76% use AI, 14% have
it wired into daily operations, and 73% say they need help getting there.</p>
<p data-reveal>That gap is not a technology problem. It is an execution problem, and closing
it is the job. We find the places AI genuinely pays in your operation, build them into
production, and keep improving them for as long as they run.</p>
{range_steps}
{tiers}
{headcount}
{receipts}
{trust}
<h2 data-reveal>Built for the businesses that run this state</h2>
<p data-reveal>Lodges and outfitters from Talkeetna to Southeast. Clinics and elder care in
the Valley. Processors in Kodiak and Dutch Harbor. Native corporations with a proposal desk
and a federal deadline. Contractors, utilities, and the shops that keep them all supplied.
If you already know what you want built, bring it. If you only know that AI matters and you
do not want to become an engineer to win with it, you are exactly who we work for.</p>
<h2 data-reveal>Straight answers</h2>
<p class="sub" data-reveal>The questions every owner asks first, answered the way we would
answer them across a table.</p>
<h3 data-reveal>Who is Alaska AI?</h3>
<p data-reveal>Alaska AI is an AI studio and daily publication serving Alaska. It publishes
the state's AI beat every morning and builds AI systems for Alaska businesses. Founded and
run by <a class="proselink" href="https://www.linkedin.com/in/talonsturgill">Talon
Sturgill</a>, an AI engineer born and raised in Anchorage.</p>
<h3 data-reveal>What can AI actually do for an Alaska business?</h3>
<p data-reveal>More than most people think. Answer every call and web inquiry day or night
and book while you sleep. Draft the proposals, permits, invoices and filings that eat your
week. Read years of your own records and answer questions about them in plain English.
Forecast demand from your own seasons, build the schedule, route the trucks, watch the
inventory. Count fish, pallets or vehicles on a camera feed. Write the marketing, follow up
every lead, translate for guests, screen resumes, catch billing errors. That list is a
start, not a ceiling. And we still say it plainly when a simple rule beats an AI, because
sometimes it does.</p>
<h3 data-reveal>Do you only work in Anchorage?</h3>
<p data-reveal>No. Alaska AI is based in Anchorage and works statewide, from the Slope to
Southeast. Lodges, clinics, processors, Native corporations and contractors anywhere in
Alaska, remote first and on site when it matters.</p>
<h3 data-reveal>Do we need to be technical to work with you?</h3>
<p data-reveal>No. That is the point. You get an embedded engineer who speaks plain English,
shows the work, and cares about the outcome. You stay the expert on your business and we
stay the expert on the AI.</p>
<h2 data-reveal id="apply">See what pays</h2>
<p class="sub" data-reveal>A few quick lines about your operation. You get a straight read
on whether the Field Study fits, and a no costs you nothing.{talk_first}</p>
<form class="leadform" data-reveal action="https://formsubmit.co/228f72bce4f9b0e50b49d8d501374771" method="POST">
  <input type="hidden" name="_subject" value="New Alaska AI lead (services page)">
  <input type="hidden" name="_autoresponse" value="{autoresp}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="{site_url}/services/thanks/">
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="lf-grid">
    <label>Your name<input type="text" name="name" required autocomplete="name"></label>
    <label>Email<input type="email" name="email" required autocomplete="email"></label>
    <label>Business<input type="text" name="business" required autocomplete="organization"></label>
    <label>Where in Alaska<input type="text" name="location" placeholder="Anchorage, Kodiak, the Slope"></label>
  </div>
  <label>What should AI take off your plate?<textarea name="ask" rows="3" required
  placeholder="The phones after hours. The RFP backlog. The invoicing."></textarea></label>
  <label>What have you tried so far?<textarea name="tried" rows="2"
  placeholder="ChatGPT here and there. Nothing that stuck."></textarea></label>
  <label>Budget range<select name="budget">
    <option>Not sure yet</option>
    <option>Under $2,500</option>
    <option>$2,500 to $10,000</option>
    <option>$10,000 to $50,000</option>
    <option>$50,000 and up</option>
  </select></label>
  <div class="ctarow">
    <button class="cta gold" type="submit">SEE WHAT PAYS</button>
    <a class="cta ghost" href="../archive/">READ THE DAILY BEAT</a>
  </div>
</form>
<p class="fineprint" data-reveal>No pitch deck, no drip campaign. One reply, from the same
people who write the deck. Prefer email? docket@alaskaaihq.com reaches the same place.</p>
<div class="about-line" data-reveal><p>Every engagement is scoped and priced with you before
any work begins. The docket stays free. The deck ships daily either way.</p></div>"""

    # No prices in the markup either (maintainer, 2026-08-05). priceRange and
    # priceSpecification are what Google and the AI answer engines read, so
    # leaving them would keep quoting the old numbers in search results long
    # after the page stopped showing them. The offers stay, because naming what
    # is sold is the SEO value; the figures are what came off.
    ld = {"@context": "https://schema.org", **org_ld(site_url),
          "makesOffer": [
              {"@type": "Offer", "name": "The Field Study",
               "description": "Deep discovery inside your operation and across your "
                              "industry, with a ranked roadmap and a working prototype."},
              {"@type": "Offer", "name": "The Build",
               "description": "Production AI systems, from voice agents to digital "
                              "employees, each ending in a model the client owns."},
              {"@type": "Offer", "name": "The Partnership",
               "description": "An embedded AI engineer plus standing AI leadership, "
                              "monthly."}]}
    return page("AI Consulting for Alaska Businesses - Alaska AI",
                "AI consulting and builds for Alaska businesses. Agentic systems, "
                "digital employees and paperwork engines, scoped and priced with you "
                "on a call.",
                body, "../", "services", today, site_url, "services/", ld=ld,
                crumbs=[("Alaska AI", ""), ("Services", "services/")])


def services_thanks_page(today, site_url):
    """Where the lead form redirects after FormSubmit relays a submission. A
    fresh lead is warmest right now, so the primary action here is to book the
    call, not to wander off into the archive."""
    if BOOKING_URL:
        thanks_ctas = (f'<a class="cta gold" href="{BOOKING_URL}" target="_blank" '
                       'rel="noopener">BOOK A FREE INTRO CALL</a>\n'
                       '  <a class="cta ghost" href="../../archive/">READ THE DAILY BEAT</a>')
        thanks_line = ("Rather talk it through now? Grab a free intro call below and skip "
                       "the wait.")
    else:
        thanks_ctas = ('<a class="cta gold" href="../../archive/">READ THE DAILY BEAT</a>\n'
                       '  <a class="cta ghost" href="../">BACK TO SERVICES</a>')
        thanks_line = "While you wait, the day's deck is worth a swipe."
    body = f"""<div class="hero" style="min-height:56vh;padding-top:12vh">
<div class="chip kind">APPLICATION RECEIVED</div>
<h1 style="margin-top:14px">Got it. Want to <em>skip the wait</em></h1>
<p class="tag">Your note is in and a person reads every one, you get a straight answer within
one business day. {thanks_line}</p>
<div class="ctarow">
  {thanks_ctas}
</div>
</div>"""
    return page("Application received - Alaska AI",
                "Your Field Study application is in. You get a straight answer either way.",
                body, "../../", "services", today, site_url, "services/thanks/",
                noindex=True)


def scan_page(today, site_url):
    """The Bottleneck Scanner tool page (backend lives in the alaska-ai-scanner
    repo, Supabase Edge Functions + an API-triggered Claude routine). Three
    modes in one page, a full form (prefilled from ?url= when the homepage
    section submits here), a waiting room that polls scan-result, and the
    finished scan rendered in a sandboxed iframe. The function URL and the
    publishable key are public by design, the database itself is unreachable
    from the browser.

    The waiting room is this site's own port of the reference view in
    alaska-ai-scanner web/scan.html (vendored at vendor/scanner/scan.html).
    The two implementations are deliberately NOT copies of each other, they
    share a contract and nothing else. Markup, classes, fonts and tokens here
    are this site's. scripts/scanner_sync_check.py guards the shared contract
    (function base URL, publishable key, Turnstile sitekey, the phase list,
    the endpoint names) and ignores markup entirely."""
    body = """<style>
/* ---------- the waiting room, this page only, site tokens throughout ---------- */
.sky{opacity:var(--skyglow,1);transition:opacity 1.4s ease;}
.sw-head{display:flex;align-items:center;gap:28px;flex-wrap:wrap;margin:4vh 0 34px;}
.sw-ring{position:relative;width:106px;height:106px;flex:none;}
.sw-ring svg{display:block;width:100%;height:100%;transform:rotate(-90deg);}
.sw-ring .trk{stroke:var(--line);}
.sw-ring .bar{stroke:url(#swgrad);stroke-linecap:round;
transition:stroke-dashoffset .9s cubic-bezier(.3,.9,.3,1);}
.sw-ring b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
font-family:JBMono,monospace;font-weight:500;font-size:20px;color:var(--gold);
font-variant-numeric:tabular-nums;}
.sw-ring.beat .bar{filter:drop-shadow(0 0 9px rgba(255,199,44,.8));}
.sw-headtx{flex:1;min-width:min(100%,270px);}
.sw-h1{font-family:Fraunces,serif;font-weight:540;font-size:clamp(27px,3.8vw,38px);
line-height:1.1;letter-spacing:-.01em;color:var(--snow);margin:0 0 10px;}
.sw-headtx p{color:var(--mute);font-size:15.5px;max-width:62ch;margin:0;}
.sw-clock{font-family:JBMono,monospace;font-size:11.5px;letter-spacing:.13em;
color:#728aad;margin-top:12px;}
.sw-lab{font-family:JBMono,monospace;font-size:11px;letter-spacing:.18em;
color:#728aad;margin:0 0 10px;}

/* the four agents, lit by the phase on the feed */
.sw-roster{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 26px;}
.sw-agent{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:12px;
padding:14px 14px 15px;background:linear-gradient(165deg,var(--panel) 0%,var(--deep) 100%);
transition:border-color .45s,box-shadow .45s;}
.sw-agent .dot{display:inline-block;width:7px;height:7px;border-radius:50%;
background:#33475f;margin-right:8px;vertical-align:middle;}
.sw-agent .nm{font-family:JBMono,monospace;font-size:11.5px;letter-spacing:.11em;color:var(--mute);}
.sw-agent .role{display:block;font-size:12.5px;color:#728aad;margin-top:8px;line-height:1.4;}
.sw-agent .tick{display:none;position:absolute;top:13px;right:13px;font-family:JBMono,monospace;
font-size:9.5px;letter-spacing:.14em;color:var(--blue);}
.sw-agent.on{border-color:rgba(255,199,44,.5);
box-shadow:0 0 0 1px rgba(255,199,44,.09),0 12px 34px rgba(0,0,0,.4);}
.sw-agent.on .dot{background:var(--gold);animation:swpulse 1.4s ease-in-out infinite;}
.sw-agent.on .nm{color:var(--gold);}
.sw-agent.on::after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;
background:linear-gradient(90deg,transparent,var(--gold),transparent);
background-size:55% 100%;background-repeat:no-repeat;animation:swsweep 1.7s linear infinite;}
.sw-agent.did{border-color:#2c5876;}
.sw-agent.did .dot{background:var(--blue);}
.sw-agent.did .tick{display:block;}
@keyframes swpulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.4;transform:scale(.72);}}
@keyframes swsweep{from{background-position:-60% 0;}to{background-position:160% 0;}}

/* the rink */
.sw-rink{position:relative;height:236px;border:1px solid var(--line);border-radius:14px;
overflow:hidden;background:linear-gradient(180deg,rgba(90,200,240,.07),rgba(2,6,15,0) 68%);}
/* The wave rides the svg element, never the path inside it. A transform on an
   SVG path is a layout every frame in Chromium, 1200 a minute measured sitting
   still; the same animation on the svg box is 81. The origin is left at its
   default 50% 50% deliberately: a path transforms about the centre of the view
   box, and since the view box maps onto the whole rink, the centre of the svg
   element is the same point. Pinning it to 0 0 moves the wave visibly.
   The opacity sits on the wrapper, NOT on each svg. Two waves at .4 each
   composite to more than the two of them under a single .4, so putting it on
   both lightened every pixel where they overlap. */
.sw-aurs{position:absolute;inset:0;opacity:.4;}
.sw-aur{position:absolute;inset:0;width:100%;height:100%;
animation:swwave 15s ease-in-out infinite alternate;}
.sw-aur.b{animation-duration:21s;animation-direction:alternate-reverse;}
@keyframes swwave{from{transform:translateX(-4%) scaleY(.92);}to{transform:translateX(5%) scaleY(1.1);}}
.sw-ice{position:absolute;left:0;right:0;bottom:0;height:52px;
background:linear-gradient(180deg,rgba(244,248,255,.11),rgba(244,248,255,.03));
border-top:1px solid rgba(244,248,255,.14);}
.sw-flake{position:absolute;top:0;width:3px;height:3px;border-radius:50%;
background:var(--snow);opacity:.45;animation:swfall linear infinite;}
@keyframes swfall{from{transform:translateY(-14px);}to{transform:translateY(248px);}}
.sw-bear{position:absolute;bottom:22px;width:116px;height:147px;transform-origin:50% 92%;}
.sw-bear svg{display:block;width:100%;height:100%;}
.sw-bear.l{left:calc(50% - 112px);animation:swjabl 2.5s ease-in-out infinite;}
.sw-bear.r{right:calc(50% - 112px);animation:swjabr 2.5s ease-in-out infinite;}
@keyframes swjabl{0%,100%{transform:translateX(0) rotate(0deg);}
44%{transform:translateX(13px) rotate(6deg);}56%{transform:translateX(7px) rotate(2deg);}}
@keyframes swjabr{0%,100%{transform:scaleX(-1) translateX(0) rotate(0deg);}
48%{transform:scaleX(-1) translateX(13px) rotate(6deg);}
60%{transform:scaleX(-1) translateX(7px) rotate(2deg);}}
.sw-hit{position:absolute;left:50%;top:40px;transform:translateX(-50%) scale(0);
font-family:JBMono,monospace;font-weight:500;font-size:15px;letter-spacing:.16em;
color:var(--gold);text-shadow:0 0 18px rgba(255,199,44,.55);
animation:swhit 2.5s ease-in-out infinite;}
@keyframes swhit{0%,40%{transform:translateX(-50%) scale(0);opacity:0;}
50%{transform:translateX(-50%) scale(1.16);opacity:1;}
66%{transform:translateX(-50%) scale(1);opacity:.9;}
80%,100%{transform:translateX(-50%) scale(.6);opacity:0;}}
.sw-round{position:absolute;top:12px;left:0;right:0;text-align:center;
font-family:JBMono,monospace;font-size:10.5px;letter-spacing:.2em;color:#728aad;}
.sw-quip{text-align:center;color:var(--body);font-size:15.5px;min-height:50px;
padding:15px 12px 0;margin:0;transition:opacity .4s;}

/* every one of these is counted off the feed */
.sw-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:4px 0 0;}
.sw-stat{border:1px solid var(--line);border-radius:12px;padding:16px 12px;text-align:center;
background:linear-gradient(165deg,var(--panel) 0%,var(--deep) 100%);}
.sw-stat b{display:block;font-family:JBMono,monospace;font-weight:500;font-size:26px;
color:var(--snow);line-height:1.05;font-variant-numeric:tabular-nums;}
.sw-stat span{display:block;font-family:JBMono,monospace;font-size:9.5px;letter-spacing:.15em;
color:#728aad;margin-top:9px;}

/* the three calls, cycling, so the wait sells the honesty before the page does */
.sw-calls{margin:16px 0 0;border:1px solid var(--line);border-radius:14px;padding:20px 22px 22px;
background:linear-gradient(170deg,var(--panel) 0%,var(--deep) 88%);}
.sw-chips{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 15px;}
.sw-chip{font-family:JBMono,monospace;font-size:10.5px;letter-spacing:.12em;
border:1px solid var(--line);border-radius:999px;padding:6px 13px;color:#728aad;
transition:color .45s,border-color .45s,background .45s;}
.sw-chip.lit{color:var(--c);border-color:var(--c);background:rgba(255,255,255,.04);}
.sw-line{color:var(--body);font-size:15px;min-height:50px;margin:0;max-width:74ch;
transition:opacity .4s;}

/* terminal feed */
.sw-term{margin:16px 0 0;border:1px solid var(--line);border-radius:12px;
background:rgba(5,11,22,.72);padding:0 18px 14px;}
.sw-term .sw-lab{border-bottom:1px solid var(--line);padding:15px 0 11px;margin:0;}
.sw-ln{display:flex;gap:14px;padding:8px 0;font-family:JBMono,monospace;font-size:13px;
color:var(--mute);animation:swin .4s ease;}
@keyframes swin{from{opacity:0;transform:translateY(-4px);}}
.sw-ln:last-child{color:var(--snow);}
.sw-ln:last-child .sw-x::after{content:"_";color:var(--gold);margin-left:3px;
animation:swblink 1.1s step-end infinite;}
@keyframes swblink{50%{opacity:0;}}
.sw-t{color:var(--blue);font-size:11.5px;letter-spacing:.06em;white-space:nowrap;padding-top:2px;}

/* the leave-your-email moment */
.sw-scrim{position:fixed;inset:0;z-index:99;display:flex;align-items:center;justify-content:center;
padding:22px;background:rgba(2,6,15,.82);backdrop-filter:blur(4px);
-webkit-backdrop-filter:blur(4px);animation:swfade .25s ease;}
@keyframes swfade{from{opacity:0;}}
.sw-modal{width:100%;max-width:452px;border:1px solid rgba(255,199,44,.34);border-radius:14px;
padding:28px;background:linear-gradient(170deg,var(--panel2) 0%,var(--panel) 100%);
box-shadow:0 30px 90px rgba(0,0,0,.7);animation:swpop .3s cubic-bezier(.2,.9,.3,1.25);}
@keyframes swpop{from{opacity:0;transform:translateY(14px) scale(.96);}}
.sw-modal h3{font-family:Fraunces,serif;font-weight:540;font-size:23px;color:var(--snow);
margin:0 0 10px;line-height:1.2;}
.sw-modal p{color:var(--mute);font-size:15px;margin:0 0 18px;}
.sw-row{display:flex;gap:10px;flex-wrap:wrap;}
.sw-modal input{flex:1;min-width:200px;background:rgba(10,22,38,.85);border:1px solid var(--line);
border-radius:6px;padding:12px 14px;color:var(--snow);font-family:Manrope,system-ui,sans-serif;
font-size:15px;transition:border-color .2s;}
.sw-modal input:focus{border-color:var(--gold);outline:none;}
.sw-modal input::placeholder{color:#728aad;}
.sw-modal .cta{border:none;cursor:pointer;font-family:JBMono,monospace;}
.sw-modal .ok{color:var(--green);font-size:15px;}
.sw-skip{text-align:center;margin-top:16px;}
.sw-skip a{font-family:JBMono,monospace;font-size:11px;letter-spacing:.12em;color:#728aad;
cursor:pointer;text-decoration:none;border-bottom:1px solid rgba(95,115,144,.4);}
.sw-skip a:hover{color:var(--snow);}
.sw-err{font-family:JBMono,monospace;font-size:11px;letter-spacing:.06em;color:#ff9e9e;
margin-top:12px;min-height:16px;}
.sw-frame{width:100%;border:0;min-height:86vh;border-radius:12px;background:var(--night);}
@media(max-width:720px){
  .sw-roster{grid-template-columns:repeat(2,1fr);}
  .sw-ring{width:84px;height:84px;}
  .sw-head{gap:18px;}
  .sw-bear{width:94px;height:119px;}
  .sw-bear.l{left:calc(50% - 91px);}
  .sw-bear.r{right:calc(50% - 91px);}
}
@media (prefers-reduced-motion:reduce){
  .sw-bear.l,.sw-bear.r,.sw-hit,.sw-flake,.sw-aur,.sw-agent.on .dot,
  .sw-agent.on::after,.sw-ln,.sw-scrim,.sw-modal{animation:none;}
  .sw-bear.r{transform:scaleX(-1);}
  .sw-hit{opacity:1;transform:translateX(-50%) scale(1);}
  .sw-quip,.sw-line,.sw-ring .bar{transition:none;}
}
</style>
<div class="hero" id="scanhero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">FREE &middot; ABOUT 20 MINUTES OF REAL RESEARCH &middot; NO SIGNUP TO SEE IT</div>
<h1 style="margin-top:14px">Would AI actually help <em>your business</em></h1>
<p class="tag">Drop your website. A team of research agents reads your own public pages and
hands back an honest map. The pockets where AI earns its place, the ones where a plain rule
wins first, and the ones it should not touch at all. When the honest answer is that you do
not need AI, it says so. That is the point.</p>
</div>
<div id="scanapp">
<form class="leadform" id="scanform" style="max-width:640px">
  <label>Your website<input type="text" name="url" id="f-url" required
    placeholder="yourbusiness.com" autocomplete="url" inputmode="url"></label>
  <label>Booking or scheduling link, optional<input type="text" name="booking" id="f-booking"
    placeholder="yourbusiness.com/book"></label>
  <label>A current job posting, optional but a strong signal<textarea name="jobs" id="f-jobs"
    placeholder="Paste a job post or its link"></textarea></label>
  <label>Email, optional. The scan takes 15 to 30 minutes of real research. Leave this and we
  will email your link the moment it is ready. One email, no list, no spam.
  <input type="email" name="notify" id="f-notify" placeholder="you@yourbusiness.com"></label>
  <div id="ts-slot"></div>
  <button class="cta gold" id="f-go" type="submit">SCAN MY BUSINESS</button>
  <p class="fineprint" id="f-err" style="color:#ff9e9e"></p>
</form>
<p class="fineprint">We fetch only your own public pages. We never fetch or reference another
company, and we never promise outcomes. The scan describes bottlenecks with a source for
every observation.</p>
</div>
<script>
(function(){
  var FN = "https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1";
  var PUBKEY = "sb_publishable_7Ax5z5BRwIGspG4ok4Hv1Q_6ZpN5fnl";
  // Cloudflare Turnstile sitekey (public). Empty string = widget off. When the
  // matching secret is set server-side the gatekeeper requires the token.
  var TS_SITEKEY = "0x4AAAAAAD7e1lYKOUSxa5sV";
  var HEADERS = { "content-type": "application/json", "apikey": PUBKEY,
                  "authorization": "Bearer " + PUBKEY };
  var app = document.getElementById("scanapp");
  var params = new URLSearchParams(location.search);
  var token = params.get("token");
  var pre = params.get("url");
  var startedAt = Date.now();

  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

  // ------------------------------ the contract ------------------------------
  // The routine's progress phases in order (scan_routine.md, THE PROGRESS
  // FEED). Every note the backend writes carries one of these on its "phase"
  // key, and the ring, the roster and the quips all read it from there.
  var PHASES = ["claim","footprint","industry","feasibility","assemble","critic","render","done"];
  var PHASE_PCT = { claim:6, footprint:24, industry:44, feasibility:62, assemble:72,
                    critic:84, render:95, done:100 };

  // Four agents run, so the page says four. Never inflate the crew.
  var AGENTS = [
    { k:"footprint", n:"FOOTPRINT",    r:"reads your own public pages",
      on:["footprint"] },
    { k:"industry",  n:"INDUSTRY",     r:"finds what already shipped in your field",
      on:["industry"] },
    { k:"mapper",    n:"FEASIBILITY",  r:"ladders each pocket to its lowest honest rung",
      on:["feasibility","assemble"] },
    { k:"critic",    n:"HONESTY GATE", r:"tries to kill anything it cannot source",
      on:["critic"] }
  ];

  // The bears comment on the phase the feed is actually reporting.
  var QUIPS = {
    claim: ["Warming up. The bears are stretching.",
            "Queued. Bear one is already skeptical."],
    footprint: ["The bears are arguing about your booking flow.",
                "Bear two read your careers page and has opinions.",
                "Reading your actual pages. No guessing allowed in this rink."],
    industry: ["Off to see what your industry has already shipped.",
               "Bear one wants a source. Bear one always wants a source.",
               "They are hunting the published failures too. Those carry more signal."],
    feasibility: ["Bear one says rules first. Bear two wants an agent.",
                  "Somebody said the words voice agent and it got heated.",
                  "Bear one is checking whether a spreadsheet already does this."],
    assemble: ["They are laying the pockets out in order.",
               "Bear two is still lobbying for the chatbot."],
    critic: ["The honesty gate is trying to kill our own findings.",
             "Anything without a source is getting cut right now.",
             "Bear two wanted to add a chatbot. It did not survive review."],
    render: ["Writing your page. Nearly there.",
             "Setting the type. The bears are shaking hands."]
  };
  var SPARE = ["Real research takes real minutes. The bears are the entertainment.",
               "Still reading. Still refusing to make anything up.",
               "The bears agree on one thing, most of this is not an AI problem."];

  // The three calls the scan can make. No outcome is promised anywhere here.
  var CALLS = [
    "AI earns its place on this pocket. The scan names the lowest rung that clears the "
      + "bar and the human check that stays on it.",
    "A scale, a barcode, a plain rule, or software you already pay for does this better. "
      + "The scan says so, and it does not sell you a model.",
    "AI should not go near this one. Low volume, safety critical, or the data does not "
      + "exist. Naming these is what makes the rest worth reading."
  ];

  // Reared up on the hind legs, front paw swiping. The head is ONE smooth
  // shape tapering straight into a small black nose, with two small close set
  // eyes, no separate muzzle patch and no mouth line.
  var BEAR = '<svg viewBox="0 0 120 152" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    + '<ellipse cx="32" cy="140" rx="17" ry="8" fill="#c6d5e9"/>'
    + '<ellipse cx="34" cy="114" rx="16" ry="26" fill="#cfdcee" transform="rotate(6 34 114)"/>'
    + '<ellipse cx="72" cy="96" rx="18" ry="9" fill="#c6d5e9" transform="rotate(20 72 96)"/>'
    + '<ellipse cx="60" cy="142" rx="18" ry="8" fill="#e2eaf6"/>'
    + '<ellipse cx="58" cy="116" rx="17" ry="27" fill="#e8eff9"/>'
    + '<ellipse cx="50" cy="86" rx="29" ry="34" fill="#f4f8ff"/>'
    + '<circle cx="50" cy="22" r="7.5" fill="#f4f8ff"/>'
    + '<circle cx="74" cy="17" r="7.5" fill="#f4f8ff"/>'
    + '<circle cx="50" cy="22" r="3.4" fill="#c9a9ae"/>'
    + '<circle cx="74" cy="17" r="3.4" fill="#c9a9ae"/>'
    + '<path fill="#f4f8ff" d="M40,44 C40,26 52,16 68,16 C82,16 94,22 99,32 '
    + 'C102,37 103,41 103,44 C103,49 100,52 94,54 C82,58 62,64 50,58 C42,54 40,50 40,44 Z"/>'
    + '<ellipse cx="99" cy="45" rx="4.6" ry="3.8" fill="#141c28"/>'
    + '<ellipse cx="97.8" cy="43.8" rx="1.3" ry="0.9" fill="#59647a"/>'
    + '<circle cx="66" cy="32" r="3" fill="#141c28"/>'
    + '<circle cx="80" cy="35" r="2.7" fill="#141c28"/>'
    + '<ellipse cx="86" cy="80" rx="20" ry="10" fill="#e8eff9" stroke="rgba(2,6,15,.2)" '
    + 'stroke-width="1.4" transform="rotate(-28 86 80)"/>'
    + '<circle cx="103" cy="69" r="6.5" fill="#d7e2f2" stroke="rgba(2,6,15,.2)" stroke-width="1.4"/>'
    + '</svg>';

  var CIRC = 263.9; // 2 * pi * r, r = 42
  var quipI = 0, callI = 0, quipT = null, callT = null, clockT = null, modalT = null;
  // The poll's own handle, so a hidden tab can stand the loop down and a
  // returning one can pick it straight back up.
  var pollT = null, pollDue = false;
  var lastPhase = "claim", modalUp = false;
  // How many notes the terminal has rendered, and the identity of the last one.
  // Together they answer "did this feed simply grow" in two comparisons, which
  // is what lets a new note be appended instead of the whole terminal rebuilt.
  var feedCount = 0, feedTail = null;
  // The run is over, one way or another. Nothing may paint, poll or pop after
  // this flips, which is what keeps the email modal off a finished report.
  var settled = false;
  // The most notes we have painted. progress is append only, so a reply
  // carrying fewer is a bad read, never news.
  var seen = 0, feedNotes = [];

  function store(k){ try { return localStorage.getItem(k) === "1"; } catch(e){ return false; } }
  function mark(k){ try { localStorage.setItem(k, "1"); } catch(e){} }
  // The decorative loop on its own. A backgrounded tab stops these and a tab
  // coming back restarts them, which must NOT touch the email timer: cancelling
  // that on every hide would mean anyone who glanced away in the first 45
  // seconds never got offered the email at all.
  function stopDecor(){
    clearInterval(quipT); clearInterval(callT); clearInterval(clockT);
  }
  // Every timer the page owns, including the two setTimeouts. An earlier
  // version listed only the intervals, so the 45s email modal survived the
  // teardown and dropped itself over finished reports.
  function stopTimers(){
    stopDecor(); clearTimeout(modalT); clearTimeout(pollT);
  }
  // The modal lives on document.body, so replacing the app does not remove it.
  // Every ending has to sweep it, or a modal opened a minute earlier sits on
  // top of the report or the error asking for an email.
  function dropModal(){
    var s = document.querySelectorAll(".sw-scrim");
    for (var k = 0; k < s.length; k++) {
      if (s[k].parentNode) { s[k].parentNode.removeChild(s[k]); }
    }
  }
  function hideHero(){
    var h = document.getElementById("scanhero");
    if (h) { h.style.display = "none"; }
  }

  function currentPhase(notes){
    var best = -1;
    for (var i = 0; i < notes.length; i++) {
      var j = PHASES.indexOf(notes[i] && notes[i].phase);
      if (j > best) { best = j; }
    }
    return best < 0 ? "claim" : PHASES[best];
  }

  // Creep a little inside a phase so a long step never looks frozen, but never
  // past the next phase's floor. The number on the ring stays honest.
  function pctFor(phase, mins){
    var base = PHASE_PCT[phase], next = PHASES[PHASES.indexOf(phase) + 1];
    if (base === undefined) { base = 6; }
    var ceil = next && PHASE_PCT[next] !== undefined ? PHASE_PCT[next] : 100;
    var creep = Math.min(ceil - base - 1, Math.max(0, mins - 1) * 1.2);
    return Math.min(100, Math.round(base + Math.max(0, creep)));
  }

  function cycleQuip(now){
    var q = document.getElementById("sw-quip");
    if (!q) { return; }
    var pool = (QUIPS[lastPhase] || []).concat(SPARE);
    var next = pool[quipI % pool.length];
    quipI++;
    if (now) { q.textContent = next; return; }
    q.style.opacity = 0;
    setTimeout(function(){ q.textContent = next; q.style.opacity = 1; }, 380);
  }

  function cycleCall(now){
    var line = document.getElementById("sw-line");
    if (!line) { return; }
    var i = callI % 3;
    for (var k = 0; k < 3; k++) {
      var c = document.getElementById("sw-chip" + k);
      if (c) { c.className = "sw-chip" + (k === i ? " lit" : ""); }
    }
    callI++;
    if (now) { line.textContent = CALLS[i]; return; }
    line.style.opacity = 0;
    setTimeout(function(){ line.textContent = CALLS[i]; line.style.opacity = 1; }, 380);
  }

  function shell(){
    hideHero();
    var flakes = "", i;
    for (i = 0; i < 16; i++) {
      flakes += '<div class="sw-flake" style="left:' + ((i * 6.3 + 3) % 97) +
        '%;animation-duration:' + (6 + (i % 5) * 2.2) + 's;animation-delay:-' +
        ((i % 7) * 1.3) + 's"></div>';
    }
    var roster = "";
    for (i = 0; i < AGENTS.length; i++) {
      roster += '<div class="sw-agent" id="sw-ag-' + AGENTS[i].k + '">' +
        '<span class="tick">DONE</span><span class="dot"></span>' +
        '<span class="nm">' + esc(AGENTS[i].n) + '</span>' +
        '<span class="role">' + esc(AGENTS[i].r) + '</span></div>';
    }
    app.innerHTML =
      '<div class="sw-head">' +
        '<div class="sw-ring" id="sw-ring">' +
          '<svg viewBox="0 0 96 96" aria-hidden="true"><defs>' +
          '<linearGradient id="swgrad" x1="0" y1="0" x2="1" y2="1">' +
          '<stop offset="0%" stop-color="#ffc72c"/><stop offset="100%" stop-color="#5ac8f0"/>' +
          '</linearGradient></defs>' +
          '<circle class="trk" cx="48" cy="48" r="42" fill="none" stroke-width="7"/>' +
          '<circle class="bar" id="sw-bar" cx="48" cy="48" r="42" fill="none" stroke-width="7" ' +
          'stroke-dasharray="' + CIRC + '" stroke-dashoffset="' + CIRC + '"/></svg>' +
          '<b id="sw-pct">0%</b>' +
        '</div>' +
        '<div class="sw-headtx"><h1 class="sw-h1">Deep scan running</h1>' +
        '<p>Four specialist agents are on this one. They read your own public pages, hunt ' +
        'published results in your industry anywhere in the world, ladder every pocket to its ' +
        'lowest honest rung, then try to kill anything they cannot source.</p>' +
        '<div class="sw-clock" id="sw-clock"></div></div>' +
      '</div>' +
      '<p class="sw-lab">THE CREW ON YOUR SCAN</p>' +
      '<div class="sw-roster">' + roster + '</div>' +
      '<div class="sw-rink">' +
        // Two svg elements rather than one carrying two paths, because the
        // wave animation lives on the svg BOX now instead of on the path.
        // Animating transform on an SVG path forces a full layout every frame:
        // measured at 1200 layouts a minute sitting still, and moving the same
        // animation up to the svg element takes that to 81. Each svg carries
        // its own gradient so neither depends on an id defined in the other.
        '<div class="sw-aurs">' +
        '<svg class="sw-aur a" viewBox="0 0 400 200" preserveAspectRatio="none" aria-hidden="true">' +
        '<defs><linearGradient id="swau1" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="#3ce6b4" stop-opacity=".42"/>' +
        '<stop offset="100%" stop-color="#3ce6b4" stop-opacity="0"/></linearGradient></defs>' +
        '<path fill="url(#swau1)" d="M0,12 C70,52 130,-14 200,22 C270,58 330,4 400,34 ' +
        'L400,132 L0,132 Z"/></svg>' +
        '<svg class="sw-aur b" viewBox="0 0 400 200" preserveAspectRatio="none" aria-hidden="true">' +
        '<defs><linearGradient id="swau2" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="#5ac8f0" stop-opacity=".32"/>' +
        '<stop offset="100%" stop-color="#5ac8f0" stop-opacity="0"/></linearGradient></defs>' +
        '<path fill="url(#swau2)" d="M0,40 C80,4 150,66 220,34 C290,2 350,54 400,26 ' +
        'L400,150 L0,150 Z"/></svg></div>' +
        flakes +
        '<div class="sw-ice"></div>' +
        '<div class="sw-round" id="sw-round"></div>' +
        '<div class="sw-bear l">' + BEAR + '</div>' +
        '<div class="sw-bear r">' + BEAR + '</div>' +
        '<div class="sw-hit">WHUMP</div>' +
      '</div>' +
      '<p class="sw-quip" id="sw-quip"></p>' +
      '<div class="sw-stats">' +
        '<div class="sw-stat"><b id="sw-pages">0</b><span>YOUR PAGES READ</span></div>' +
        '<div class="sw-stat"><b id="sw-ind">0</b><span>INDUSTRY CHECKS</span></div>' +
        '<div class="sw-stat"><b id="sw-gate">0</b><span>HONESTY GATE ROUNDS</span></div>' +
      '</div>' +
      '<div class="sw-calls"><p class="sw-lab">THE THREE CALLS IT CAN MAKE</p>' +
        '<div class="sw-chips">' +
        '<span class="sw-chip" id="sw-chip0" style="--c:#3ce6b4">AI WOULD HELP HERE</span>' +
        '<span class="sw-chip" id="sw-chip1" style="--c:#5ac8f0">A RULE LIKELY WINS FIRST</span>' +
        '<span class="sw-chip" id="sw-chip2" style="--c:#8da2be">NOT AN AI JOB</span>' +
        '</div><p class="sw-line" id="sw-line"></p></div>' +
      '<div class="sw-term"><p class="sw-lab">LIVE FEED</p><div id="sw-feed"></div></div>' +
      '<p class="fineprint">Real research takes 15 to 30 minutes. Keep this tab open, or ' +
      'bookmark this link and come back to it. It stays at this address.</p>';

    cycleQuip(true);
    cycleCall(true);
    startTimers();
  }

  // The quips, the bear calls and the clock. Split out from shell() so a tab
  // coming back into view can restart exactly these without rebuilding the room.
  function startTimers(){
    stopDecor();
    if (settled || document.hidden) { return; }
    quipT = setInterval(function(){ cycleQuip(false); }, 7000);
    callT = setInterval(function(){ cycleCall(false); }, 4600);
    clockT = setInterval(tickClock, 20000);
  }

  function put(id, v){ var e = document.getElementById(id); if (e) { e.textContent = v; } }

  // Only the things that move because time passed. The 20s tick used to call
  // paint(), which recounted the whole feed and re-derived the terminal in
  // order to advance a minute counter. Everything else on this screen changes
  // when the FEED changes, which is what the poll already handles.
  function tickClock(){
    var mins = Math.max(0, Math.round((Date.now() - startedAt) / 60000));
    var pct = pctFor(lastPhase, mins);
    var bar = document.getElementById("sw-bar");
    if (bar) { bar.setAttribute("stroke-dashoffset", String(CIRC * (1 - pct / 100))); }
    put("sw-pct", pct + "%");
    // the site's own sky brightens as the run advances
    document.body.style.setProperty("--skyglow", String(0.5 + 0.5 * (pct / 100)));
    put("sw-clock", (mins < 1 ? "just started" : "watching for " + mins + " min") +
      ", usually 15 to 30");
  }

  function paint(progress){
    // Normalize once, here, and nowhere else. progress is a raw jsonb column
    // written by hand-composed SQL, so it can arrive as a non-array or carry a
    // null element. Everything downstream then works on a plain array of real
    // objects and cannot throw, which matters because a throw inside paint
    // used to kill the poll loop for the life of the tab.
    var notes = [], i;
    if (progress && Object.prototype.toString.call(progress) === "[object Array]") {
      for (i = 0; i < progress.length; i++) {
        if (progress[i]) { notes.push(progress[i]); }
      }
    }
    var phase = currentPhase(notes);
    if (phase !== lastPhase) {
      lastPhase = phase;
      quipI = 0;
      cycleQuip(false);
      var ring = document.getElementById("sw-ring");
      if (ring) {
        ring.classList.add("beat");
        setTimeout(function(){ ring.classList.remove("beat"); }, 1400);
      }
    }

    // Every count below is read straight off the feed the routine wrote.
    // Nothing here is decoration and nothing here is inflated.
    //
    // Counters read the note's kind when the routine set one, and fall back to
    // the old phase shape for rows written before kind existed. Counting kind
    // is what keeps these true once the feed runs dense: a critic round that
    // emits ten notes is still one round.
    // The fallback is decided PER NOTE, never once for the whole feed. A
    // single flag was wrong: one kinded note flipped it for everything, so
    // every kind-less note fell out of the totals at once and a tile could
    // drop from 14 to 0 mid run while its 14 lines sat in the feed below.
    //
    // sync:counters begin
    // scripts/scanner_sync_check.py cuts this block out and RUNS it against
    // probe feeds, so keep it self contained: read only `notes`, declare
    // everything else, and leave nPages, nInd and nGate holding the three tile
    // values. Rename any of that and the check tells you which one it lost.
    var nPages = 0, nInd = 0, nGate = 0;
    for (var ci = 0; ci < notes.length; ci++) {
      var kd = notes[ci].kind;
      if (kd) {
        if (kd === "page")        { nPages++; }
        else if (kd === "search") { nInd++; }
        else if (kd === "round")  { nGate++; }
      } else {
        var ph = notes[ci].phase, nt = notes[ci].note || "";
        if (ph === "footprint" && /^reading /i.test(nt)) { nPages++; }
        else if (ph === "industry") { nInd++; }
        else if (ph === "critic")   { nGate++; }
      }
    }
    // sync:counters end
    put("sw-pages", nPages); put("sw-ind", nInd); put("sw-gate", nGate);

    tickClock();
    var round = document.getElementById("sw-round");
    if (round) {
      round.innerHTML = "ROUND " + (PHASES.indexOf(phase) + 1) + " &middot; " +
        esc(phase.toUpperCase());
    }

    var at = PHASES.indexOf(phase);
    for (i = 0; i < AGENTS.length; i++) {
      var el = document.getElementById("sw-ag-" + AGENTS[i].k);
      if (!el) { continue; }
      var last = -1, working = false, j;
      for (j = 0; j < AGENTS[i].on.length; j++) {
        var idx = PHASES.indexOf(AGENTS[i].on[j]);
        if (idx > last) { last = idx; }
        if (AGENTS[i].on[j] === phase) { working = true; }
      }
      el.className = "sw-agent" + (working ? " on" : (last < at ? " did" : ""));
    }

    // The terminal is append only, so it is built append only. Rewriting
    // innerHTML restarted the swin slide on all nine rows for every note,
    // which under the dense feed meant the whole terminal flashed 60 to 120
    // times a run instead of one line arriving at a time. Rows already on
    // screen are left alone now and only genuinely new ones animate.
    //
    // The change test is two comparisons rather than a signature built over
    // every note, which was a 6 KB string concatenated on every poll and every
    // clock tick just to answer a yes or no question.
    var box = document.getElementById("sw-feed");
    if (box) {
      var tail = notes.length ? key(notes[notes.length - 1]) : "";
      // feedTail starts null, never "", so the very first paint of an empty
      // feed still renders the queued placeholder instead of an empty box.
      if (notes.length !== feedCount || tail !== feedTail) {
        // Grew from what is on screen, rather than changed underneath it.
        var grew = feedCount > 0 && notes.length > feedCount &&
                   notes[feedCount - 1] && key(notes[feedCount - 1]) === feedTail;
        if (grew) {
          for (i = Math.max(feedCount, notes.length - 9); i < notes.length; i++) {
            box.insertAdjacentHTML("beforeend", row(notes[i]));
          }
          while (box.children.length > 9) { box.removeChild(box.firstChild); }
        } else {
          var feed = "";
          for (i = Math.max(0, notes.length - 9); i < notes.length; i++) { feed += row(notes[i]); }
          box.innerHTML = feed || ('<div class="sw-ln"><span class="sw-t">now</span>' +
            '<span class="sw-x">queued, an agent is picking this up</span></div>');
        }
        feedCount = notes.length;
        feedTail = tail;
      }
    }
  }

  function key(n){ return n.at + "|" + n.note; }
  function row(n){
    return '<div class="sw-ln"><span class="sw-t">' + esc(n.at) +
      '</span><span class="sw-x">' + esc(n.note) + '</span></div>';
  }

  // --------------------- the leave-your-email moment ---------------------
  function emailModal(){
    // settled is the guard that matters. Offering to email someone their link
    // when the scan is already on their screen, or has already failed, reads
    // as the page not knowing what it just did.
    if (settled || modalUp || !token || store("swnotify." + token)) { return; }
    modalUp = true;
    var scrim = document.createElement("div");
    scrim.className = "sw-scrim";
    scrim.innerHTML = '<div class="sw-modal" role="dialog" aria-modal="true" ' +
      'aria-labelledby="sw-mh"><h3 id="sw-mh">This takes 15 to 30 minutes</h3>' +
      '<p>Real research is slow, and we would rather be slow than make something up. ' +
      'Leave your email and we will send your link the moment the scan finishes. ' +
      'One email, no list, no pitch.</p>' +
      '<div class="sw-row"><input id="sw-email" type="email" ' +
      'placeholder="you@yourbusiness.com" autocomplete="email">' +
      '<button class="cta gold" id="sw-send" type="button">SEND IT TO ME</button></div>' +
      '<p class="sw-err" id="sw-merr"></p>' +
      '<div class="sw-skip"><a id="sw-later">NO THANKS, I WILL WAIT HERE</a></div></div>';
    document.body.appendChild(scrim);

    // Dismissing is dismissing, however they do it. Only the NO THANKS link
    // used to be remembered, so Escape or a click on the backdrop brought the
    // same modal back 45 seconds into every later visit to the link. The
    // keydown listener comes off with it, so a closed modal stops holding a
    // detached subtree and its fetch closure alive.
    function onKey(e){ if (e.key === "Escape") { close(); } }
    function close(){
      mark("swnotify." + token);
      document.removeEventListener("keydown", onKey);
      if (scrim.parentNode) { scrim.parentNode.removeChild(scrim); }
    }
    scrim.querySelector("#sw-later").addEventListener("click", close);
    scrim.addEventListener("click", function(e){ if (e.target === scrim) { close(); } });
    document.addEventListener("keydown", onKey);
    var input = scrim.querySelector("#sw-email");
    if (input) { input.focus(); }

    scrim.querySelector("#sw-send").addEventListener("click", function(){
      var err = scrim.querySelector("#sw-merr"), btn = scrim.querySelector("#sw-send");
      var email = (input.value || "").trim();
      if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        err.textContent = "that email does not look right"; return;
      }
      err.textContent = ""; btn.disabled = true; btn.textContent = "SAVING...";
      fetch(FN + "/scan-notify-me", { method: "POST", headers: HEADERS,
        body: JSON.stringify({ token: token, email: email }) })
        .then(function(r){ return r.json().then(function(d){ return { ok: r.ok, d: d }; }); })
        .then(function(x){
          if (!x.ok) { throw new Error(x.d.error || "could not save that"); }
          mark("swnotify." + token);
          var msg = x.d.already_done
            ? "Your scan is already finished, so it is loading on this page right now."
            : (x.d.already_set
                ? "An email is already attached to this scan, so the link is going there."
                : "We will email your link to " + esc(email) +
                  " the moment the scan finishes. You can close this tab.");
          scrim.querySelector(".sw-modal").innerHTML = '<h3>Saved</h3><p class="ok">' + msg +
            '</p><div class="sw-skip"><a id="sw-back">BACK TO THE BEARS</a></div>';
          scrim.querySelector("#sw-back").addEventListener("click", close);
        })
        .catch(function(ex){
          err.textContent = ex.message; btn.disabled = false; btn.textContent = "SEND IT TO ME";
        });
    });
  }

  function fail(head, msg){
    settled = true;
    stopTimers();
    dropModal();
    hideHero();
    app.innerHTML = '<div class="sw-head" style="margin-top:6vh"><div class="sw-headtx">' +
      '<h1 class="sw-h1">' + head + '</h1><p>' + msg + '</p>' +
      '<p class="fineprint"><a href="./">RUN IT AGAIN</a></p></div></div>';
  }

  function poll(){
    shell();
    paint([]);
    // Give them a beat to watch the bears before asking for anything. The
    // handle goes in modalT so stopTimers() can cancel it on every ending.
    modalT = setTimeout(emailModal, 45000);
    // A slow scan is never given up on. The page keeps the feed alive at a
    // steady 5s for as long as the run takes, because a long run is still a
    // running run. A self scheduling timeout rather than setInterval, so a
    // slow response can never stack requests on top of each other.
    //
    // The ONE stop is a two hour safety net, for a run that wedges without
    // ever reporting done or failed. Nothing else ends the loop, and two
    // hours is four times the top of a real run, so a scan that is merely
    // slow will never see it. It also bounds a forgotten tab.
    var started = Date.now(), STOP_AFTER = 7200000;
    // scan-result names three errors. Two of them never fix themselves, so
    // asking again for two hours only fabricates a waiting room for a scan
    // that is not running. "lookup failed" is the read breaking rather than
    // the scan, which can pass, so it is tolerated for two minutes first.
    var DEAD = { "not found": 1, "bad token": 1 }, readFails = 0;
    // A tab nobody is looking at is asked to stand down rather than keep
    // pulling the whole feed every five seconds. Two hours in a background tab
    // was 1440 requests and about 8 MB fetched for a screen nobody could see.
    // Coming back polls at once, so the room is current the moment it is
    // looked at rather than up to five seconds stale.
    function next(){
      clearTimeout(pollT);
      if (settled) { return; }
      if (document.hidden) { pollDue = true; return; }
      pollT = setTimeout(tick, 5000);
    }
    document.addEventListener("visibilitychange", function(){
      if (settled) { return; }
      if (document.hidden) {
        stopDecor();
        clearTimeout(pollT);
        pollDue = true;
        return;
      }
      startTimers();
      tickClock();          // the minute counter caught up in one step
      if (pollDue) { pollDue = false; tick(); }
    });
    function tick(){
      var httpOk = true;
      // `since` says how many notes we already hold, so the reply can carry
      // only what is new. An older deployment ignores it and sends the whole
      // feed, which still works, see the reader below.
      fetch(FN + "/scan-result?token=" + encodeURIComponent(token) + "&since=" + seen,
            { headers: HEADERS })
        .then(function(r){ httpOk = r.ok; return r.json(); })
        // A rejected fetch (offline, DNS, CORS, dropped connection) never runs
        // the handler above, so httpOk kept its initial true and the empty
        // object carried no d.error. Control then fell past the failure branch
        // to readFails = 0, and a reader who had lost connectivity watched a
        // fully animated, apparently-progressing room for the whole two-hour
        // STOP_AFTER instead of the two-minute give-up this is built around.
        .catch(function(){ httpOk = false; return {}; })
        .then(function(d){
          if (d.status === "done" || d.status === "degraded") {
            settled = true;
            stopTimers();
            dropModal();
            document.body.style.setProperty("--skyglow", "1");
            var f = document.createElement("iframe");
            f.setAttribute("sandbox", "allow-forms allow-popups allow-top-navigation-by-user-activation");
            f.className = "sw-frame";
            // A finished row with no html is reachable, so say something
            // rather than hand them a blank box with no way forward.
            f.srcdoc = d.html || "<!doctype html><meta charset='utf-8'>" +
              "<body style='background:#02060f;color:#f4f8ff;font:16px/1.6 system-ui,sans-serif;" +
              "padding:40px'><p>Your scan finished but the page did not come back with it. " +
              "Reload this link and it should appear.</p>";
            app.innerHTML = "";
            app.appendChild(f);
            return;
          }
          if (d.status === "failed") {
            fail("That scan did not finish", "It happens when a site blocks reading or the " +
                 "footprint is unreachable.");
            return;
          }
          if (d.error && DEAD[d.error]) {
            if (d.error === "bad token") {
              fail("That link is not a scan we have",
                   "The token in this address is not one we issued, so there is nothing here "
                   + "to watch. Usually it means the link got cut short on its way to you.");
            } else {
              fail("That scan did not finish", "It happens when a site blocks reading or the "
                   + "footprint is unreachable.");
            }
            return;
          }
          if (d.error || !httpOk) {
            // The read is failing rather than the scan. Ride it out briefly,
            // then stop rather than animate a room we cannot see into.
            readFails++;
            if (readFails > 24) {
              fail("We cannot read your scan right now",
                   "The scan itself may well be fine. Our reader has been failing for two "
                   + "minutes, so this page will not learn anything by asking again. Open "
                   + "this link again in a few minutes.");
              return;
            }
            next();
            return;
          }
          readFails = 0;
          // The reply carries either the whole feed or only what is new since
          // the last poll, and says which by whether progress_from is there.
          // A deployment that predates the cursor sends the whole feed and no
          // progress_from, which reads here as "from 0", so both work.
          //
          // Repaint only on a reply that accounts for at least as much feed as
          // is already shown. progress is append only, so anything shorter is a
          // bad read, and painting it would flash the ring, the roster and
          // every counter back to zero. An empty array is truthy, so the check
          // this replaced let exactly that through.
          if (Object.prototype.toString.call(d.progress) === "[object Array]") {
            var from = (typeof d.progress_from === "number") ? d.progress_from : 0;
            var total = (typeof d.progress_len === "number")
              ? d.progress_len : from + d.progress.length;
            if (from === 0) {
              if (total >= seen) { seen = total; feedNotes = d.progress; paint(feedNotes); }
            } else if (from === seen && total >= seen) {
              if (d.progress.length) {
                seen = total;
                feedNotes = feedNotes.concat(d.progress);
                paint(feedNotes);
              }
            } else {
              // We and the server disagree about how much we hold. Ask for the
              // whole feed next time rather than stitching a gap into the
              // terminal and reporting counts with a hole in them.
              seen = 0;
            }
          }
          if (Date.now() - started > STOP_AFTER) {
            fail("This page has been watching for two hours",
                 "That is well past the longest real scan and nothing has come back, so it "
                 + "has stopped asking. If you left an email we will still send your link "
                 + "when it lands. Otherwise open this link again to pick the watch back up.");
            return;
          }
          next();
        })
        // The last line of defence. Anything thrown above lands here, and
        // without it the loop simply stopped, with no error on screen and the
        // two hour net dead too, because the net lives inside that handler.
        .catch(function(){ next(); });
    }
    next();
  }

  function wire(){
    if (pre) { document.getElementById("f-url").value = pre; }
    if (TS_SITEKEY) {
      document.getElementById("ts-slot").innerHTML =
        '<div class="cf-turnstile" data-sitekey="' + esc(TS_SITEKEY) + '" data-theme="dark"></div>';
      var s = document.createElement("script");
      s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
      s.async = true; s.defer = true;
      document.head.appendChild(s);
    }
    document.getElementById("scanform").addEventListener("submit", function(e){
      e.preventDefault();
      var btn = document.getElementById("f-go"), err = document.getElementById("f-err");
      var tsToken = (TS_SITEKEY && window.turnstile) ? (turnstile.getResponse() || "") : "";
      if (TS_SITEKEY && !tsToken) { err.textContent = "finish the human check above first"; return; }
      err.textContent = ""; btn.disabled = true; btn.textContent = "STARTING...";
      var early = document.getElementById("f-notify").value || null;
      fetch(FN + "/scan-request", { method: "POST", headers: HEADERS, body: JSON.stringify({
        url: document.getElementById("f-url").value,
        booking_url: document.getElementById("f-booking").value || null,
        jobs: document.getElementById("f-jobs").value || null,
        notify_email: early,
        turnstile_token: tsToken || null
      })}).then(function(r){ return r.json().then(function(d){ return { ok: r.ok, d: d }; }); })
      .then(function(x){
        if (!x.ok) { throw new Error(x.d.error || "could not start the scan"); }
        // They already left an address, so never nag them for it on the wait screen.
        if (early) { mark("swnotify." + x.d.token); }
        location.search = "?token=" + encodeURIComponent(x.d.token);
      }).catch(function(ex){
        err.textContent = ex.message;
        btn.disabled = false; btn.textContent = "SCAN MY BUSINESS";
        if (TS_SITEKEY && window.turnstile) { turnstile.reset(); }
      });
    });
  }

  if (token) { poll(); } else { wire(); }
})();
</script>"""
    ld = {"@context": "https://schema.org", "@graph": [
        org_ld(site_url),
        breadcrumb_ld(site_url, [("Alaska AI", ""), ("Scanner", "scan/")])]}
    return page("The Bottleneck Scanner - Alaska AI",
                "Drop your website and get an honest map of where AI would help your "
                "Alaska business, where a plain rule wins first, and where AI should "
                "not go at all. Free, no signup to see it.",
                body, "../", "scanner", today, site_url, "scan/", ld=ld)


def about_page(today, site_url):
    body = f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<h1>Built in the <em>North</em></h1>
<p class="tag">Alaska AI is a daily publication and an AI studio focused on Alaska.
One team, two jobs.</p>
</div>
<div class="prose" data-reveal>
<h2>What Alaska AI is</h2>
<p>Alaska AI is a daily publication about the biggest technology shift of our
lifetimes, told from the only place we would tell it from. AI is arriving in
Alaska the way pipelines and railroads once did, as land leases, gas
contracts, utility votes and federal solicitations. Alaskans deserve to see
it coming, in plain English, with receipts.</p>
<p>Alaska AI is also a working AI studio. It builds agentic systems that run
whole workflows end to end, along with digital employees, paperwork engines,
assistants trained on a company's own files, and voice agents. All of it for
Alaska businesses, statewide. That work lives on the
<a href="../services/">services page</a>. Writing the beat every morning is
exactly why the studio knows what actually pays.</p>
<h2>Who runs it</h2>
<p>Alaska AI is founded and run by <a href="https://www.linkedin.com/in/talonsturgill">Talon
Sturgill</a>, born and raised in Anchorage. He is also the lead AI engineer for a large
Lower 48 lab serving enterprise clients, work he does remotely. Alaska AI brings that
expertise home to help Alaska businesses that rarely get access to it.</p>
<h2>How the work gets verified</h2>
<p>Every day Alaska AI works {count_word(len(TOPICS))} beats across the state, from power and
compute to policy and money to what Alaskans are actually saying. Every
number and quote is re-fetched from a primary source before it can appear
on a slide, the docket, or this site, and each one carries its own claim
record. Every deck's artwork is drawn fresh from code for its story. The
same team maintains <a href="../docket/">the Alaska AI Docket</a>, a public
tracker of every AI infrastructure decision in the state and whether the
public gets a say in it, published as open data.</p>
<h2>The rules we work by</h2>
<p>The publication runs on receipts. The studio runs on four commitments,
written down here so clients can hold us to them.</p>
<p><strong>Your outcome outranks our invoice.</strong> The recommendation you
get is what we would do in your seat with our own money. Sometimes that is a
smaller build than you asked about, sometimes it is a hard call you have been
putting off, and sometimes it is the honest no, that AI does not pay in your
business yet. You get the same answer either way.</p>
<p><strong>Plain talk, both directions.</strong> Bad news arrives early and in
plain words. No soft versions, no jargon fog, no risk buried in an appendix.
We ask for the same back, a client who tells us straight gets problems fixed
while they are still small.</p>
<p><strong>We guard the build, even from the brief.</strong> Most AI projects
die of enthusiasm, the wrong first system, built too big, on data that was not
ready. We watch that happen across an industry every morning, so we know where
the road washes out before you can see it from inside your own operation. When
the exciting ask and the right build disagree, we say so and steer. That
judgment is most of what you are paying for.</p>
<p><strong>You will not chase us.</strong> A note to this desk gets a reply
within a business day and usually much sooner, a human reads everything and
the machines are on shift around the clock. Speed is respect, and we expect it
back. Slow answers stall more builds than hard problems do.</p>
<h2>Where to find us</h2>
<p>The decks ship daily on
<a href="https://www.linkedin.com/company/alaska-ai/">LinkedIn</a> and
<a href="https://www.tiktok.com/@alaskaai_">TikTok</a> under Alaska AI.
The docket and the articles live here. For the studio, start with
<a href="../services/">services</a> or write to docket@alaskaaihq.com.</p>
</div>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "url": f"{site_url}/about/",
         "name": "About Alaska AI",
         "about": {"@id": org_id(site_url)}},
        org_ld(site_url),
        {"@type": "Person", "@id": f"{site_url}/about/#talon",
         "name": "Talon Sturgill", "jobTitle": "Lead AI Engineer",
         "worksFor": {"@id": org_id(site_url)},
         "url": f"{site_url}/about/",
         "birthPlace": {"@type": "Place", "name": "Anchorage, Alaska"},
         "sameAs": ["https://www.linkedin.com/in/talonsturgill"]}]}
    return page("About Alaska AI - An AI Studio and Daily AI Publication in Anchorage",
                "Alaska AI is a daily publication on Alaska's AI beat and an AI studio "
                "in Anchorage, founded by Talon Sturgill. Every fact verified to its "
                "source.",
                body, "../", "about", today, site_url, "about/", ld=ld,
                crumbs=[("Alaska AI", ""), ("About", "about/")])


def not_found_page(today, site_url):
    body = """<div class="hero" style="min-height:56vh;padding-top:12vh">
<div class="chip kind">404</div>
<h1 style="margin-top:14px">Off the <em>trail</em></h1>
<p class="tag">This page does not exist, or it moved when the ice went out.
The stars will get you home.</p>
<div class="ctarow">
  <a class="cta gold" href="/">BACK HOME</a>
  <a class="cta ghost" href="/docket/">DOCKET</a>
  <a class="cta ghost" href="/archive/">ARTICLES</a>
</div>
</div>"""
    return page("Page not found - Alaska AI",
                "That page does not exist. The stars will get you home.",
                body, "/", "none", today, site_url, "404.html", noindex=True)


def touch_icon(out):
    """The logo tile at 180px for phone home screens: the gold Alaska
    silhouette (true geodata) on the night, with a soft glow."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    s = 180
    im = Image.new("RGB", (s, s), (2, 6, 15))
    dr = ImageDraw.Draw(im)
    paths = db.alaska_paths(max_points=1400, keep_rings=6)
    T = db.fit_transform(paths, s, s, 16)
    rings = [[T(p) for p in path] for path in paths]
    cx = cy = s / 2
    for gr, col in ((1.10, (80, 62, 10)), (1.045, (166, 130, 26)), (1.0, (255, 199, 44))):
        for pts in rings:
            glow = [(cx + (x - cx) * gr, cy + (y - cy) * gr) for x, y in pts]
            if len(glow) >= 3:
                dr.polygon(glow, fill=col)
    im.save(out / "apple-touch-icon.png", optimize=True)


def sitemap(site_url, runs, today, decisions=None):
    """Truthful lastmod only: home, videos, docket, and archive genuinely
    change every build (new deck, new dispatch video, docket updates), deck
    pages carry their publish date, and services/about omit lastmod rather
    than fake a daily bump. Google ignores priority and changefreq, so
    neither is emitted."""
    iso = today.isoformat()
    entries = []
    # Beats and the source archive change whenever a deck lands on them, which
    # is every build that ships an article, so they carry a real lastmod too.
    fresh = ("", "videos/", "docket/", "gas-watch/", "archive/", "topics/", "sources/")
    for u in fresh + ("services/", "scan/", "about/"):
        lm = f"<lastmod>{iso}</lastmod>" if u in fresh else ""
        entries.append(f"<url><loc>{site_url}/{u}</loc>{lm}</url>")
    for t in TOPICS:
        entries.append(f"<url><loc>{site_url}/topics/{t['slug']}/</loc>"
                       f"<lastmod>{iso}</lastmod></url>")
    for r in runs:
        entries.append(f"<url><loc>{site_url}/archive/{r['date']}/</loc>"
                       f"<lastmod>{r['date']}</lastmod></url>")
    # Each tracked decision carries its OWN last_updated, which is the date the
    # routine last re-verified it against a source. That is a truthful lastmod
    # per URL rather than a build-date bump across the whole docket.
    for it in (decisions or []):
        entries.append(f"<url><loc>{site_url}/docket/{it['id']}/</loc>"
                       f"<lastmod>{it['last_updated']}</lastmod></url>")
    for u in ("data/", "questions/", "privacy/"):
        entries.append(f"<url><loc>{site_url}/{u}</loc><lastmod>{iso}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(entries) + "</urlset>")



GAS_WATCH_META = {
    "license": DATA_LICENSE,
    "license_label": DATA_LICENSE_LABEL,
    "attribution": "Alaska AI, https://alaskaaihq.com",
    "publisher": "Alaska AI",
    "spatial_coverage": "Southcentral Alaska, United States",
    "docket_item_id": "enstar-cook-inlet-gas-storage",
}


GAS_WATCH_FIELD_DOCS = {
    "date": "The CINGSA nomination day the record describes, ISO 8601.",
    "cingsa.inventory_mcf": "Measured working gas in Cook Inlet storage at end of day, thousand cubic feet.",
    "cingsa.inventory_pct_of_design": "Measured inventory as a percent of the field's design volume.",
    "cingsa.withdrawal_operating_mcfd": "Measured maximum daily withdrawal the field can deliver, thousand cubic feet per day.",
    "cingsa.inventory_delta_mcf": "Measured change in inventory across the day. Negative is a withdrawal.",
    "forecast": "Per day Anchorage forecast, mean temperature, heating degree days and modeled demand.",
    "derived.peak_modeled_demand_mmcfd": "Highest modeled regional demand in the forecast window, million cubic feet per day. Model output, not a measurement.",
    "reconciliation.non_cingsa_supply_mmcfd": "Derived daily gas supply from everything that is not CINGSA storage, obtained from the mass balance. Field production plus any Hilcorp storage movement combined. Published nowhere else.",
    "reconciliation.error": "Forecast heating degree days minus observed, the model's own daily accuracy check.",
    "model": "The demand coefficients that produced this record, carried per record so an old number stays reproducible.",
    "sources": "Provenance for every external fetch, with url, timestamp, http status and attempt count.",
    "verified": "False when a fetch failed or the source was stale. An unverified record carries no number forward from the day before.",
}


def gas_watch_ld(today, site_url, series, model, figs):
    """Dataset structured data for the gas watch.

    Without this the page is HTML that happens to link a JSON file. With it,
    Google Dataset Search, A11y and citation tools, and any model reading the
    page can tell what a row holds, how often it updates, what it may be reused
    for, and which fields are measured against which are modeled. That last
    distinction is the whole point of the dataset, so it belongs in the machine
    readable layer and not only in the prose.

    variableMeasured is where a scraper learns that non_cingsa_supply is
    derived and published nowhere else, which is the reason to cite us."""
    latest = gw.latest_verified(series)
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": f"{site_url}/gas-watch/#dataset",
        "name": "Cook Inlet Gas Watch",
        "alternateName": ["Southcentral Alaska natural gas storage tracker",
                          "Cook Inlet gas storage daily record"],
        "description": (
            "A daily numeric record of Southcentral Alaska's natural gas position. "
            "Measured Cook Inlet storage inventory and deliverability from the CINGSA "
            "public dashboard, modeled regional demand from Anchorage heating degree "
            "days, and the derived non CINGSA supply that falls out of the mass "
            "balance and is published nowhere else. CINGSA keeps no archive, so this "
            "series exists only because it is collected daily. It publishes no safety "
            "verdict, no shortfall prediction and no all clear."),
        "url": f"{site_url}/gas-watch/",
        "dateModified": figs.get("as_of", today.isoformat()),
        "datePublished": figs.get("first_date", today.isoformat()),
        "creator": {"@id": org_id(site_url)},
        "publisher": {"@id": org_id(site_url)},
        "maintainer": {"@id": org_id(site_url)},
        "license": DATA_LICENSE,
        "isAccessibleForFree": True,
        "version": gw.SCHEMA_VERSION,
        "inLanguage": "en-US",
        "creativeWorkStatus": "Published",
        "accrualPeriodicity": "P1D",
        "keywords": [
            "Cook Inlet", "Southcentral Alaska", "natural gas storage", "CINGSA",
            "Alaska energy", "gas supply", "Enstar", "Anchorage", "heating degree days",
            "gas deliverability", "energy data", "open data", "Railbelt",
            "Alaska natural gas", "storage inventory", "gas shortfall", "Kenai"],
        "spatialCoverage": {
            "@type": "Place", "name": "Southcentral Alaska, United States",
            "geo": {"@type": "GeoShape", "box": "58.9 -154.0 62.5 -145.0"}},
        "temporalCoverage": (f"{series[0]['date']}/{figs.get('as_of', today.isoformat())}"
                             if series else today.isoformat()),
        # Derived from the model config, not typed. This sentence said the model
        # used "a published two point linear calibration, and is not fitted to
        # observed utility sendout" for hours after the least-squares refit
        # shipped, so the machine-readable layer contradicted the visible prose
        # two screens above it. gaswatch_build.underclaims() was written for
        # exactly that failure but only reads the config, and the routine's page
        # checker scopes to <main>, so nothing could see it. Reading the config
        # here means it cannot drift from the model again.
        "measurementTechnique": (
            "Storage inventory and deliverability are read daily from the CINGSA "
            "public dashboard and stamped with the source timestamp. Regional demand "
            "is modeled from the National Weather Service Anchorage forecast, "
            f"{model.get('fit_source', 'see the model config')}. "
            "Non CINGSA supply is derived from "
            "the mass balance, demand less measured storage withdrawal, using "
            "observed degree days one day in arrears. A failed fetch writes an "
            "explicit unverified record and carries no number forward."),
        "variableMeasured": [{"@type": "PropertyValue", "name": k, "description": v}
                             for k, v in GAS_WATCH_FIELD_DOCS.items()],
        "distribution": [
            {"@type": "DataDownload", "name": "The full series as JSON",
             "encodingFormat": "application/json",
             "contentUrl": f"{site_url}/gas-watch.json"},
        ],
        "includedInDataCatalog": {"@type": "DataCatalog", "name": "Alaska AI open data",
                                  "url": f"{site_url}/data/"},
        "isRelatedTo": {"@type": "Dataset", "@id": f"{site_url}/docket/#dataset",
                        "name": "The Alaska AI Docket",
                        "url": f"{site_url}/docket/{GAS_WATCH_META['docket_item_id']}/"},
        "citation": (f"Alaska AI, Cook Inlet Gas Watch, {site_url}/gas-watch/, "
                     f"read {figs.get('as_of', today.isoformat())}."),
        **({"distributionSize": len(series)} if series else {}),
    }


def gas_watch_page(today, site_url, series, model, figs=None):
    """Cook Inlet Gas Watch, the live instrument beside the docket.

    The docket tracks decisions on a scale of months. This tracks the physical
    system on a scale of days. Siblings, not parent and child, which is why the
    series lives in its own ledger and its own feed rather than inside
    docket.json, whose schema is decision-centric and would break.

    Every figure on this page is computed in gaswatch_build.figures() from the
    committed record. numeral_lint() below refuses to ship a number that traces
    back to nothing, so no typed or remembered figure can reach a reader."""
    body = gw.page_body(today, site_url, series, model, GAS_WATCH_META, figs=figs)
    figs = gw.figures(series, model, figs)
    planted = gw.numeral_lint(
        body, gw.allowed_numerals(figs, model,
                                  [DATA_LICENSE_LABEL, gw.SCHEMA_VERSION], series))
    if planted:
        db.fail("gas watch page carries numeral(s) no computation produced, "
                f"{sorted(set(planted))[:6]}. Every figure must come from "
                "gaswatch_build.figures().")
    desc = ("A daily numeric record of Southcentral Alaska's natural gas position. "
            "Measured Cook Inlet storage, modeled regional demand, and the derived "
            "supply nobody else publishes. No safety verdict, ever.")
    return page("Cook Inlet Gas Watch", desc, body, "../", "gas", today, site_url,
                "gas-watch/", extra_css=gw.GW_CSS, extra_js=gw.GW_JS,
                ld=gas_watch_ld(today, site_url, series, model, figs),
                crumbs=[("Home", ""), ("Gas Watch", "gas-watch/")])


def prose_colon_gate(rel, html):
    """House style bans colons in visible copy (clock times like 4:30 and
    URLs are not prose and pass). Fails the build if one slips in."""
    import re as _re
    txt = _re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", html)
    txt = _re.sub(r"<[^>]+>", "\n", txt)
    txt = _re.sub(r"https?://\S+", " ", txt)
    txt = _re.sub(r"\d{1,2}:\d{2}", " ", txt)
    for line in txt.split("\n"):
        if ":" in line:
            db.fail(f"prose colon in {rel} near {line.strip()[:70]!r}")


def build(today, out_dir, site_url=None, domain=""):
    site_url = site_url or db.DEFAULT_SITE
    docket = load_docket(today)
    runs = load_runs()
    out = REPO / out_dir

    # Feeds, Markdown mirrors and deck pages all want the same reconstructed
    # article, so build it once per run here rather than three times downstream.
    for r in runs:
        _, _, r["article_text"] = article_html(r)
        r["cover"] = f"{RAW}/runs/{r['date']}/og.jpg"

    gas_series = gw.load_series()
    gas_model = gw.gc.load_model(gw.MODEL_CONFIG)
    # Computed once here and handed to everything that needs it. The homepage
    # strip, the gas watch page, its feed and its numeral lint were each asking
    # for the same dict from the same two inputs, four full recomputations and
    # nine reparses of the 4,599 day weather record per build, on a build that
    # runs on every collector cron.
    gas_figs = gw.figures(gas_series, gas_model) if gas_model else None

    pages = {
        "index.html": home_page(today, site_url, docket, runs,
                                gas_series, gas_model, gas_figs),
        "docket/index.html": docket_page(today, site_url, docket),
        "gas-watch/index.html": gas_watch_page(today, site_url, gas_series,
                                              gas_model, gas_figs),
        "archive/index.html": archive_page(today, site_url, runs),
        "services/index.html": services_page(today, site_url),
        "services/thanks/index.html": services_thanks_page(today, site_url),
        "scan/index.html": scan_page(today, site_url),
        "about/index.html": about_page(today, site_url),
        "404.html": not_found_page(today, site_url),
    }
    # Standing beats and the source archive. Both are permanent URLs: a beat
    # page renders whether or not anything ran on it, so the link and the
    # ranking survive a quiet month instead of 404ing between stories.
    try:
        topics_ledger = json.loads((REPO / "ledger/topics.json").read_text())
    except Exception:
        topics_ledger = {}
    tindex = topic_index(runs, topics_ledger)
    docket_hits = {}
    for t in TOPICS:
        docket_hits[t["slug"]] = [
            d for d in docket[0]
            if any(term in " ".join([str(d.get("title") or ""),
                                     str(d.get("summary") or ""),
                                     str(d.get("kind") or ""),
                                     str(d.get("decider") or "")]).lower()
                   for term in t["terms"])]

    # The beat membership, inverted.
    #
    # Every article and every tracked decision belongs to at least one standing
    # beat, and until now neither said so. An article linked to the beats INDEX
    # and a decision page linked to no beat at all, so the seven pages that
    # collect a subject had nothing pointing at them from the pages that are the
    # subject. Inverting the two maps that already exist costs nothing and turns
    # a flat pile of pages into a cluster that reads as being about something.
    beats_for_run, beats_for_item = {}, {}
    for t in TOPICS:
        for r in tindex.get(t["slug"]) or []:
            beats_for_run.setdefault(r["date"], []).append(t)
        for d in docket_hits[t["slug"]]:
            beats_for_item.setdefault(d["id"], []).append(t)

    for r in runs:
        pages[f"archive/{r['date']}/index.html"] = deck_page(
            today, site_url, r, beats_for_run.get(r["date"]) or [])

    pages["topics/index.html"] = topics_index_page(today, site_url, tindex)
    for t in TOPICS:
        pages[f"topics/{t['slug']}/index.html"] = topic_page(
            today, site_url, t, tindex.get(t["slug"]) or [], docket_hits[t["slug"]][:8])
    pages["sources/index.html"] = sources_page(today, site_url, runs)
    # One canonical page per tracked decision, so an answer engine citing a
    # specific decision has a URL, a title and a lastmod for THAT decision
    # rather than an anchor on a shared page.
    pages["data/index.html"] = data_page(today, site_url, docket, runs,
                                        gas_series, gas_model)
    pages["questions/index.html"] = questions_page(today, site_url, docket)
    pages["privacy/index.html"] = privacy_page(today, site_url)
    for _it in docket[0]:
        pages[f"docket/{_it['id']}/index.html"] = decision_page(
            today, site_url, _it, runs, beats_for_item.get(_it["id"]) or [])

    # The shared bundle, written once and linked by every page. FONTPREFIX is
    # empty because relative url() in a stylesheet resolves against the
    # stylesheet's own location, and this file sits at the root beside fonts/.
    # GATE EVERY PAGE FIRST, THEN WRITE.
    #
    # These two ran in one loop, and db.fail is sys.exit(1), so a page failing
    # the punctuation or colon gate left docs/ half updated: the pages built
    # before it were new, the rest stale, and no feeds, sitemap, docket.json or
    # Markdown mirror were written at all, because those come after. The site
    # then disagreed with itself about what it contained, and the failure that
    # was supposed to stop a bad ship had already published part of one.
    #
    # An em dash in a source name is enough to trigger it, which is exactly the
    # case house() exists for and feeds_build was missing.
    for rel, html in pages.items():
        bad = db.BANNED.findall(html)
        if bad:
            db.fail(f"banned punctuation in {rel} {bad[:8]}")
        prose_colon_gate(rel, html)
    out.mkdir(parents=True, exist_ok=True)
    # Pillow is the one soft dependency, and without it grain_data_uri() returns
    # "" and this quietly wrote url(none) into the sheet every page loads. A
    # 2026-07-29 build on a box without Pillow stripped the film grain from all
    # 47 pages and the only trace was a one-line diff in site.css that a run
    # would have committed without noticing. Degrading the whole site's texture
    # is not a fallback, so say so instead.
    grain = db.grain_data_uri()
    if not grain:
        db.fail("no grain texture (Pillow missing). pip install Pillow, then "
                "rebuild. Shipping without it silently flattens every page.")
    (out / "site.css").write_text(
        SITE_CSS.replace("FONTPREFIX", "").replace("GRAIN_URI", grain))
    (out / "site.js").write_text(JS)
    for rel, html in pages.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)

    # The videos page is a static passthrough, owned outside this generator.
    # docs/videos/index.html is a hand-built, self-contained player (inline
    # CSS/JS; it fetches its feed at runtime) and docs/videos/videos.json is
    # that feed, data prepended daily by publish_feed.py in the
    # alaska-ai-weekly repo. Neither file is generated, reformatted, or
    # deleted here, ever. Building into a fresh out dir copies both over
    # byte for byte so the VIDEOS nav link on every page still resolves.
    videos_src = REPO / "docs" / "videos"
    if videos_src.is_dir():
        if (out / "videos").resolve() != videos_src.resolve():
            (out / "videos").mkdir(parents=True, exist_ok=True)
            for name in ("index.html", "videos.json"):
                f = videos_src / name
                if f.exists():
                    (out / "videos" / name).write_bytes(f.read_bytes())
    else:
        print("warning: docs/videos/ not found, the VIDEOS nav link will 404",
              file=sys.stderr)

    # The docket as a DATASET, not a dump. It used to carry only `updated` and
    # `items`, which told a consumer nothing about the contract, nothing about
    # what the fields mean, and never granted permission to reuse it, so nobody
    # could build on it and no catalogue could index it. The envelope below is
    # the contract: a version to pin, a license to rely on, field documentation
    # a human and a machine can both read, and the canonical URL of every item.
    feed = json.dumps({
        "name": "The Alaska AI Docket",
        "description": ("Every AI-infrastructure decision in Alaska. Land leases, "
                        "comment windows, utility votes, legislation and federal "
                        "solicitations, with the deciding body, the dates that "
                        "matter, whether the public has a way in, and a fetched "
                        "source for every fact."),
        "version": DOCKET_SCHEMA_VERSION,
        "updated": today.isoformat(),
        "canonical": f"{site_url}/docket.json",
        "documentation": f"{site_url}/data/",
        "license": DATA_LICENSE,
        "license_label": DATA_LICENSE_LABEL,
        "attribution": "Alaska AI, https://alaskaaihq.com",
        "publisher": "Alaska AI",
        "spatial_coverage": "Alaska, United States",
        "temporal_coverage": docket_temporal(docket[0]),
        "count": len(docket[0]),
        "fields": DOCKET_FIELD_DOCS,
        "enums": {
            "kind": sorted(db.KINDS),
            "status": sorted(db.STATUSES),
            "public_access": sorted(db.ACCESS),
            "key_dates.kind": sorted(db.DATE_KINDS),
        },
        # The reciprocal half of the gas watch cross reference. Emitted into
        # the feed rather than written into ledger/docket.json, so the two
        # datasets join by stable id without mutating a machine-maintained
        # ledger whose item count and schema other gates depend on. Additive,
        # which the docket's own version policy already allows for.
        "items": [
            dict(it, url=f"{site_url}/docket/{it['id']}/",
                 **({"related_dataset": f"{site_url}/gas-watch.json",
                     "related_dataset_page": f"{site_url}/gas-watch/"}
                    if it["id"] == GAS_WATCH_META["docket_item_id"] else {}))
            for it in docket[0]],
    }, indent=2)
    (out / "docket.json").write_text(feed)
    (out / "docket").mkdir(exist_ok=True)
    (out / "docket" / "docket.json").write_text(feed)
    # The gas watch series, beside the docket and deliberately not inside it.
    # Same envelope keys so the two read as one data family, but `series` where
    # the docket has `items`, because a time series does not fit a schema built
    # around who decides and when.
    (out / "gas-watch.json").write_text(json.dumps(
        gw.feed(gas_series, gas_model, site_url, today, GAS_WATCH_META,
                figs=gas_figs), indent=2))
    touch_icon(out)
    (out / "sitemap.xml").write_text(sitemap(site_url, runs, today, docket[0]))
    (out / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# AI answer engines and their crawlers are welcome to read and cite this site.\n"
        "# Attribution to Alaska AI with a link to the page is requested.\n"
        "# Every article also exists as Markdown at the same path plus index.md,\n"
        "# and the whole corpus is one fetch at /llms-full.txt.\n"
        "# Every tracked decision has its own page at /docket/<id>/ and the whole\n"
        "# docket is versioned open data at /docket.json, CC BY 4.0, documented\n"
        "# at /data/. Cook Inlet Gas Watch is a second dataset on the same terms,\n"
        "# a daily record of Southcentral Alaska gas storage at /gas-watch/ and\n"
        "# /gas-watch.json. Citing a specific decision page is the intended use.\n\n"
        f"Sitemap: {site_url}/sitemap.xml\n")
    # ---------- the machine-readable surface ----------
    # Feeds carry full content, not teasers. This publication wants to be
    # quoted correctly more than it wants the click, and the two newsrooms it
    # competes with publish either a headline-only feed or no feed at all.
    feeds = {
        "feed.xml": fb.rss(site_url, runs),
        "atom.xml": fb.atom(site_url, runs),
        "feed.json": fb.json_feed(site_url, runs),
        "docket/feed.xml": fb.docket_rss(site_url, docket[0]),
    }
    # Same rule for the feeds: validate all four, then write all four, so a
    # malformed atom.xml cannot leave a fresh feed.xml beside a stale one.
    for rel, text in feeds.items():
        fb.validate(rel, text, db.fail)
    for rel, text in feeds.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    # A Markdown mirror beside every deck page. An agent fetching a URL would
    # rather have 3 KB of Markdown than parse 60 KB of HTML for the story
    # inside it, and the file costs one write per run.
    for r in runs:
        (out / "archive" / r["date"] / "index.md").write_text(
            fb.deck_markdown(r, site_url))
    (out / "llms-full.txt").write_text(fb.llms_full_txt(site_url, runs, {"items": docket[0]}))
    (out / "llms.txt").write_text(fb.llms_txt(
        site_url, runs,
        topics=[{**t, "count": len(tindex.get(t["slug"]) or [])} for t in TOPICS],
        decisions=docket[0],
        gas_watch=({"count": len(gas_series),
                    "coverage": f"{gas_series[0]['date']} to {gas_series[-1]['date']}"}
                   if gas_series else None)))
    # IndexNow ownership proof.
    #
    # Bing, Yandex, Seznam and Naver take a push instead of waiting for a crawl,
    # and the whole protocol is this: host a file named for your key, containing
    # your key. scripts/indexnow.py then submits changed URLs and they are
    # fetched in minutes rather than whenever the crawler next wanders past.
    #
    # Worth being exact about the benefit, because it is easy to oversell.
    # GOOGLE DOES NOT USE INDEXNOW and this does nothing for a Google ranking.
    # It matters because Bing's index is what Copilot and ChatGPT search read,
    # so this is about being citable by the answer engines, which is the same
    # reason /llms.txt and the per-decision pages exist.
    (out / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY + "\n")
    (out / ".nojekyll").write_text("")
    if domain:
        (out / "CNAME").write_text(domain + "\n")
    print(f"site -> {out} ({len(pages)} pages, {len(runs)} decks, "
          f"{len(docket[1])} tracked decisions)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="build date YYYY-MM-DD (America/Anchorage)")
    ap.add_argument("--out", default="docs")
    ap.add_argument("--domain", default=db.DEFAULT_DOMAIN,
                    help="custom domain; emits CNAME and rewrites absolute URLs")
    args = ap.parse_args()
    site = f"https://{args.domain}" if args.domain else db.DEFAULT_SITE
    build(ddate.fromisoformat(args.date), args.out, site, args.domain)


if __name__ == "__main__":
    main()
