#!/usr/bin/env python3
"""caption_check.py — OBJECTIVE linter for the LinkedIn carousel post copy.

Runs BEFORE the scorer so a mechanically-broken caption never reaches the
subjective gates. Grounded in the 2026 evidence base (knowledge/
CAROUSEL_CRAFT.md): 140-char mobile fold, 300-900 char band for carousel
captions, exactly 3 hashtags at the end, no links in body, brand punctuation
rules (no em/en dashes, no semicolons, straight quotes), AI-tell scan,
closing engagement question required.

  python scripts/caption_check.py out/<run>/caption.txt \
      --ledger ledger/captions.json --deck-summary "<the deck-summary line>"
Writes caption_report.json next to the input. Exit 0 = PASS, 1 = FAIL.

BANNED PHRASES COME FROM TWO PLACES, AND BOTH ARE ENFORCED (2026-08-02).
Until this run the script's hardcoded AI_TELLS list was the only thing that
ran; config/brand.yaml's banned_phrases array was never loaded by anything, so
"leverage", "disrupt", "unlock" and "here's where the frame breaks" were
written down as banned and silently unenforced. The caption critic and the
scorer found this independently on 2026-08-02. brand.yaml is now loaded and
merged, which TIGHTENS the gate.

The one legitimate case, and how it is handled: a banned word inside a
straight-quoted VERBATIM passage. The 2026-08-02 caption opens on
'"Leverage technology, such as artificial intelligence," says an order the
governor signed last August.' That is the state's own words, quoted, and it is
the whole point of the deck. So a brand.yaml phrase that appears ONLY inside
straight double quotes is a WARN naming it, not a FAIL. The exemption is
deliberately narrow:
  - it applies to phrases sourced from brand.yaml only. Every phrase already
    in AI_TELLS keeps failing anywhere in the text, quoted or not, so nothing
    that failed before this change passes after it.
  - unbalanced quotes mean no exemption.

THE CAPTION IS NOT THE ONLY COPY A READER SEES (2026-08-08). Optional flag:

  python scripts/caption_check.py out/<run>/caption.txt --copy out/<run>/copy.json

Run No.29 shipped six bare non-ordinal dates ("August 5, 2026") in copy.json's
`first_comment`, the sources block that gets pasted under the post within 60
seconds of publishing. CLAUDE.md names the ordinal form as a house rule that
never bends and cites THIS FILE as its enforcement, and the enforcement was
real: DATE_FORMS would have caught every one of them. It just never saw the
text, because this gate reads caption.txt and nothing else. The scorer caught
it by eye at the ship gate. So the SAME rule table now also runs over the
reader-facing prose fields of copy.json, which is a widening of an existing
gate and adds no new rule. See COPY_READER_FIELDS for what is in scope and why
the editor-only fields are not.
"""
import json
import re
import sys
from pathlib import Path

FOLD = 140
LO, HI = 300, 900
HARD_MAX = 3000
HASHTAGS_EXACTLY = 3

AI_TELLS = ["delve", "tapestry", "testament", "landscape of", "ever-evolving",
            "ever-changing", "in today's", "navigating the", "unlock the",
            "unleash", "game-changer", "game changer", "realm of",
            "at the end of the day", "it's important to note", "paradigm",
            "synergy", "embark", "seamless", "cutting-edge", "revolutionize",
            "supercharge", "skyrocket", "buckle up", "let's dive",
            "here's the honest part", "here is the honest part",
            "here's what matters", "here is what matters",
            # Owner rule, 2026-08-06. The "here's the X part" construction is a
            # narrator clearing his throat before the point, and this one slips
            # past the two bans above because neither is a substring of it.
            "here's the part that matters", "here is the part that matters",
            "imagine if",
            "in a world where", "it's no secret"]
# DATE FORM (owner rule 2026-08-05: "rn ur saying '10 August', the normal way to say it is
# August 10th"). Month name first, day as an ordinal. ISO stays correct for a PROVENANCE
# STAMP (a citation line, a filename, a ledger field) but a sentence a human reads takes
# "August 10th". Mirrors alaska-ai-weekly's scripts/caption_check.py DATE_FORMS so the two
# surfaces cannot drift apart.
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
ABBREV = r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec"
DATE_FORMS = [
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + MONTHS + r")\b"),
     "day-first", "write the month first with an ordinal day, e.g. August 10th"),
    (re.compile(r"\b(" + MONTHS + r")\s+(\d{1,2})(?!\s*(?:st|nd|rd|th))(?!\d)"),
     "no ordinal", "add the ordinal, e.g. August 10th"),
    (re.compile(r"\bthe\s+\d{1,2}(?:st|nd|rd|th)\s+of\s+(" + MONTHS + r")\b"),
     "of-form", "write it plainly, e.g. August 10th"),
    (re.compile(r"\b(" + ABBREV + r")\.?\s+\d{1,2}\b"),
     "abbreviated month", "spell the month out with an ordinal day, e.g. August 10th"),
]

# COMMA DISCIPLINE (owner rule 2026-08-05: "reduce comma usage by 10% on the captions
# moving forward"). MEASURED AGAINST THIS DECK'S OWN CAPTIONS, not the weekly repo's.
# Across the 22 captions shipped as of that date the mean here was 6.88 commas per 100
# words of body (median 6.52), so ten percent below is 6.20 and the ceiling is 6.2.
#
# Deliberately NOT the 4.9 that alaska-ai-weekly uses. Carousel captions run shorter and
# comma-heavier, and applying that repo's number here would be a 29 percent cut rather than
# the 10 percent the owner asked for. The RULE is "ten percent below what this surface
# actually ships", and the two surfaces ship differently.
#
# The cure is NOT deleting commas and leaving a run-on. Split at the comma and let it be two
# sentences, or cut the clause that was only there to be qualified.
COMMA_PER_100W = 6.2

BANNED_PUNCT = {"—": "em dash", "–": "en dash", ";": "semicolon",
                "“": "curly quote", "”": "curly quote",
                "‘": "curly apostrophe", "’": "curly apostrophe"}
EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⌀-⏿]")
UNICODE_BOLD = re.compile("[\U0001D400-\U0001D7FF]")
URLISH = re.compile(r"https?://|www\.|\S+\.(com|org|net|io|gov|edu)/\S*", re.I)


# Contractions the house always prefers. "cannot" was banned outright by the
# maintainer on 2026-07-30 ("always use can't instead, especially in the
# captions"). It is a voice rule, not a typo rule: "cannot" is the register of a
# press release and "can't" is the register of a person talking, and this page
# is supposed to sound like an analyst talking to a busy Alaskan. Mechanically
# checkable, so it is a gate rather than a note in a doc nobody reads.
CONTRACTIONS = {"cannot": "can't"}

# THE COMMA BUDGET (maintainer rule, 2026-08-05). "Reduce comma usage by 10
# percent on the captions moving forward." Turned into a number rather than a
# vibe by measuring every shipped caption in runs/*/caption.txt, hashtag line
# excluded: 26 captions, mean 1.17 commas per 100 characters, median 1.12.
# Ten percent below the mean is 1.05, and that is the budget.
#
# It is a GATE and not a warning, because the deck-summary rule sat in
# brand.yaml as a true statement nobody enforced and lapsed for three runs
# running. A caption over budget is not wrong, it is over budget, and the fix
# is to cut a comma or split a sentence.
# NO FIRST PERSON IN THE CAPTION (maintainer rule, 2026-08-05). The page is an
# analyst describing the world, never a narrator describing their own work.
#
# THIS NEEDS TWO CHECKS AND NOT ONE, which is the whole lesson. A pronoun grep
# over all 26 shipped captions returns ZERO bare hits, so by that measure there
# was never a problem. The drift was real anyway, and it wore no pronoun:
# No.26 shipped "No page anyone could reach shows what SEDS-AK was worth" and
# opened a paragraph with "Enclosed,". Both are the studio narrating its own
# search and its own envelope; the first one is literally the de-pronouned
# rewrite of a slide that says "any page we could reach". Ban the pronouns AND
# ban the posture, or the posture just drops the pronoun and carries on.
# Case-insensitive, because "We stood up" is the same defect as "we stood up".
# Two deliberate omissions. "mine" is left OUT of the list: this page covers
# Graphite Creek, Red Dog and Ambler, so "the mine" is a noun here far more
# often than it is a possessive, and a gate that cries wolf on the mining beat
# would get worked around. And an ALL-CAPS match longer than one character is
# skipped, so "the US Air Force" is not read as "us" while a bare "I" still is.
FIRST_PERSON = re.compile(
    r"(?<![A-Za-z'])(I|I'm|I've|I'd|I'll|we|we're|we've|we'd|we'll|us|our|ours|"
    r"ourselves|my|me|let's)(?![A-Za-z'])", re.I)
# THE HOOK STANDS ALONE (maintainer rule, 2026-08-05, "ur last two captions
# have been trash, possible drift"). Sentence one is read cold, by a stranger
# scrolling, with no deck open and no context. It has to be a complete claim
# about the world on its own terms.
#
# The drift was real and it was the VARIETY ENGINE eating the caption. The
# engine exists to stop template repetition, and it started optimising for
# novelty of SHAPE, which beat clarity two runs running:
#
#   2026-08-04  "One column tallies 119.7 megawatts becoming 120.0."
#               One column of WHAT. The antecedent arrives three paragraphs
#               later. The hook is a riddle, not a claim.
#   2026-08-05  "To the Administration for Native Americans."
#               Addressed to a federal agency that will never read it, in a
#               feed of Alaskans who had 22 days to act. The reader is a
#               bystander to someone else's letter.
#
# Compare the two that worked, both plain claims a stranger gets instantly:
#   2026-08-02  "Leverage technology, such as artificial intelligence," says
#               an order the governor signed last August.
#   2026-08-03  AI supply chain here means one item on a five item list.
#
# CAPTION_CRAFT already said "form serves the story, never a gimmick for
# variety's own sake". The rule existed; nothing enforced it, and the
# showrunner's own briefs called the assigned move "binding", which is how a
# guardrail became a mandate. These three checks are the enforcement.
HOOK_ADDRESS = re.compile(r"^\s*(To the |To Mr|To Ms|To Dr|Dear )", re.I)
# The paired-deictic riddle: "One X ... The other ...". Both halves needed, so
# a plain "One in five Alaskans" opener never trips it.
HOOK_PAIRED = re.compile(r"^\s*One\b", re.I)
# A bare pronoun subject at position zero has nothing to refer back to. The
# verb requirement keeps "This week Alaska filed" and "These five notices"
# clean, since those carry their own noun.
HOOK_BARE_PRONOUN = re.compile(
    r"^\s*(It|They|This|That|These|Those)\s+(is|are|was|were|has|have|had|will|would|makes|made)\b")

# NO SENTENCE OPENS WITH "AND" OR "BUT" (maintainer rule, 2026-08-05). Those
# are conjunctions joining clauses, and a sentence starting on one is a fragment
# wearing a full stop. Currently clean across all 26 shipped captions, so this
# gate is preventive rather than remedial: it exists to stop a habit that shows
# up in the run records and the retros from leaking into the copy.
SENTENCE_START_CONJ = re.compile(
    r"(?:^|(?<=[.!?])\s+|(?<=\n))\s*(And|But)\b")

# The studio-as-narrator postures, first person with the pronoun filed off.
SELF_NARRATION = re.compile(
    r"\b(enclosed|(?:anyone|nobody|no one|we) could (?:not )?"
    r"(?:reach|find|obtain|locate|verify|confirm|turn up))\b", re.I)

COMMA_PER_100 = 1.05

# DATE FORM (maintainer rule, 2026-08-05). "rn ur saying dates like '10 August'
# the normal way to say it is August 10th." Month before day, always. The
# ordinal form is the bare one; with a year the house writes "August 27, 2026",
# which is the standard American form and is what the record's own documents
# print. Day-then-month ("27 August") is the form being banned.
MONTHS = ("January February March April May June July August September "
          "October November December").split()
DAY_FIRST = re.compile(
    r"\b([0-9]{1,2})(?:st|nd|rd|th)?\s+(" + "|".join(MONTHS) + r")\b", re.I)
BARE_CARDINAL = re.compile(
    r"\b(" + "|".join(MONTHS) + r")\s+([0-9]{1,2})\b(?!\s*(?:st|nd|rd|th|,\s*[0-9]{4}|\s+[0-9]{4}))",
    re.I)

REPO = Path(__file__).resolve().parent.parent
BRAND_DEFAULT = REPO / "config" / "brand.yaml"

# THE COPY FIELDS A READER ACTUALLY SEES (2026-08-08). Scope is deliberately
# narrow and deliberately explicit rather than "every string in the file":
#
#   document_title     set on upload, rendered under the deck on LinkedIn
#   post_copy          the caption itself (already gated via caption.txt; kept
#                      here so a copy.json that drifts from caption.txt is
#                      still checked)
#   deck_summary_line  a line of the caption
#   first_comment      the sources block, pasted under the post. THE DEFECT.
#   slides[].*         kicker, headline and any label strings, which are set
#                      in type on the artwork
#
# NOT in scope, and this is the reason: `editor_notes_for_email`, `aftercare`
# and `caption_meta` are addressed to the maintainer in the dated draft, never
# to a reader, and `aftercare` legitimately carries clock forms ("8 to 11 a.m.")
# and process prose. Gating a private note on public house style would train the
# machine to work around the gate, which is worse than the gate not existing.
COPY_READER_FIELDS = ("document_title", "post_copy", "deck_summary_line",
                      "first_comment")
COPY_SLIDE_SKIP = {"n", "claim_ids", "claim_id", "note", "beat", "words",
                   "lines", "breather"}
# A citation stamp is allowed to be ISO and a URL is allowed to be anything.
# DATE_FORMS never matches an ISO date, but a URL path like /2026/08/05/ and a
# query string are stripped first so no rule can ever fire inside a link.
_URLISH_STRIP = re.compile(r"https?://\S+|www\.\S+")


def load_banned_phrases(path=None):
    """Read brand.yaml's banned_phrases. Returns (phrases, error_or_None).

    Parsed with a 4-line reader rather than an import so the gate has no
    dependency of its own: the block is a flat list of quoted scalars under
    'banned_phrases:' and has been for the life of the file.
    """
    p = Path(path) if path else BRAND_DEFAULT
    try:
        raw = p.read_text()
    except OSError as e:
        return [], "cannot read %s (%s)" % (p, e.__class__.__name__)
    m = re.search(r"(?m)^(\s*)banned_phrases:\s*$", raw)
    if not m:
        return [], "%s has no banned_phrases: block" % p
    indent = len(m.group(1))
    out = []
    for line in raw[m.end():].splitlines():
        if not line.strip():
            continue
        cur = len(line) - len(line.lstrip())
        if cur <= indent and not line.lstrip().startswith("-"):
            break
        item = re.match(r"\s*-\s*(.+?)\s*$", line)
        if not item:
            break
        out.append(item.group(1).strip().strip('"').strip("'"))
    if not out:
        return [], "%s: banned_phrases is empty" % p
    return out, None


def _ordinal(d):
    n = int(d)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


# OWNER RULES 2026-08-06. Two style fixes rather than bans, so each one names
# the replacement in its failure. Both are exempt inside a straight-quoted
# verbatim passage, on the same reasoning as the phrase list: a source is
# allowed to write however it wrote.
#
# CANNOT. "can't" is how the voice speaks. "cannot" is stiffer and reads
# written rather than said.
CANNOT_RE = re.compile(r"\bcannot\b", re.I)

# AND / BUT AS AN OPENER. A sentence that opens on a conjunction is leaning on
# the one before it. Matched only at a real sentence start: the top of the
# text, after terminal punctuation and a space, or at the head of a line. A
# decimal cannot trip it because "3.5 And" has no space after the period, and
# the trailing boundary means Andrew and Butler are untouched.
OPENER_RE = re.compile(r"(?:\A|(?<=[.!?])\s+|\n\s*)(And|But)\b")


# THE CONTRAST REFRAME. The Economist's 2026 comparison of its own articles
# against ChatGPT, Claude, Gemini and Grok named this the giveaway structure:
# "It's not about X, it's about Y." It manufactures a sense of insight without
# supplying one, which is exactly the move a publication built on verified
# figures cannot afford. Matched only in its tight form, one subject pronoun
# negated and then restated across a comma, so an ordinary sentence that
# happens to carry "not" is untouched.
_SUBJ = r"(?:it|this|that)"
CONTRAST_RE = re.compile(
    rf"\b{_SUBJ}(?:'s| is)\s+not\s+[^.!?;]{{2,70}},\s*{_SUBJ}(?:'s| is)\b"
    rf"|\b{_SUBJ}\s+isn't\s+[^.!?;]{{2,70}},\s*{_SUBJ}(?:'s| is)\b",
    re.I)


def quoted_spans(t):
    """[(start, end)] of straight-double-quoted passages. An odd number of
    quotes means the text is not reliably quotable, so nothing is exempt."""
    if t.count('"') % 2:
        return []
    return [(m.start(), m.end()) for m in re.finditer(r'"[^"]*"', t)]


def lint(text, ledger_entries=None, deck_summary=None, brand_phrases=None):
    fails, warns = [], []
    t = text.rstrip("\n")
    lines = t.split("\n")
    nonempty = [l for l in lines if l.strip()]

    # hook
    hook = nonempty[0].strip() if nonempty else ""
    if not hook:
        fails.append("HOOK: empty first line")
    elif len(hook) > FOLD:
        fails.append(f"HOOK: first line {len(hook)} chars > {FOLD} mobile fold")
    if hook.endswith("?"):
        warns.append("HOOK: opens with a question; declarative openers test better")

    # length
    n = len(t)
    if n > HARD_MAX:
        fails.append(f"LENGTH: {n} > {HARD_MAX} LinkedIn cap")
    elif not (LO <= n <= HI):
        fails.append(f"LENGTH: {n} chars outside {LO}-{HI} carousel band")

    # hashtags: exactly 3, all in the trailing block
    tags = re.findall(r"(?<!\w)#\w+", t)
    if len(tags) != HASHTAGS_EXACTLY:
        fails.append(f"HASHTAGS: {len(tags)} found, need exactly {HASHTAGS_EXACTLY}")
    if tags:
        last_line = nonempty[-1]
        if not all(w.startswith("#") for w in last_line.split()):
            fails.append("HASHTAGS: final line must be only the hashtags")
        body_wo_last = "\n".join(nonempty[:-1])
        if re.findall(r"(?<!\w)#\w+", body_wo_last):
            fails.append("HASHTAGS: hashtags found mid-copy; all must be in the tail line")

    # links
    if URLISH.search(t):
        fails.append("LINKS: URL-like string in body (sources go in first comment)")

    # Sources and credits (music, audio, any production credit) belong ONLY
    # in the paste-ready comment blocks, never in the post (maintainer rule,
    # 2026-07-21: a delivered draft carried sources AND music credits in the
    # post above the hashtags as well as in their own sections).
    # Two shapes: a sources header ("Sources...", "Sources for this deck") and a
    # credit line ("Music, X", "Audio by Y", "Credits..."). Media words need the
    # stronger by/courtesy/credit signal so story sentences like "Sound in Cook
    # Inlet has doubled" never false-positive.
    if re.search(r"(?im)^\s*(sources?|credits?)\b\s*($|[:,]|for\b|below\b|in\b)"
                 r"|^\s*(music|audio|soundtrack|sound|track)\b\s*([:,]|by\b|courtesy\b|credits?\b)", t):
        fails.append("SOURCES/CREDITS: sources or credits block in the post copy; "
                     "they go ONLY in the comment paste blocks")

    # colons are banned in the caption, ever (maintainer rule, 2026-07-21;
    # brand.yaml previously allowed them and captions kept shipping with
    # them). Clock times like 4:30 are the only pass.
    if ":" in re.sub(r"\d{1,2}:\d{2}", " ", t):
        fails.append("PUNCT: colon present (never use colons; rewrite the sentence)")

    # punctuation & characters
    for ch, name in BANNED_PUNCT.items():
        if ch in t:
            fails.append(f"PUNCT: {name} present")
    if EMOJI.search(t):
        fails.append("EMOJI: emoji present")
    if UNICODE_BOLD.search(t):
        fails.append("UNICODE: math-alphanumeric fake bold/italic present")

    # house contractions
    low_pre = t.lower()
    for bad, good in CONTRACTIONS.items():
        if re.search(r"(?<![a-z])" + bad + r"(?![a-z])", low_pre):
            fails.append("VOICE: '%s' is banned house-wide, write '%s' "
                         "(maintainer rule, 2026-07-30)" % (bad, good))

    # AI tells + banned phrases
    low = t.lower()
    for tell in AI_TELLS:
        if tell in low:
            fails.append(f"PHRASE: banned/AI-tell '{tell}'")

    # brand.yaml banned_phrases, everything the hardcoded list does not already
    # carry. Enforced outside straight-quoted verbatim passages; a quoted-only
    # occurrence is named as a warn so it is never silent (see module docstring).
    spans = quoted_spans(t)
    for phrase in (brand_phrases or []):
        p = phrase.lower().strip()
        if not p or p in AI_TELLS:
            continue
        hits = [m.start() for m in re.finditer(re.escape(p), low)]
        if not hits:
            continue
        unquoted = [i for i in hits
                    if not any(a <= i and i + len(p) <= b for a, b in spans)]
        if unquoted:
            fails.append("PHRASE: banned phrase '%s' (config/brand.yaml "
                         "banned_phrases)" % p)
        else:
            warns.append("PHRASE: banned phrase '%s' appears only inside a "
                         "straight-quoted verbatim passage, which is allowed. "
                         "Confirm it really is a quotation." % p)

    for m in CONTRAST_RE.finditer(t):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        fails.append("STYLE: the contrast reframe, %r. It manufactures insight "
                     "instead of supplying it. State the thing that is true and "
                     "stop." % m.group(0)[:60])

    # Owner rules 2026-08-06. Same quoted-passage exemption as the phrase list.
    for m in CANNOT_RE.finditer(t):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            warns.append("STYLE: 'cannot' appears only inside a straight-quoted "
                         "verbatim passage, which is allowed. Confirm it really "
                         "is a quotation.")
        else:
            fails.append("STYLE: %r, write \"can't\". The voice speaks it that "
                         "way and 'cannot' reads written rather than said."
                         % m.group(0))
    for m in OPENER_RE.finditer(t):
        if any(a <= m.start(1) and m.end(1) <= b for a, b in spans):
            continue
        fails.append("STYLE: a sentence opens on %r. A sentence that opens on a "
                     "conjunction is leaning on the one before it. Join them, or "
                     "cut the conjunction and let the sentence stand."
                     % m.group(1))

    # engagement question: last non-hashtag line ends with ?
    content_lines = [l for l in nonempty if not all(w.startswith("#") for w in l.split())]
    if content_lines and not content_lines[-1].strip().endswith("?"):
        fails.append("CLOSE: final content line must be an engagement question ending with ?")

    # DATE FORM. Hard fail, same reasoning as the house-wide banned-word table: a style rule
    # nobody checks drifts back within a few runs.
    for rx, what, fix in DATE_FORMS:
        mm = rx.search(text)
        if mm:
            fails.append(f"DATE: '{mm.group(0)}' is the {what} form - {fix} "
                         f"(owner rule 2026-08-05). ISO is still right for a citation stamp, "
                         f"but this is a sentence.")
            break

    # COMMA DISCIPLINE, measured on the body with the hashtag tail excluded, which is how
    # the 6.88 baseline was measured so the ceiling and the measurement agree.
    body_only = re.sub(r"(?m)^\s*#\S+.*$", "", text)
    body_words = len(body_only.split())
    if body_words >= 80:
        n_commas = body_only.count(",")
        per100 = 100.0 * n_commas / body_words
        if per100 > COMMA_PER_100W:
            allowed = int(COMMA_PER_100W * body_words / 100)
            fails.append(f"COMMAS: {n_commas} commas in {body_words} words is {per100:.2f} per 100, "
                         f"over the {COMMA_PER_100W} ceiling (owner rule 2026-08-05, ten percent "
                         f"below this deck's shipped mean of 6.88). Cut at least "
                         f"{max(1, n_commas - allowed)}. Split the sentence at the comma rather "
                         f"than deleting the comma.")

    # variety engine: banned furniture, the connective tissue that made every
    # caption read like a mail merge (9 of the first 14 runs used it). The
    # old SUMMARY warn that ENCOURAGED a deck-pointer line is retired.
    for phrase in ("deck walks through", "slides walk through", "walks you through",
                   "deck walks you", "this deck walks", "the deck covers"):
        if phrase in low:
            fails.append(f"FURNITURE: banned template phrase '{phrase}' "
                         "(see knowledge/CAPTION_CRAFT.md)")
    if re.search(r"(?i)\bthese \d+ slides\b", t):
        fails.append("FURNITURE: 'these N slides' as connective tissue "
                     "(see knowledge/CAPTION_CRAFT.md)")

    # variety engine: the opening may not repeat any recent run's opening
    if ledger_entries:
        first4 = " ".join(re.findall(r"[a-z0-9']+", low)[:4])
        for e in ledger_entries[-12:]:
            prev4 = " ".join(re.findall(r"[a-z0-9']+", str(e.get("first_words", "")).lower())[:4])
            if first4 and first4 == prev4:
                fails.append(f"VARIETY: first words repeat the {e.get('run_date')} caption "
                             f"('{first4}...'); open differently")
                break

    # DECK SUMMARY LINE. brand.yaml sets deck_summary_line: true and
    # CAROUSEL_CRAFT gives the reason: a LinkedIn document post has NO alt text
    # at all, so for a screen-reader user the caption is the entire deck. The
    # rule lapsed silently for three consecutive runs (2026-07-26, 07-29,
    # 07-30) because nothing enforced it and the scorer could only dock for it
    # afterwards. The room now has to name the line and the line has to be in
    # the caption, which is mechanically checkable; whether it is any GOOD stays
    # with the caption-critic, per the house split of geometric checks from
    # semantic ones.
    def _norm(x):
        return re.sub(r"[^a-z0-9]+", "", x.lower())

    if deck_summary is None:
        fails.append("DECK SUMMARY: no --deck-summary given. brand.yaml requires a "
                     "1 to 2 line plain summary of what the deck covers, because a "
                     "LinkedIn document has no alt text and the caption is all a "
                     "screen reader gets. Write one, then pass it with "
                     "--deck-summary \"<the exact line>\"")
    else:
        ds = deck_summary.strip()
        if len(ds) < 40:
            fails.append("DECK SUMMARY: %d chars is too short to describe a deck; "
                         "write a real sentence" % len(ds))
        elif _norm(ds) not in _norm(t):
            fails.append("DECK SUMMARY: the declared line is not present in the "
                         "caption verbatim, so the caption does not actually carry it")
        elif content_lines and _norm(ds) == _norm(content_lines[-1]):
            fails.append("DECK SUMMARY: the declared line IS the closing question; "
                         "it has to be its own line doing its own work")
        elif _norm(ds) == _norm(hook):
            fails.append("DECK SUMMARY: the declared line IS the hook; "
                         "it has to be its own line doing its own work")

    # The hashtag line is not prose, so it is excluded from both checks below.
    # This is the same slice the 2026-08-05 baseline was measured on.
    body = "\n".join(l for l in lines if not l.strip().startswith("#"))

    # --- FIRST PERSON ------------------------------------------------------
    # A source quoting itself is quotable, same carve-out the banned-phrase
    # check already uses. The studio speaking as itself is not.
    spans = quoted_spans(body)
    for m in FIRST_PERSON.finditer(body):
        if any(a <= m.start() < b for a, b in spans):
            continue
        w = m.group(1)
        if len(w) > 1 and w.isupper():      # "the US Air Force", not "us"
            continue
        fails.append("FIRST PERSON: '%s' in the caption. The page describes the "
                     "world, it does not narrate itself. Rewrite the sentence "
                     "about its subject." % m.group(1))
    for m in SELF_NARRATION.finditer(body):
        if any(a <= m.start() < b for a, b in spans):
            continue
        fails.append("FIRST PERSON: '%s' is the studio narrating its own work "
                     "with the pronoun removed. Say what is true of the record, "
                     "not what the search turned up." % m.group(1))

    # --- THE HOOK STANDS ALONE ---------------------------------------------
    first_sentence = re.split(r"(?<=[.?!])\s", hook)[0] if hook else ""
    if HOOK_ADDRESS.match(first_sentence):
        fails.append("HOOK: opens as a letter addressed to someone who is not "
                     "the reader. The audience is Alaskans in a feed, not the "
                     "body being written to. Open on the claim instead.")
    if HOOK_PAIRED.match(first_sentence) and re.search(r"\bthe other\b", hook, re.I):
        fails.append("HOOK: 'One ... the other' with no antecedent. A stranger "
                     "reading sentence one cold has nothing to attach it to. "
                     "Name the two things.")
    if HOOK_BARE_PRONOUN.match(first_sentence):
        fails.append("HOOK: opens on a bare pronoun with nothing before it to "
                     "refer to. Say the noun.")

    # --- SENTENCE-OPENING CONJUNCTIONS -------------------------------------
    for m in SENTENCE_START_CONJ.finditer(body):
        if any(a <= m.start() < b for a, b in spans):
            continue
        fails.append("CONJUNCTION: a sentence opens with '%s'. Join it to the "
                     "sentence before with a comma, or drop the word."
                     % m.group(1))

    # --- DATE FORM ---------------------------------------------------------
    for m in DAY_FIRST.finditer(body):
        day, month = m.group(1), m.group(2)
        fails.append("DATE FORM: '%s' is day before month; the house writes "
                     "'%s %s' (month first, ordinal when the year is absent)"
                     % (m.group(0), month.capitalize(), _ordinal(day)))
    for m in BARE_CARDINAL.finditer(body):
        fails.append("DATE FORM: '%s' needs the ordinal when no year follows; "
                     "write '%s %s'"
                     % (m.group(0), m.group(1).capitalize(), _ordinal(m.group(2))))

    # --- COMMA BUDGET ------------------------------------------------------
    commas = body.count(",")
    body_chars = len(body)
    density = (commas / body_chars * 100) if body_chars else 0.0
    allowed = int(COMMA_PER_100 * body_chars / 100)
    if commas > allowed:
        fails.append("COMMAS: %d in %d chars is %.2f per 100, over the %.2f "
                     "budget. Cut %d, or split a sentence."
                     % (commas, body_chars, density, COMMA_PER_100,
                        commas - allowed))

    return {"chars": n, "hook": hook, "hook_len": len(hook),
            "commas": commas, "comma_per_100": round(density, 2),
            "comma_budget": COMMA_PER_100,
            "hashtags": tags, "deck_summary": deck_summary,
            "brand_phrases_loaded": len(brand_phrases or []),
            "fails": fails, "warns": warns,
            "verdict": "FAIL" if fails else "PASS"}


def copy_prose(copy):
    """Yield (field_path, string) for every reader-facing prose string in a
    copy.json. See COPY_READER_FIELDS for the scope and the exclusions.

    A SLIDE IS NOT ALWAYS A DICT (2026-08-16). This walker skipped any slide
    whose value was a plain LIST OF STRINGS, which is the shape the copy room
    has been writing, so `slides` contributed nothing at all: run No.35 reported
    copy_fields_checked 4, the four caption-side prose fields, and every string
    set in type on the artwork went unread by the date table and the banned
    phrase pass alike. The gate looked green because it was looking at the
    caption. Recurse instead: a slide value may be a dict of fields, a list of
    strings, or a nested list, and every leaf string is on-slide copy.
    """
    out = []
    for k in COPY_READER_FIELDS:
        v = copy.get(k)
        if isinstance(v, str) and v.strip():
            out.append((k, v))
    slides = copy.get("slides")
    items = []
    if isinstance(slides, list):
        items = [("slides[%d]" % i, s) for i, s in enumerate(slides)]
    elif isinstance(slides, dict):
        items = sorted(slides.items())

    def walk(node, path):
        if isinstance(node, str):
            if re.search(r"[A-Za-z]", node):
                out.append((path, node))
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, "%s[%d]" % (path, i))
        elif isinstance(node, dict):
            for k, v in node.items():
                if k in COPY_SLIDE_SKIP:
                    continue
                walk(v, "%s.%s" % (path, k))

    for key, s in items:
        walk(s, key)
    return out


def check_copy_phrases(copy, brand_phrases):
    """Run brand.yaml's banned_phrases over copy.json's reader-facing prose.

    THE SLIDES WERE NEVER SCANNED (2026-08-15). The phrase gate had only ever
    read the CAPTION, so a banned phrase set in a slide's own body shipped past
    every gate in the run and was caught by the scorer, one phase from the
    email. This run lost a hard fail to it: slide 02 printed 'a coordinated,
    actionable plan' in the deck's unquoted voice, and 'actionable' is item 46
    of the list. Same rule and same exemption as the caption, applied to the
    same fields check_copy_dates already walks. Widens an existing gate to the
    surface it was always meant to cover; adds no rule of its own.
    """
    fails = []
    for path, s in copy_prose(copy):
        low = s.lower()
        spans = quoted_spans(s)
        for phrase in (brand_phrases or []):
            p = phrase.lower().strip()
            if not p:
                continue
            for m in re.finditer(re.escape(p), low):
                i = m.start()
                if any(a <= i and i + len(p) <= b for a, b in spans):
                    continue  # a source is allowed to write however it wrote
                fails.append("PHRASE: banned phrase '%s' in copy.json %s "
                             "(config/brand.yaml banned_phrases)" % (p, path))
                break
    return fails


def check_slide_openers(copy):
    """brand.yaml's on-slide opener rule, run on on-slide text (2026-08-16).

    "No slide string opens with 'And' or 'But'" is a maintainer rule of
    2026-08-05, written twice in config/brand.yaml (visual.on_slide_text_rules
    and brand.voice.dont), and it had no code anywhere. The caption has carried
    the same rule as a hard fail since the beginning, via SENTENCE_START_CONJ
    over the caption body, and slides were simply never asked.

    Run No.35 shipped slide 06's kicker as "AND FOURTEEN MORE" past every green
    gate. The scorer caught it by reading the pixels and capped a raw 8.52 at
    6.90, which is the most expensive machine gap in that run by a wide margin.

    SCOPE, decided deliberately and not by default. The rule as written is
    about a slide string OPENING on the conjunction, so only the head of each
    on-slide string is tested, not every sentence inside it: a body line that
    runs "...decisions, and fourteen more" is ordinary English and is left
    alone. Editor-only fields stay out of scope exactly as they are for the
    phrase and date passes, because copy_prose is the shared scope and
    editor_notes_for_email, aftercare and caption_meta are not in it. A quoted
    source may open however it wrote, same exemption as everywhere else.
    """
    fails = []
    for path, s in copy_prose(copy):
        if path in COPY_READER_FIELDS:
            continue          # caption-side prose; the caption body gate owns it
        t = s.lstrip().lstrip('"\'(')
        m = re.match(r"(?i)(and|but)\b", t)
        if not m:
            continue
        if quoted_spans(s) and any(a == 0 for a, b in quoted_spans(s)):
            continue          # the whole string is a quotation
        fails.append(
            "OPENER (copy.json %s): the slide string opens with '%s'. No slide "
            "string opens with 'And' or 'But' (maintainer rule 2026-08-05, "
            "config/brand.yaml visual.on_slide_text_rules and brand.voice.dont). "
            "A slide that opens on a conjunction is leaning on the slide before "
            "it, and a reader who lands mid-deck has nothing to lean on. Say the "
            "noun: '%s'" % (path, m.group(1), s[:48]))
    return fails


def check_copy_dates(copy):
    """Run the house DATE_FORMS table over copy.json's reader-facing prose.

    Widens an existing gate to the surfaces it was always supposed to cover;
    adds no rule of its own. Returns a list of failure strings. Every hit is
    reported, not just the first: run No.29's first_comment carried six.
    """
    fails = []
    for path, raw in copy_prose(copy):
        text = _URLISH_STRIP.sub(" ", raw)
        for rx, what, fix in DATE_FORMS:
            for m in rx.finditer(text):
                fails.append(
                    "DATE (copy.json %s): '%s' is the %s form - %s (owner rule "
                    "2026-08-05). ISO is still right for a citation stamp, but "
                    "this is prose a reader sees." % (path, m.group(0), what, fix))
    return fails


def _move_key(v):
    """Normalise a declared move so 'NEW:X', 'NEW: x' and 'new x' are one thing."""
    s = re.sub(r"^new\b[:\s]*", "", (v or "").strip().lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def burn_table(entries):
    """THE BURN LIST, PUT IN FRONT OF THE ASSIGNMENT (2026-08-14).

    Run No.33's caption-critic killed candidate A because its price close had
    been burned on 2026-07-30, restated on 2026-08-06, and was phrased as the
    2026-07-24 close with the nouns swapped. That is the FIFTH run in which a
    director was sent to write against a burn the ledger already recorded. The
    information was never missing; it lives in these entries and in their free
    text notes, and the assignment brief was written without reading it.

    So this prints it, deterministically, in the shape the brief needs, and
    Phase 6 step 1 now runs it before picking the two assignments. It states no
    opinion and enforces nothing. The enforcement lives in caption_meta_hits().
    """
    out = []
    n = len(entries)
    last = entries[-1]["run_date"] if n else "no entries"
    out.append("BURN LIST from the caption ledger, %d entries through %s." % (n, last))
    out.append("Read this BEFORE picking the two assignments (Phase 6 step 1).")
    out.append("")
    out.append("FORBIDDEN RIGHT NOW, by the ledger's own divergence windows")
    for field, win in (("opening_move", 6), ("structure", 3), ("closing_move", 1)):
        used = []
        for e in reversed(entries[-win:]):
            v = e.get(field)
            if v and v not in used:
                used.append("%s (%s)" % (v, e["run_date"]))
        out.append("  %-13s differs from the last %d, so not  %s"
                   % (field + ",", win, "  /  ".join(used) or "nothing on record"))
    fw = []
    for e in reversed(entries[-12:]):
        w = (e.get("first_8_words") or e.get("first_words") or "").split()
        if w:
            fw.append(" ".join(w[:4]))
    out.append("  %-13s differ from the last 12, so not  %s"
               % ("first 4 words,", "  /  ".join(fw) or "nothing on record"))
    out.append("")
    out.append("EVERY CLOSING MOVE EVER SHIPPED, most recently used first")
    seen = {}
    for e in entries:
        k = _move_key(e.get("closing_move"))
        if not k:
            continue
        seen.setdefault(k, {"label": e.get("closing_move"), "dates": []})
        seen[k]["dates"].append(e["run_date"])
    for k, v in sorted(seen.items(), key=lambda kv: kv[1]["dates"][-1], reverse=True):
        out.append("  %-24s %d use%s, last %s%s"
                   % (v["label"][:24], len(v["dates"]),
                      "" if len(v["dates"]) == 1 else "s", v["dates"][-1],
                      ", also " + " ".join(v["dates"][:-1][-4:])
                      if len(v["dates"]) > 1 else ""))
    out.append("")
    out.append("A close named NEW: has to BE new. Every name above is spent, "
               "whether or not it was invented as a NEW: one.")
    said = [(e["run_date"], " ".join((e.get("note") or e.get("notes") or "").split()))
            for e in entries]
    said = [(d, t) for d, t in said if "burn" in t.lower()]
    if said:
        out.append("")
        out.append("NOTES THAT SAY BURNED, verbatim from the ledger")
        for d, t in said[-6:]:
            i = t.lower().find("burn")
            out.append("  %s  ...%s..." % (d, t[max(0, i - 120):i + 120]))
    return out


def caption_meta_hits(meta, entries, run_date):
    """GRADE THE DECLARED MOVES AGAINST THE LEDGER (2026-08-14).

    The ledger's `_spec` has always written the divergence windows down and
    nothing has ever read them, so for 33 runs the only thing standing between
    a repeated move and the feed was somebody remembering. Two checks, both
    arithmetic on values the room itself declared in copy.json.

    The second one is the one run No.33 needed. A closing move labelled NEW: is
    a CLAIM, in the same family as a declared maxLines or a printed dimension,
    and No.33 shipped NEW:SUFFICIENCY TEST nine days after 2026-08-05 shipped
    NEW:SUFFICIENCY TEST. Nobody noticed, because a novel-move claim was the one
    kind of declaration here with nothing behind it.

    Today's own entry is excluded by run_date, so re-running after ship is safe.
    """
    hits = []
    if not isinstance(meta, dict):
        return hits
    prior = [e for e in entries if e.get("run_date") != run_date]
    for field, win in (("opening_move", 6), ("structure", 3), ("closing_move", 1)):
        v = meta.get(field)
        if not v:
            hits.append("VARIETY: copy.json caption_meta declares no %s, so the "
                        "divergence window for it can't be checked" % field)
            continue
        for e in prior[-win:]:
            if _move_key(e.get(field)) == _move_key(v):
                hits.append("VARIETY: %s %r was used on %s and the ledger's own "
                            "rule is that it differs from the last %d entries"
                            % (field, v, e["run_date"], win))
                break
    close = meta.get("closing_move") or ""
    if re.match(r"^\s*new\b", close, re.I):
        k = _move_key(close)
        earlier = [e["run_date"] for e in prior if _move_key(e.get("closing_move")) == k]
        if earlier:
            hits.append("VARIETY: the closing move is declared NEW (%r) and the "
                        "same move already shipped on %s, so the claim is false. "
                        "A NEW: name is a claim of novelty and this is the run "
                        "No.33 defect, NEW:SUFFICIENCY TEST shipped twice nine "
                        "days apart with nothing checking it"
                        % (close, ", ".join(earlier)))
    return hits


def main():
    args = [a for a in sys.argv[1:]]
    if "--burns" in args:
        i = args.index("--burns")
        lp = Path(args[i + 1]) if len(args) > i + 1 else Path("ledger/captions.json")
        if not lp.exists():
            print("FAIL: --burns %s not found" % lp)
            sys.exit(1)
        for line in burn_table(json.loads(lp.read_text()).get("entries", [])):
            print(line)
        sys.exit(0)
    ledger_entries = None
    ledger_missing = None
    deck_summary = None
    brand_path = None
    if "--brand" in args:
        i = args.index("--brand")
        brand_path = args[i + 1]
        del args[i:i + 2]
    copy_path = None
    if "--copy" in args:
        i = args.index("--copy")
        copy_path = Path(args[i + 1])
        del args[i:i + 2]
    if "--deck-summary" in args:
        i = args.index("--deck-summary")
        deck_summary = args[i + 1]
        del args[i:i + 2]
    if "--ledger" in args:
        i = args.index("--ledger")
        ledger_path = Path(args[i + 1])
        del args[i:i + 2]
        if ledger_path.exists():
            ledger_entries = json.loads(ledger_path.read_text()).get("entries", [])
        else:
            # Explicitly asked to check variety against a ledger that is not
            # there (a typo, or the documented relative path 'ledger/captions.json'
            # run from any cwd but the repo root). Silently leaving the variety
            # engine off and writing PASS is how a repeated caption opener ships.
            # A check that cannot look is a FAIL, recorded in the report so the
            # ship gate sees it too, not a stale pass.
            ledger_missing = str(ledger_path)
    if args:
        src = Path(args[0])
        text = src.read_text()
        out = src.parent / "caption_report.json"
        # A CAPTION NEVER COLLIDES WITH ITSELF (2026-08-15). The ship order
        # appends this run's entry to ledger/captions.json and only then runs
        # the completion gate, so from that point on the variety engine was
        # comparing the caption against its OWN row and hard-failing every run
        # on "first words repeat the <today> caption". It is a tautology, not a
        # repeat, and it fired on the one gate the ship cannot proceed past.
        # Dropping same-date rows loosens nothing: one run writes one caption,
        # so there is no honest way for a real repeat to carry today's date.
        # Keyed off the run directory's name, which is where the date lives.
        if ledger_entries is not None:
            run_date = src.parent.name
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", run_date):
                ledger_entries = [e for e in ledger_entries
                                  if e.get("run_date") != run_date]
    else:
        text = sys.stdin.read()
        out = Path("caption_report.json")
    brand_phrases, brand_err = load_banned_phrases(brand_path)
    rep = lint(text, ledger_entries, deck_summary, brand_phrases)
    if brand_err:
        # Same rule as the ledger below: a check that could not look is not a
        # pass. brand.yaml is committed, so this only fires on a real breakage.
        rep["fails"].append("BRAND: %s, so the banned_phrases half of the phrase "
                            "gate could not run" % brand_err)
        rep["verdict"] = "FAIL"
    if ledger_missing:
        rep["fails"].append("VARIETY: --ledger %s not found, the caption variety "
                            "check could not run, so this is not a pass" % ledger_missing)
        rep["verdict"] = "FAIL"
    if copy_path is not None:
        # Same rule as --ledger and --brand above: a check that was asked for
        # and could not look is a FAIL, never a silent pass.
        try:
            copy_obj = json.loads(copy_path.read_text())
        except (OSError, ValueError) as e:
            rep["fails"].append("COPY: --copy %s could not be read (%s), so the "
                                "house date form was checked on the caption only"
                                % (copy_path, e.__class__.__name__))
            rep["verdict"] = "FAIL"
        else:
            hits = check_copy_dates(copy_obj)
            hits.extend(check_copy_phrases(copy_obj, brand_phrases))
            hits.extend(check_slide_openers(copy_obj))
            rep["copy_fields_checked"] = len(copy_prose(copy_obj))
            # THE DECLARED MOVES, GRADED (2026-08-14). copy.json carries the
            # room's own caption_meta and the ledger carries the windows those
            # moves have to clear; nothing had ever put the two together. Only
            # runs when both --copy and --ledger are given, which is what the
            # Phase 6 ship-gate invocation passes.
            if ledger_entries is not None:
                hits.extend(caption_meta_hits(copy_obj.get("caption_meta"),
                                              ledger_entries,
                                              copy_obj.get("run_date")))
            rep["fails"].extend(hits)
            if hits:
                rep["verdict"] = "FAIL"
    out.write_text(json.dumps(rep, indent=2))
    for f in rep["fails"]:
        print("FAIL:", f)
    for w in rep["warns"]:
        print("warn:", w)
    print(f"verdict: {rep['verdict']} ({rep['chars']} chars, hook {rep['hook_len']}) -> {out}")
    sys.exit(1 if rep["fails"] else 0)


if __name__ == "__main__":
    main()
