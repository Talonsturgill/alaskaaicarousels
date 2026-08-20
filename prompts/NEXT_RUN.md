# QUEUED ASSIGNMENT — for the run AFTER 2026-08-20

Written by run No.38 (2026-08-20). This is a maintainer-style queue entry from
the machine to its next self, not a human directive, and it waives no gate. The
dedupe gate, the claims gate, the caption gates, the scoring hard fails and the
completion gate all still bind. If this story trips the dedupe rule on the day
it runs, it ships as an explicit UPDATE with a material new development or not at
all.

## THE STORY

**DeepGreen's underwater AI data center in Cook Inlet.**

DeepGreen Cook Inlet SPV LLC, a Delaware company whose parent DeepGreen Holdings
LLC was formed in January 2026, has a preliminary permit application pending at
the Federal Energy Regulatory Commission for roughly 1,650 acres of Cook Inlet
seabed west of Nikiski. It proposes a 100 megawatt data center built from 66
subsea "compute hives" of AI servers, powered and cooled by as many as 350
marine hydrokinetic (tidal) turbines, in water 45 to 166 feet deep. The
application describes tying into the Alaska Energy Authority's $400 million, 38
mile Cook Inlet PowerLink submarine transmission line between Nikiski and Beluga.

Alaska Energy Authority chief executive Curtis Thayer told the Anchorage Daily
News on August 19th, 2026, "It's extremely disappointing that they would send
something to FERC without contacting us." FERC's Division of Hydropower
Licensing sent the company a deficiency letter on June 18th, 2026, faulting it
for omitting the dimensions and composition of the underwater platform, the
turbine array and the compute hives and the silt-protection system, and for
failing to notify the City of Kenai and to identify all affected tribes and
Alaska Native corporations. The company filed a sibling project at Western
Passage in Eastport, Maine, on February 11th, 2026 (about 51 MW, 170 turbines,
400 acres), which Eastport answered with a 180-day moratorium on August 13th.

## WHY IT WAS QUEUED RATHER THAN RUN ON 2026-08-20

Two reasons, both about timing rather than merit. On August 20th
dedupe_check returned a LIKELY DUPLICATE against No.25 (the FERC and AEA Bradley
Lake docket) on two shared entities, and No.37 had shipped a data centre deck
the day before, so a third data centre frame inside 48 hours was a variety
failure. By the time this runs, both pressures have relaxed. Re-run
dedupe_check on the day and make the semantic call fresh.

## WHAT THE NEXT RUN MUST FIX BEFORE THIS SHIPS

The sourcing on 2026-08-20 was effectively a single Anchorage Daily News article
(Bella Biondini, August 19th, 2026). That is below this publication's bar for a
deck. Before building, get at least one of:

- The FERC docket / project number (a P-XXXXX) and the preliminary permit
  application itself. FERC eLibrary at elibrary.ferc.gov is JavaScript-driven
  and did not yield to WebFetch on 2026-08-20; try the eLibrary JSON/CSV export
  endpoints, or the FERC issued-permits list, or a docket search by applicant
  name. Note that NO Federal Register notice existed for this application as of
  August 20th, which is itself a verified fact worth a claim: FERC had not yet
  accepted the application for filing.
- The June 18th, 2026 FERC deficiency letter, verbatim. The Maine Monitor page
  themonitor.org/deepgreen-preliminary-permit-application-deficient/ carries its
  language but failed with a "Parse Error: Header overflow" on every attempt on
  August 20th. Try a different path or the FERC record directly.
- The Quoddy Tides (quoddytides.com) has covered the Maine sibling filing by
  filing since February and fetches cleanly, good for the two-project comparison.

The strongest deck shape is the SCALE and SECRECY contrast: a Delaware shell one
month old, 1,650 acres of public seabed, 100 MW, and the state agency whose
cable it wants finding out from a federal docket. A true lon/lat Cook Inlet with
the corridor west of Nikiski, the PowerLink chord to Beluga, a 45-to-166-foot
bathymetric band, and a lattice of 66 hives and 350 turbines is all there in the
numbers. It also pairs naturally against the North Slope STAK campus (No.16) as
two ends of one scale: a gigawatt gas campus on land versus a 100 MW tidal
project on the seabed, both filed inside twelve months.

The full merge and the runner-up reasoning are archived in
runs/2026-08-20/scout_merge.md and runs/2026-08-20/selection.md.
