#!/usr/bin/env python3
"""critic_brief.py -- the plan lines a pixel critic needs to judge a frame's art the way the flow critic will.

WHY THIS EXISTS (2026-10-04, the first weekly machine pass).

In the week of September 28th to October 3rd the flow critic named 32 weakest
frames across six decks, and 31 of them under a cause that belongs to ONE frame:
b, the largest object least modelled (10 frames, all six decks); c, a dead or
eventless region, above all the lower third (8 frames, five decks); d, a texture
artifact (13 frames, all six). Every one of those frames had already been through
its pixel critic's loop, which runs until every slide verdicts ship (or four rounds)
before the flow critic is spawned. The pixel critic's protocol never asked the
three questions: it checks the dossier's checklist, "quiet zone intact", and
banding, and it was never handed the CRAFT PLAN row that says what the largest
object is and how it is to be modelled. So the defect was first named at the
deck-level review, with one craft cycle left to fix it, and the craft cycle moved
art by 0 to 0.5 on every run of the week.

The measured alternative was tried first and failed, and that is why this is a
brief and not a gate: over 226 shipped frames, a lower-band flatness measure
separated the frames critics named as dead from the rest at AUC 0.63, and over
108 frames a terminal-flat-band measure not at all (named frames 0.003 to 0.139
of frame height, unnamed p90 0.128). FIELD_NOTES, 2026-10-04 weekly pass.

So the plan goes to the eyes that see the frame first. For each slide this prints
the CRAFT PLAN row (primary mark-making; largest object and its modelling), field
4a (the lower-third treatment, with its y range when the dossier gives one), and
whether the slide is the masterful depth frame. Paste a slide's block into its
pixel critic's prompt (Phase 9 step 2); the critic answers `frame_causes` from it.

Since 2026-10-09 the block also lists the slide's NATIVE CROPS, the 100 percent
tiles render.py cuts from every frame (render/crops/), with the design-px region
of each, so cause d is judged at native size; a tile set cut from an earlier
render is reported stale and not listed. A missing or stale set never changes the
exit code.

    python3 scripts/critic_brief.py --run-dir out/2026-10-04 [--slide 5] [--json]
    python3 scripts/critic_brief.py --self-test

Read-only. Exit 0 when every requested slide has its lines, 2 when the storyboard
is missing or a slide lacks its CRAFT PLAN row or field 4a (dossier_check.py
FAILs those already; this says which).
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dossier_check as dc  # noqa: E402

Y_RANGE_RE = re.compile(r"\by\s*(\d{2,4})\s*(?:to|-)\s*(\d{2,4})\b", re.I)


def craft_rows(text):
    """{slide: (mark-making, largest object and modelling)} and the depth frame."""
    m = dc.CRAFT_PLAN_HEAD_RE.search(text)
    if not m:
        return {}, None
    nxt = re.search(r"^##\s", text[m.end():], re.M)
    block = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
    rows = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"\d{1,2}", cells[0]):
            rows[int(cells[0])] = (cells[1], cells[2])
    dm = re.search(r"^\s*[-*]?\s*Masterful depth frame:\s*(\d{1,2})", block, re.M | re.I)
    return rows, (int(dm.group(1)) if dm else None)


def brief(text, only=None):
    rows, depth = craft_rows(text)
    out, missing = [], []
    for no, _head, body in dc.slide_sections(text):
        if only and no != only:
            continue
        f4a, _ = dc.field_4a(body)
        row = rows.get(no)
        if not row:
            missing.append("%02d has no CRAFT PLAN row" % no)
        if not f4a:
            missing.append("%02d has no field 4a" % no)
        yr = Y_RANGE_RE.search(f4a or "")
        out.append({"slide": no,
                    "mark_making": row[0] if row else None,
                    "largest_object": row[1] if row else None,
                    "lower_third": f4a,
                    "lower_third_y": [int(yr.group(1)), int(yr.group(2))] if yr else None,
                    "masterful_depth_frame": depth == no})
    return out, missing


def native_crops(render_dir, slide):
    """The 100 percent tiles render.py cut from this slide's CURRENT frame.

    NATIVE CROPS (2026-10-09, weekly machine pass). Three runs of critics said
    they judged texture from a downscaled view; render.py now writes
    render/crops/slide-NN-rRcC.png, each tile small enough to be read at native
    size, and records the sha256 of the frame it cut them from. A tile set cut
    from an earlier render of the slide is reported STALE and never listed as
    evidence, because a crop of the frame the critic is not judging is worse
    than none. Returns {"tiles": [...]} or {"stale"|"missing": reason}.
    """
    if not render_dir:
        return {"missing": "no render dir"}
    rd = Path(render_dir)
    man = rd / "crops" / ("slide-%02d.json" % slide)
    frame = rd / ("slide-%02d.png" % slide)
    if not man.exists() or not frame.exists():
        return {"missing": "no native crops for slide %02d in %s (render.py writes "
                           "them beside every frame it renders)" % (slide, rd / "crops")}
    try:
        m = json.loads(man.read_text())
    except Exception as e:
        return {"missing": "crops manifest did not parse (%s)" % type(e).__name__}
    import hashlib
    if hashlib.sha256(frame.read_bytes()).hexdigest() != m.get("frame_sha256"):
        return {"stale": "the tiles in %s were cut from an earlier render of slide %02d; "
                         "re-render it with render.py to refresh them" % (rd / "crops", slide)}
    tiles, lost = [], []
    for t in m.get("tiles") or []:
        p = (rd / "crops" / t["file"]).resolve()
        if p.exists():
            tiles.append({"path": str(p), "design": t.get("design")})
        else:
            lost.append(t["file"])
    # a partial set would be read as a full 100 percent view (Codex, PR #422)
    if lost or not tiles:
        return {"stale": "the crop set for slide %02d is incomplete (%s missing); re-render "
                         "it with render.py to cut every tile" % (slide, ", ".join(lost) or "all")}
    return {"tiles": tiles}


def crop_lines(c):
    if c.get("tiles"):
        out = ["  native crops, 100 percent (Read every tile before answering cause d; "
               "regions in design px):"]
        for t in c["tiles"]:
            d = t["design"] or [0, 0, 0, 0]
            out.append("    x %d to %d, y %d to %d: %s" % (d[0], d[2], d[1], d[3], t["path"]))
        return out
    return ["  native crops: %s" % (c.get("stale") or c.get("missing"))]


def render_block(b):
    yr = b["lower_third_y"]
    tail = crop_lines(b["native_crops"]) if "native_crops" in b else []
    return "\n".join([
        "CRAFT LINES, slide %02d (from the storyboard; answer frame_causes against these)" % b["slide"],
        "  primary mark-making: %s" % (b["mark_making"] or "MISSING"),
        "  largest object, and how the plan models it: %s" % (b["largest_object"] or "MISSING"),
        "  lower third (field 4a)%s: %s" % (
            ", design y %d to %d" % tuple(yr) if yr else "", b["lower_third"] or "MISSING"),
        "  masterful depth frame: %s" % ("YES, the deck's depth is earned here" if b["masterful_depth_frame"]
                                         else "no")] + tail)


def self_test():
    bad = 0

    def ok(label, cond, extra=""):
        nonlocal bad
        print("  %s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond else "  " + str(extra)))
        bad += 0 if cond else 1

    sb = """# Deck

## CRAFT PLAN
| slide | primary mark-making | largest object, and how it is modelled |
|---|---|---|
| 01 | akthree PBR render | the year rule, ground steel with a lit bevel and a two-part contact shadow |
| 02 | layout-blue scribe | the rule face, lacquer with orange-peel relief lit from above |
Masterful depth frame: 01, the rule on lit granite
Tonal arc: dark 01, the lit peak on 02

## SLIDE 01, The rule
**4a. Lower-third treatment.** From y 900 to 1260 the rule's near chamfer and its contact shadow
on lit granite whose flecks carry tone to the bottom edge.

**5. Something else.** x

## SLIDE 02, The face
No lower third declared here.

## BUILD RECONCILIATION
nothing
"""
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "storyboard.md"
        p.write_text(sb)
        b, missing = brief(p.read_text())
        ok("one block per dossier", [x["slide"] for x in b] == [1, 2], b)
        ok("the CRAFT PLAN row reaches its slide", b[0]["largest_object"].startswith("the year rule")
           and b[1]["mark_making"] == "layout-blue scribe", b)
        ok("field 4a is read whole, across its wrapped line, with its y range",
           "bottom edge" in (b[0]["lower_third"] or "") and b[0]["lower_third_y"] == [900, 1260], b[0])
        ok("the depth frame is flagged on its slide only",
           b[0]["masterful_depth_frame"] and not b[1]["masterful_depth_frame"], b)
        ok("a slide without field 4a is named", missing == ["02 has no field 4a"], missing)
        one, _ = brief(p.read_text(), only=2)
        ok("--slide selects one block", [x["slide"] for x in one] == [2], one)
        ok("the printed block says MISSING rather than nothing", "MISSING" in render_block(one[0]))
        # native crops: fresh tiles listed with their design region, a frame
        # re-rendered after the cut reads stale, no crops reads missing
        import hashlib
        rd = Path(td) / "render"
        (rd / "crops").mkdir(parents=True)
        frame = rd / "slide-01.png"
        frame.write_bytes(b"frame one")
        (rd / "crops" / "slide-01-r1c1.png").write_bytes(b"tile")
        (rd / "crops" / "slide-01.json").write_text(json.dumps({
            "frame": "slide-01.png", "frame_sha256": hashlib.sha256(b"frame one").hexdigest(),
            "tiles": [{"file": "slide-01-r1c1.png", "design": [0, 0, 540, 450]}]}))
        c = native_crops(rd, 1)
        ok("fresh crops are listed with their design region",
           len(c.get("tiles") or []) == 1 and c["tiles"][0]["design"] == [0, 0, 540, 450], c)
        ok("the printed block names the tile and its region",
           "x 0 to 540, y 0 to 450" in render_block(dict(b[0], native_crops=c)))
        frame.write_bytes(b"frame two, re-rendered")
        c = native_crops(rd, 1)
        ok("crops cut from an earlier render read stale and list nothing",
           "stale" in c and not c.get("tiles"), c)
        ok("a slide with no crops reads missing", "missing" in native_crops(rd, 2))
        # Codex, PR #422: a manifest naming a tile that is gone is incomplete, not a partial view
        (rd / "slide-03.png").write_bytes(b"frame three")
        (rd / "crops" / "slide-03-r1c1.png").write_bytes(b"tile")
        (rd / "crops" / "slide-03.json").write_text(json.dumps({
            "frame": "slide-03.png", "frame_sha256": hashlib.sha256(b"frame three").hexdigest(),
            "tiles": [{"file": "slide-03-r1c1.png", "design": [0, 0, 540, 450]},
                      {"file": "slide-03-r1c2.png", "design": [540, 0, 540, 450]}]}))
        c = native_crops(rd, 3)
        ok("a crop set with a tile missing reads incomplete and lists nothing",
           "stale" in c and "incomplete" in c["stale"] and not c.get("tiles"), c)
    print("\ncritic_brief self-test: " + ("all passed" if not bad else "%d FAILED" % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run-dir")
    ap.add_argument("--slide", type=int)
    ap.add_argument("--render-dir", help="where render.py wrote the frames and crops/; "
                                         "defaults to <run-dir>/render")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.run_dir:
        ap.error("--run-dir is required (or --self-test)")
    sb = Path(a.run_dir) / "storyboard.md"
    if not sb.exists():
        print("critic_brief: %s missing" % sb)
        return 2
    blocks, missing = brief(sb.read_text(encoding="utf-8"), a.slide)
    rdir = Path(a.render_dir) if a.render_dir else Path(a.run_dir) / "render"
    for b in blocks:
        b["native_crops"] = native_crops(rdir, b["slide"])
    if a.json:
        print(json.dumps({"slides": blocks, "missing": missing}, indent=2))
    else:
        print("\n\n".join(render_block(b) for b in blocks))
        for m in missing:
            print("[MISSING] " + m)
    return 2 if (missing or not blocks) else 0


if __name__ == "__main__":
    sys.exit(main())
