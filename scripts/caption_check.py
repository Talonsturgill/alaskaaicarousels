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


def main():
    args = [a for a in sys.argv[1:]]
    ledger_entries = None
    ledger_missing = None
    deck_summary = None
    brand_path = None
    if "--brand" in args:
        i = args.index("--brand")
        brand_path = args[i + 1]
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
    out.write_text(json.dumps(rep, indent=2))
    for f in rep["fails"]:
        print("FAIL:", f)
    for w in rep["warns"]:
        print("warn:", w)
    print(f"verdict: {rep['verdict']} ({rep['chars']} chars, hook {rep['hook_len']}) -> {out}")
    sys.exit(1 if rep["fails"] else 0)


if __name__ == "__main__":
    main()
