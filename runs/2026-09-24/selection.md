# SELECTION — Carousel No. 67 — September 24th

## The pick

**XPRIZE Wildfire's autonomous track was examined in Alaska, and the record of the answer is
thinner than the purse.** On September 23rd XPRIZE paid $4.55 million across two tracks of its
$11 million wildfire competition (S1-C01 to S1-C03). The Autonomous Wildfire Response track was
decided by two weeks of June finals in rural Nenana, from the Nenana Municipal Airport where
ACUASI ran flight operations and the airspace (S1-C15 to S1-C17). The task was to detect and
completely suppress a high-risk fire within 10 minutes of ignition across 1,000 km2, leaving decoy
fires untouched (S1-C12 to S1-C14), over an 8 hour watch with up to three controlled fires
(S1-C20). Anduril took first and $1.2 million plus the $1 million Lockheed Martin bonus, Dryad
second and $800,000, AURA Foresight third and $500,000 (S1-C08 to S1-C11).

## The angle, and why it is the honest one

**Alaska was the exam room. On the record, it is not yet the customer, and the exam's own
headline question is still open.**

Three things the record says, and one thing it does not:
1. The ONLY explicit statement that anyone met a 10 minute gate is XPRIZE's line that AURA met the
   critical 10 minute DETECTION gate (S1-C31). Dryad says its network detected and verified the
   target fire in 12 minutes or less (S1-C28), which is longer than 10, and that its drone hit the
   fire with suppressant (S1-C30), not that it put the fire out. XPRIZE's release does not state
   that any team fully suppressed a fire inside 10 minutes, and Lockheed Martin's Adam Broecker says
   "the final prize remains on the horizon" (S1-C34). The deck says exactly that and never "the
   grand prize went unclaimed", which no page says.
2. The next step is a 12 to 15 month Impact Phase (S1-C41). Dryad's pilots are planned for 2027 with
   no location given (S1-C42).
3. The only Alaska institutions on any page are UAF and ACUASI (S1-C16, S1-C17, S1-C39). No Alaska
   fire agency appears anywhere in the record. The deck states that as the record's silence, not as
   a finding that Alaska was excluded.
4. Scale, the drawable argument. Alaska's 2025 season burned an estimated 1.68 million acres,
   according to XPRIZE (S1-C37), which is about 6,800 km2, or the 1,000 km2 test area nearly seven
   times over. That is arithmetic on two claims and goes in aggregates.json as a ratio.

The position the deck takes: a proving ground is not the same as a buyer, and the state whose
wilderness set the exam has a reason to ask for a seat at what comes next. The closing ask is a
debatable question, not a verdict.

Why it wins on the four criteria:
- (1) Concrete Alaska impact: the test was held on Alaska ground by Alaska's drone center, in the
  state whose 2025 season is the reason XPRIZE gave for coming (S1-C37, S1-C38).
- (2) Visual potential, the strongest of the day: REAL terrain and hydrography around Nenana are
  already built (assets/geo/nenana-dem.*, nenana-rivers.geo.json), and a 1,000 km2 square at true
  scale covers most of the Tanana Flats in frame. Time (a 10 minute clock against 12 minutes),
  quantity (prize purses), and place (Nenana, the Totchaket corridor, S1-C19) all draw.
- (3) Tangibility: a dated award, named teams, named machines (Lattice, Silvanet, Silvaguard), a
  task with numbers.
- (4) An Alaskan would send it to a coworker: the headline national story everyone will read as
  "drones fight fires", told from the place it was graded.

Freshness: announced the day before this run. No Alaska newsroom has covered the awards yet
(S1-C43), so this is the first Alaska reading of the result.

## Dedupe gate

`dedupe_check.py` flagged No.62 (September 18th, "Out of Nenana and Back, With the Finding
Pending") as LIKELY DUPLICATE on two shared entities, ACUASI and Nenana, at token jaccard 0.022.
Read in full. No.62 is ACUASI's August 19th blood-sample transport flight for the International
Testing Agency. This deck is a different event (June wildfire finals), a different actor set
(XPRIZE, Anduril, Dryad, AURA, Lockheed Martin), a different decision (prize awards on September
23rd), and a different question (whether a test site becomes a customer). Not a duplicate. The LANE
is real, though: the same airport six days apart, and a regular reader will notice. The deck does
not hide it; ACUASI's role is named plainly, and the Nenana airport is the literal anchor. Soft
overlaps No.45 and No.59 (ACUASI only) and No.41 (the word fire) were read and are unrelated.
The fisheries and data center wells are untouched, which answers No.47's scorer note about lanes.

## Runner-up

**The four governor candidates on data centers, and SB 250 as the bill the next governor
inherits** (S2-C01 to S2-C09). Strong quotes and a real primary (the bill text and its BASIS
record), but the candidate positions rest on one reporter's story in three republications, and the
data center lane has carried No.47, No.50, No.54, No.58, No.65 in thirty days. Held; it becomes
stronger nearer November 3rd. Third: the Air Force enhanced use lease (S3), whose in-window content
is reaction coverage to a solicitation No.47 already drew.

## Directors room lenses (rotated)

Yesterday ran cartographer, editorial-essayist, systems-illustrator. Today:
- **cinematographer**: one continuous real landscape, a camera that moves across the deck.
- **data-journalist**: let the record's numbers (purses, minutes, square kilometres) carry it.
- **field-documentarian**: the June two weeks at the Nenana airport as observed fact.
