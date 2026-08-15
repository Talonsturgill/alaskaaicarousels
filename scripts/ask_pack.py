#!/usr/bin/env python3
"""Build the answering pack: the whole public record as prose, for one prompt.

WHY THERE IS NO RETRIEVAL HERE, AGAIN. ask_corpus.py already makes the argument
and this file is the same argument carried one step further. The published
record is small enough to hand a model whole, so there is no embedding step, no
vector store, no chunking and no similarity threshold. The single largest source
of wrong answers in a retrieval chatbot is retrieving the wrong passage, and a
record this size lets us delete that failure mode instead of tuning it.

WHY A SECOND ARTIFACT, THEN. ask-corpus.json is built for MACHINE checking. It
carries every source URL, every ISO stamp and the full gas series, because the
numeral allow-list is derived from it and a figure missing from that set becomes
a refused true answer. That shape is wrong for a model to read: long query
strings and repeated timestamps spend tokens without carrying answers.

So this is a pure function OF that corpus, not a parallel copy of the record.
It imports ask_corpus.build() and renders it. There is no second source of
truth here and no sync step that can fall behind, which is the whole reason the
design does not want a database.

THE ALLOW-LIST HERE IS TIGHTER ON PURPOSE. It is derived from the rendered pack
rather than from the corpus, so an answer may only state a number the model was
actually shown. The archive lane in workers/ask/deep.js checks against the
wider corpus set, because that lane reads the whole repository and legitimately
quotes figures this pack leaves out. Two lanes, two surfaces, each checked
against what it was given.

SIZE IS A HARD GATE, NOT A TARGET. Every token here is paid for on every
question. A pack that quietly doubles is a bill that quietly doubles, so going
over the ceiling fails the build rather than costing money nobody chose to
spend.
"""

import argparse
import json
import os
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import ask_corpus as ac  # noqa: E402
import gaswatch_build as gw  # noqa: E402
import gaswatch_collect as gc  # noqa: E402

OUT = os.path.join(REPO, "docs", "ask-pack.json")

# Roughly four characters per token for English prose. The exact figure comes
# from the token counting endpoint and is worth confirming before the spend
# ceiling is set, but a build gate has to work offline, so this is the
# conservative local stand-in.
CHARS_PER_TOKEN = 4.0

# The ceiling, and what it is calibrated against.
#
# Today's pack is about 21k tokens, essentially all of it the docket prose, at
# roughly 1k tokens per tracked item. So this is set at about 1.5x the current
# size. That is deliberate: the gate exists to catch a QUIET DOUBLING, which is
# what a duplication bug or a raw structure dumped back into render() would
# look like, and 32k catches that while leaving room to track a dozen more
# decisions without anyone having to think about it.
#
# At Haiku 4.5 input rates this ceiling is 3.2 cents a question, so the worst
# case the gate permits is still a few dollars a month at the traffic this box
# sees. When the record genuinely outgrows it, the move is to trim each item's
# history to its most recent notes, or to go to two hops with an index first.
# Both are design changes to make on purpose. Raising this number because a
# build went red is not.
MAX_TOKENS = 32_000


def esc_dashes(text):
    """House rule. No em or en dashes anywhere, including in what a model reads.

    A model writes in the register it is shown. The record itself is already
    gated by docket_build and site_build, so this only ever catches a stray in
    an upstream field, but catching it here is cheaper than catching it in an
    answer a reader is looking at.
    """
    return (text or "").replace("—", ", ").replace("–", " to ")


def place(loc):
    """A location as a person says it, not as the map stores it.

    The field is a dict carrying a name and a lon/lat pair for the docket map.
    Rendering it whole printed a Python repr into the pump and, worse, admitted
    the coordinates to the numeral allow-list, which loosens the strongest
    check here so a reader can be told a latitude nobody asked for.
    """
    if isinstance(loc, dict):
        return loc.get("name") or ""
    return loc or ""


def wrap_fields(it):
    """The one-line facts a reader most often asks for by name."""
    bits = []
    for label, key in (("Kind", "kind"), ("Status", "status"),
                       ("Decider", "decider")):
        if it.get(key):
            bits.append(f"{label}: {it[key]}")
    where = place(it.get("location"))
    if where:
        bits.append(f"Location: {where}")
    return " | ".join(bits)


def render_item(it):
    lines = [f"--- {it['id']} ---", f"Title: {esc_dashes(it.get('title'))}"]

    fields = wrap_fields(it)
    if fields:
        lines.append(fields)

    if it.get("public_access"):
        access = f"Public access: {it['public_access']}"
        if it.get("access_note"):
            access += f". {esc_dashes(it['access_note'])}"
        lines.append(access)

    seen, upd = it.get("first_seen"), it.get("last_updated")
    if seen or upd:
        lines.append(f"First seen {seen or 'unknown'}. Last updated {upd or 'unknown'}.")

    if it.get("summary"):
        lines.append(f"Summary: {esc_dashes(it['summary'])}")

    if it.get("key_dates"):
        lines.append("Key dates:")
        for d in it["key_dates"]:
            lines.append(f"  {d.get('date', '')}  {esc_dashes(d.get('label'))}")

    if it.get("history"):
        lines.append("History, oldest first:")
        for h in it["history"]:
            lines.append(f"  {h.get('date', '')}  {esc_dashes(h.get('note'))}")

    # Outlets, not URLs. A reader who wants the document follows the citation to
    # the item's own page, which carries every link. Rendering the query strings
    # here would spend real tokens on text no answer ever quotes.
    srcs = it.get("sources") or []
    if srcs:
        outlets = []
        for s in srcs:
            o = s.get("outlet")
            if o and o not in outlets:
                outlets.append(o)
        lines.append(f"Sources ({len(srcs)}): " + "; ".join(outlets))

    return "\n".join(lines)


def _num(v):
    """A figure as the record writes it, or a plain absence."""
    return "not public" if v is None else json.dumps(v)


def render_reading(row, label):
    """One daily reading, as labelled prose rather than as its raw row.

    The stored row is about 4,400 characters of nested JSON, most of it design
    constants and provenance stamps that repeat unchanged every day. Two of
    those rows were most of this section and none of it was answering
    questions. These are the measured and derived figures a reader actually
    asks for, at roughly a quarter of the size.
    """
    c = row.get("cingsa") or {}
    d = row.get("derived") or {}
    lines = [f"{label} ({row.get('date')}), read from CINGSA at "
             f"{c.get('source_timestamp')}, fetch {c.get('fetch_status')}:"]

    lines.append(
        f"  Measured storage: inventory {_num(c.get('inventory_mcf'))} Mcf, "
        f"{_num(c.get('inventory_pct_of_design'))} percent of the "
        f"{_num(c.get('storage_design_mcf'))} Mcf design, day over day change "
        f"{_num(c.get('inventory_delta_mcf'))} Mcf.")
    lines.append(
        f"  Measured deliverability: withdrawal available "
        f"{_num(c.get('withdrawal_available_mcfd'))} Mcf/d against a "
        f"{_num(c.get('withdrawal_design_mcfd'))} Mcf/d design; injection "
        f"available {_num(c.get('injection_available_mcfd'))} Mcf/d against "
        f"{_num(c.get('injection_design_mcfd'))} Mcf/d.")
    lines.append(
        f"  Derived: modeled peak demand {_num(d.get('peak_modeled_demand_mmcfd'))} "
        f"MMcf/d on {d.get('peak_forecast_date')} at "
        f"{_num(d.get('peak_forecast_hdd'))} HDD; days of cover at that peak "
        f"{_num(d.get('days_cover_at_peak'))}; measured storage withdrawal "
        f"{_num(d.get('storage_withdrawal_mmcfd'))} MMcf/d; non CINGSA supply "
        f"{_num(d.get('non_cingsa_supply_mmcfd'))}.")
    if d.get("days_cover_note"):
        lines.append("  On days of cover: " + esc_dashes(d["days_cover_note"]))
    if c.get("operational_note"):
        lines.append("  CINGSA operational note: " + esc_dashes(c["operational_note"]))
    flags = row.get("flags") or []
    if flags:
        lines.append("  Flags: " + ", ".join(str(f) for f in flags))
    return "\n".join(lines)


def render_figures(figs):
    """The numbers the GAS WATCH PAGE actually displays, in the page's own units.

    This exists because of a real failure. A reader asked how much gas is in
    storage. The page says "6.83 of 13.0 Bcf". The pack carried only
    6828861 Mcf, so 6.83 was not an authorised numeral, so the answer naming
    the figure the page publishes was cut by the guard as an invention.

    The guard was right and the pack was wrong. Both come from
    gaswatch_build.figures(), the one place every published number on that page
    is computed, so what the answerer may say and what the page shows are now
    the same set by construction rather than by coincidence.
    """
    if not figs:
        return ""
    keep = ("as_of", "inventory_bcf", "design_bcf", "inventory_mcf",
            "inventory_pct_of_design", "inventory_delta_mmcf",
            "withdrawal_operating_mmcfd", "days_cover_at_peak",
            "peak_modeled_demand_mmcfd")
    bits = [f"{k} {_num(figs[k])}" for k in keep if k in figs]
    if not bits:
        return ""
    return ("As the page states them, in the units the page uses: "
            + "; ".join(bits) + ".")


def render_gas(gas, figs=None):
    """The gas watch as a position, not as a time series.

    A model does not need every daily row to answer questions about the gas
    watch, and shipping them would be most of the pack. It needs the newest
    reading, one prior reading for direction of travel, how the demand model
    is built and checked, and above all the rule the page lives by, which is
    that this record publishes measurements and never a verdict.
    """
    series = gas.get("series") or []
    lines = ["=== COOK INLET GAS WATCH ===",
             esc_dashes(gas.get("description"))]

    if gas.get("temporal_coverage"):
        lines.append(f"Coverage: {gas['temporal_coverage']}, "
                     f"{gas.get('count', len(series))} daily readings.")
    if gas.get("updated"):
        lines.append(f"Last updated {gas['updated']}.")

    if series:
        lines.append(render_reading(series[-1], "NEWEST READING"))
        if len(series) > 1:
            prev = series[-2]
            pc = prev.get("cingsa") or {}
            lines.append(
                f"Previous reading ({prev.get('date')}), for direction of travel "
                f"only: inventory {_num(pc.get('inventory_mcf'))} Mcf, "
                f"{_num(pc.get('inventory_pct_of_design'))} percent of design.")

        m = (series[-1].get("model") or {})
        if m.get("formula"):
            lines.append(f"Demand model {m.get('version')}: {m['formula']}. "
                         f"{esc_dashes(m.get('calibration'))}")
        mb = m.get("mass_balance") or {}
        if mb.get("identity"):
            lines.append(f"Mass balance: {mb['identity']}. {esc_dashes(mb.get('note'))}")
        if m.get("not_public"):
            lines.append("Not public, and therefore not in this record: " +
                         "; ".join(str(x) for x in m["not_public"]))

        r = series[-1].get("reconciliation") or {}
        if r:
            lines.append(
                f"Most recent reconciliation ({r.get('date')}): forecast "
                f"{_num(r.get('forecast_hdd65'))} HDD against actual "
                f"{_num(r.get('actual_hdd65'))}, error {_num(r.get('error'))}; "
                f"modeled demand {_num(r.get('modeled_demand_mmcfd'))} MMcf/d.")

    cc = gas.get("crosscheck")
    if cc:
        lines.append(
            f"Model cross check against observed EIA deliveries: latest month "
            f"{cc.get('eia_latest_month')}, {_num(cc.get('eia_months_checked'))} "
            f"months checked, model gap {_num(cc.get('eia_model_gap_pct'))} "
            f"percent, Alaska working gas {_num(cc.get('eia_ak_working_gas_bcf'))} "
            f"Bcf against {_num(cc.get('eia_ak_capacity_bcf'))} Bcf capacity.")

    mh = gas.get("model_history") or []
    if mh:
        newest = mh[-1]
        lines.append(f"Demand model version {newest.get('version')}, effective "
                     f"{newest.get('effective')}: {esc_dashes(newest.get('reason'))}")

    disp = render_figures(figs)
    if disp:
        lines.append(disp)

    if gas.get("warning"):
        lines.append("STANDING LIMIT ON THIS DATA: " + esc_dashes(gas["warning"]))

    lines.append(
        "This record NEVER publishes a safety verdict. Not a shortfall "
        "prediction, not an all clear, not a blackout call. Supply side "
        "deliverability is not public, so a verdict is not a call this data "
        "can carry. Report the measured numbers and say plainly that the "
        "adequacy question is not one this record answers.")
    return "\n".join(lines)


def render(corpus, figs=None):
    items = corpus["docket"]["items"]
    head = [
        f"THE ALASKA AI DOCKET, as published on {corpus['generated']}.",
        "",
        "This is the complete public record behind alaskaaihq.com. It is two "
        "things: a docket of tracked Alaska decisions about artificial "
        "intelligence, and the Cook Inlet Gas Watch, a daily numeric record of "
        "Southcentral Alaska's natural gas position.",
        "",
        "Cite a docket item by writing its id in double brackets, like "
        "[[enstar-cook-inlet-gas-storage]]. The page turns that into a link.",
        "",
        f"=== TRACKED DECISIONS ({len(items)}) ===",
        "",
    ]
    body = "\n\n".join(render_item(it) for it in items)
    return ("\n".join(head) + body + "\n\n"
            + render_gas(corpus["gas_watch"], figs) + "\n")


# The instructions the worker sends with the pack. They live here, beside the
# record they describe, so a change to what the model is shown and a change to
# what it is told to do with it are the same commit.
SYSTEM = """You answer questions about the Alaska AI docket, using ONLY the record supplied below. You are the site speaking.

HOW TO TALK. Like a knowledgeable person who has read all of this and is happy to be asked, not like a search result and not like a form letter. Plainly and briefly, usually three sentences or fewer. Contractions. No preamble, no restating the question, no "based on the record" throat clearing, and never a bulleted list where a sentence would do.

This is a conversation and it will continue. Earlier turns are above; a follow-up like "what about the other one" or "who decides that" refers to what was just said, so read it that way rather than answering it cold.

END BY OFFERING THE NEXT THING. One short question, and only when there is a real one to ask, drawn from what this record actually holds next to what was just asked: the other item in the same fight, the deadline attached to it, how it got here, what the same decider has done elsewhere. Offer, do not interrogate. "Want the comment deadline?" is an offer. "Do you have any other questions?" is filler and is worse than stopping. When the honest answer is that the record has nothing adjacent, stop talking.

Hard rules, in order:

1. NUMBERS. Only state a number that appears verbatim in the record. Never compute a new one, never round, never convert units, never work out a difference between two figures, and never work out an interval between two dates.

This is enforced, not advisory: every sentence you write is checked against the record's numerals before a reader sees it, and a sentence containing a number the record does not state is cut. A cut sentence helps nobody, so when a question asks for a figure you would have to calculate, DO NOT attempt the calculation and then hedge. Open by saying plainly that the record does not state it, then give the figures it does state and let the reader do the arithmetic. "The record gives 6.83 Bcf on August 13th and 6.5 Bcf on August 5th; it does not state the change between them" is a good answer. Computing 0.33 is a cut one.

Where the record gives the same quantity twice in different units, either is fine, so prefer the one a person would use. Storage is published as both Mcf and Bcf; say Bcf.

2. CITATIONS. Refer to a tracked decision by putting its id in double brackets, like [[aidea-houston-industrial-park]]. Only ever cite an id that appears in the record.

3. THE GAS WATCH NEVER GETS A VERDICT. Do not say whether there is enough gas, whether the region will make it through a cold snap, whether a shortfall is likely, or that anything is safe, fine, adequate or an all clear. Supply side deliverability is not public. Report the measured numbers and say plainly that adequacy is not a question this record answers.

4. WHAT IS NOT THERE. If the record does not cover the question, say so in one sentence and stop. Do not guess, do not reason from general knowledge about Alaska or about AI, and do not soften a no into a maybe. A visible no is the correct answer and readers are told the box works this way.

House voice: no em dashes or en dashes, no emojis, straight quotes only, and write "can't" rather than "cannot". Dates are written month first with the ordinal, like August 14th.

THE RECORD FOLLOWS.
"""


def build(today=None, site_url="https://alaskaaihq.com"):
    corpus = ac.build(today=today, site_url=site_url)
    # The page's own display figures, from the one function that computes them.
    figs = gw.figures(gw.load_series(), gc.load_model(gw.MODEL_CONFIG))
    text = render(corpus, figs)
    approx = round(len(text) / CHARS_PER_TOKEN)
    return {
        "generated": corpus["generated"],
        "system": SYSTEM,
        "pack": text,
        # Derived from the rendered pack, so the model may only state a number
        # it was actually shown. Deliberately tighter than the corpus set.
        "authorised_numerals": sorted(ac.numerals(text)),
        "slugs": sorted(corpus["slugs"]),
        "chars": len(text),
        "approx_tokens": approx,
    }


def write(path=OUT, **kw):
    pack = build(**kw)
    if pack["approx_tokens"] > MAX_TOKENS:
        raise SystemExit(
            f"ask pack is roughly {pack['approx_tokens']} tokens, over the "
            f"{MAX_TOKENS} ceiling. Every token here is paid on every question, "
            f"so trim render() or raise MAX_TOKENS deliberately. It is not a "
            f"number to nudge because a build went red.")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(pack, fh, separators=(",", ":"), sort_keys=True)
    return pack, path


def self_test():
    print("the pack")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    p = build()
    text = p["pack"]
    corpus = ac.build()

    check("every docket item is in the pack",
          all(it["id"] in text for it in corpus["docket"]["items"]),
          f"{len(corpus['docket']['items'])} items")
    check("every slug is listed", len(p["slugs"]) == len(corpus["slugs"]))
    check("the gas watch section is present", "COOK INLET GAS WATCH" in text)
    check("the standing no-verdict rule is in the pack",
          "NEVER publishes a safety verdict" in text)

    print("house rules in what the model reads")
    check("no em or en dashes", "—" not in text and "–" not in text)
    check("no curly quotes",
          not any(c in text for c in "‘’“”"))
    check("no em or en dashes in the instructions",
          "—" not in SYSTEM and "–" not in SYSTEM)

    print("the allow-list")
    allowed = set(p["authorised_numerals"])
    # It has to cover its own source, or a true answer gets refused.
    missing = [t for t in ac.numerals(text) if t not in allowed]
    check("every numeral in the pack is authorised", not missing, str(missing[:3]))
    # And it has to be able to refuse, or it proves nothing.
    check("a number the record does not contain is NOT authorised",
          not [t for t in ("87654321", "99999.7") if t in allowed])
    # Every numeral the answerer may state has to come from something the site
    # actually publishes. That is the corpus, PLUS the display figures on the
    # gas watch page, which are rounded into the units a person reads and so do
    # not appear in the corpus at all. 6.83 Bcf is the case: the page says it,
    # the corpus holds only 6828861 Mcf, and without this the answer naming the
    # figure the page publishes was cut as an invention.
    wide = set(corpus["authorised_numerals"])
    figs = gw.figures(gw.load_series(), gc.load_model(gw.MODEL_CONFIG))
    wide |= ac.numerals(render_figures(figs))
    stray = sorted(allowed - wide)
    check("every numeral the answerer may state is one the site publishes",
          not stray, f"{len(allowed)} allowed" +
          (f", stray {stray[:3]}" if stray else ""))
    # And the page's own headline figure has to be sayable, which is the whole
    # reason this pack carries the figures block.
    check("the storage figure the page displays is sayable",
          str(figs.get("inventory_bcf")) in allowed,
          f"inventory_bcf {figs.get('inventory_bcf')}")

    print("size, which is the cost")
    check(f"under the {MAX_TOKENS} token ceiling", p["approx_tokens"] <= MAX_TOKENS,
          f"{p['chars']} chars, roughly {p['approx_tokens']} tokens")
    # Cost per question at Haiku 4.5 input rates, so a change in the pack shows
    # up here as money rather than as a number that got bigger.
    print(f"        input cost per question at $1.00/1M: "
          f"${p['approx_tokens'] / 1_000_000:.4f}")

    print("determinism")
    check("two builds of the same day agree", build()["pack"] == text)

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--date", help="ISO date, America/Anchorage")
    ap.add_argument("--print", action="store_true", help="write the prose to stdout")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    today = date.fromisoformat(args.date) if args.date else date.today()
    if args.print:
        sys.stdout.write(build(today=today)["pack"])
        return 0

    pack, path = write(args.out, today=today)
    print(f"ask pack -> {path} ({len(pack['slugs'])} items, "
          f"{len(pack['authorised_numerals'])} numerals, "
          f"{pack['chars']} chars, roughly {pack['approx_tokens']} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
