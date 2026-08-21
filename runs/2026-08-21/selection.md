# SELECTION — 2026-08-21 — Carousel No. 39

## THE DECISION

**DeepGreen Cook Inlet SPV LLC's pending FERC preliminary permit application
for a 100 megawatt subsea AI data center on 1,650 acres of Cook Inlet seabed
west of Nikiski, and the fact that no Alaskan has a way to comment on it.**

This is the story `prompts/NEXT_RUN.md` queued for this run. A queued
assignment overrides Phase 4's own story selection and waives no gate, so what
follows is the gate work, not a re-litigation of the choice.

## THE QUEUED BRIEF'S OWN BLOCKER IS CLEARED

The brief was honest that on August 20th the sourcing was effectively one
Anchorage Daily News article, and it said plainly that this is below the bar.
It named three targets. Two landed.

1. **A second independent newsroom.** The Maine Monitor (Melissa S. Razdrih,
   August 13th, 2026) reports the Alaska envelope, the Alaska turbine count and
   the Alaska deficiency letter, and it did so six days before ADN. Read in
   full. The Quoddy Tides corroborates the Maine side from February.
2. **A primary federal record, and it is the best fact of the run.** A Federal
   Register API query on the term DeepGreen, all agencies, all dates, run
   August 21st, 2026, returns zero documents, against ten or more comparable
   Cook Inlet tidal preliminary permit notices since 2006. FERC's spokesperson
   states the sequence on the record. So the application has not been accepted
   for filing, and the public comment period Alaskans would use has never
   opened.
3. **Not landed.** The FERC project number and the June 18th deficiency letter
   itself remain out of reach. elibrary.ferc.gov is JavaScript only and every
   ferc.gov path returned 403 to two separate scouts. The deck prints no P
   number for Alaska, and says so.

The third target's failure is not a hole in the deck. It is one of its facts.

## DEDUPE GATE

`python scripts/dedupe_check.py` run with the candidate's full entity and
keyword set. One LIKELY DUPLICATE and it does not survive reading.

    [LIKELY DUPLICATE] No.25 2026-08-04 (Drawn to Scale, Except the Demand)
      shared entities: alaska energy authority, federal energy regulatory
                       commission, ferc, kenai
      shared keywords: acres
      token jaccard: 0.052

Read in full. No.25 is the Alaska Energy Authority's own application to amend
the Bradley Lake license, in FERC docket P-8221-124, on which FERC opened a
comment window. Today's candidate is a private Delaware shell's preliminary
permit application, at a different place (Cook Inlet seabed west of Nikiski,
not Bradley Lake), under a different FERC procedure (a preliminary permit, not
a license amendment), for a different thing (a compute load, not hydro
capacity), with AEA as the injured party rather than the applicant, and turning
on the opposite fact (no comment window has opened, where No.25's whole subject
was one that had).

The four shared tokens are institutional nouns. Every Alaska energy story
shares them. **Not a duplicate, and not an update either, because it is not the
same decision.**

The soft overlaps on No.14 (AIDEA's Houston conveyance) and No.16 (STAK's North
Slope lease) share only the word "center". Both are terrestrial state land
leases decided by DNR. This is federal, subsea, and undecided.

One variety note that is not a dedupe question. Run No.37 shipped an Alaska
public opinion on data centers deck on August 19th, two days ago. That is close
enough to be worth naming. It is a different subject (statewide survey
sentiment against one pending federal filing), a different decider, and a
different argument, and the artwork constraints below force the two apart
visually. Proceeding.

## WHY THIS STORY, AGAINST THE FOUR CRITERIA

1. **Concrete Alaska impact.** 1,650 acres of Cook Inlet seabed, west of
   Nikiski, in water Alaskans set nets in, tied to a state owned cable rated
   for 200 MW by a project that wants 100 of them. The state energy authority
   named as the interconnection partner says it was never contacted.
2. **Visual potential, and it is unusually high.** Two seabed envelopes at true
   relative scale, 1,650 acres against 27.1, is a wordless argument. The depth
   band 45 to 166 feet is real geometry. The turbine and hive counts are
   drawable populations. And the deck's central absence, a comment window that
   has not opened, draws as an empty box in a row of filled ones.
3. **Tangibility.** A company one month old, with no website, that could not
   tell a federal agency the dimensions of its own hardware, asking for public
   seabed.
4. **Would an Alaskan send this to a coworker?** Yes, and specifically a Kenai
   Peninsula one. The comparison to Eastport is what makes it forwardable. The
   same developer, the same technology, the same filing month, and a town on
   the other coast that got to say no.

## THE THESIS

**Maine's town got a vote. Alaska's seabed got a filing nobody can answer.**

The deck is not an argument that the project is bad. It is an argument about
the ASYMMETRY OF THE RECORD. Everything Alaskans know about this comes from two
newsrooms and a company that has not published a website. What would normally
be public, a docket number and a Federal Register notice opening comment, is
not, six months in. Meanwhile the identical project on the other coast went
through a public process, shrank by about 70 percent, and was frozen for 180 days.

CORRECTED MID-RUN. This sentence said "94 percent" until the fact-checker
killed the figure and a treatment director caught the stale copy here. The 94
came from setting a 400 acre operational ENVELOPE against a 27.1 acre active
FOOTPRINT, and The Quoddy Tides reported on February 27th, 2026 that the
original Maine filing already described about 27 acres of active infrastructure
inside its 400 acre envelope (C34). The physical footprint barely moved. The
verified cuts are capacity, 51 MW to a maximum of 15 (C35), and turbines, about
170 to 16 in Phase I and 34 in Phase II (C36). Both are about 70 percent.

The honest close is not "stop it". It is that the one number Alaska has no way
to influence yet is the only one that has not moved.

## RUNNER-UP, and why it waits

**Jonathan Kreiss-Tomkins topped the August 18th primary at about 21.6 percent
as the only gubernatorial candidate calling for a statewide moratorium on all
new data centers.** Genuinely surprising, live, and the platform page is
primary. Two reasons it is not today's deck. Run No.37 shipped Alaska public
opinion on data centers two days ago and this sits close to it. And the
donation figures that make it a story, $521,812 from AI industry donors and
$372,000 from six Anthropic employees, come from one opinionated outlet's
reading of APOC filings that no scout retrieved first hand. A deck built on
that needs the filings read directly.

**Queued for a later run** once APOC is read. Not written into NEXT_RUN.md,
because the general election is in November and the story keeps.

## SECOND RUNNER-UP

NSF award 2630206 to UAF, August 19th, $50,000, explainable AI for satellite
derived nearshore bathymetry. Primary, in window, and a lovely story. Too small
alone to carry a deck, and it is best used as it is used here, as the pointed
detail that the same week a company proposed building on a seabed nobody has
mapped, the federal government paid Alaska $50,000 to figure out how to map one
from orbit.
