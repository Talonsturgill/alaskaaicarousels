// Tests for the answer checks. Run: node workers/ask/test.mjs
//
// Every control gets a green case AND a red case. A check that cannot fail
// certifies nothing, and these are the only thing standing between what a
// fired routine writes and a claim published under the site's name.

import {
  normalise, numerals, checkVerdict, checkCitations, checkNumerals,
  checkSentence, splitSentences, plainly,
} from "./checks.js";

let failures = 0;
function check(label, cond, detail = "") {
  const tag = cond ? "PASS" : "FAIL";
  if (!cond) failures++;
  console.log(`  ${tag}  ${label}${detail ? "  " + detail : ""}`);
}
function section(name) { console.log(name); }

// ---------------------------------------------------------------- normalise
//
// These expectations are produced by scripts/ask_corpus.py's normalise() and
// pasted here. The two implementations build and then test the same
// allow-list, so if they ever disagree the answer layer starts rejecting true
// figures. Regenerate with:
//   python3 -c "import sys; sys.path.insert(0,'scripts'); import ask_corpus as a; \
//     print([a.normalise(t) for t in ['07','0','00','6.50','6.00','715.4','2026','0.5','50']])"
section("normalise agrees with the corpus builder");
const PY = {
  "07": "7", "0": "0", "00": "0", "6.50": "6.5", "6.00": "6",
  "715.4": "715.4", "2026": "2026", "0.5": ".5", "50": "50",
};
for (const [input, want] of Object.entries(PY)) {
  check(`${input} -> ${want}`, normalise(input) === want, normalise(input));
}

section("numerals");
check("a decimal is one token, not two",
  JSON.stringify(numerals("Storage held 6.54 Bcf.")) === JSON.stringify(["6.54"]),
  JSON.stringify(numerals("Storage held 6.54 Bcf.")));
check("a padded date yields its unpadded parts",
  numerals("2026-07-17").join(",") === "2026,7,17",
  numerals("2026-07-17").join(","));

// ------------------------------------------------------------------ numeral
section("the numeral check");
const allowed = new Set(["6.54", "50.3", "2026", "7", "17", "715.4"]);
check("a figure from the record passes",
  checkNumerals("Storage was 6.54 Bcf, 50.3 percent of design.", allowed).ok);
check("a figure the record does not contain is refused",
  !checkNumerals("Storage was 9.91 Bcf.", allowed).ok,
  JSON.stringify(checkNumerals("Storage was 9.91 Bcf.", allowed).offending));
check("prose with no numbers passes",
  checkNumerals("The comment window has closed.", allowed).ok);
// The specific failure this exists to stop: a confident, well-formed,
// completely invented dollar amount.
check("an invented dollar amount is refused",
  !checkNumerals("AIDEA committed $412 million to the project.", allowed).ok);
check("digits inside a citation are not read as a figure",
  checkNumerals("See [[eo-14318-data-center-permitting]].", allowed).ok,
  JSON.stringify(checkNumerals("See [[eo-14318-data-center-permitting]].", allowed).offending || []));

// ----------------------------------------------------------------- citation
section("the citation check");
const slugs = new Set(["aidea-houston-industrial-park", "bradley-lake-dixon-diversion"]);
check("a real slug passes",
  checkCitations("Comments are open [[aidea-houston-industrial-park]].", slugs).ok);
check("an invented slug is refused",
  !checkCitations("See [[anchorage-fusion-reactor-permit]].", slugs).ok,
  JSON.stringify(checkCitations("See [[anchorage-fusion-reactor-permit]].", slugs).unknown));
check("text with no citation passes", checkCitations("No citation here.", slugs).ok);

// ------------------------------------------------------------------ verdict
section("the no-verdict rule refuses a call");
const CALLS = [
  "Southcentral will run out of gas this winter.",
  "There is enough gas to get through the winter.",
  "Cook Inlet has sufficient supply for the season.",
  "The all clear has been given on winter supply.",
  "Expect blackouts in Anchorage in January.",
  "There is no risk of a supply interruption.",
  "We will make it through the winter.",
  "A shortfall is likely by February.",
  "Southcentral's gas supply is adequate.",
  "The region is safe for this heating season.",
  "You won't run out of heat this winter.",
];
for (const s of CALLS) {
  const r = checkVerdict(s);
  check(`refused: "${s.slice(0, 46)}..."`, !r.ok, r.hit ? `hit "${r.hit}"` : "NOT CAUGHT");
}

// The half that decides whether this guard is usable rather than merely safe.
// A refusal necessarily contains the words of the claim it declines to make,
// so a guard that blocks these would block its own correct answer and push the
// model toward answering instead.
section("and still allows the record to describe itself");
const ALLOWED_PROSE = [
  "The record does not say whether there will be enough gas this winter.",
  "The gas watch publishes no shortfall prediction of any kind.",
  "Nobody publishes a public forecast of winter adequacy.",
  "This page cannot tell you whether supply is adequate.",
  "Storage stood at 6.54 Bcf on August 7th, 2026, which is 50.3 percent of design.",
  "CINGSA reports storage daily and keeps no archive.",
  "The docket tracks the Enstar Cook Inlet gas storage decision.",
  "That is not a forecast and should not be read as one.",
  "Curtailment can happen on a day the numbers looked survivable.",
];
for (const s of ALLOWED_PROSE) {
  const r = checkVerdict(s);
  check(`allowed: "${s.slice(0, 46)}..."`, r.ok, r.hit ? `WRONGLY hit "${r.hit}"` : "");
}

// ---------------------------------------------------------------- composite
section("the composite check");
check("a clean sentence passes all four",
  checkSentence("Comments are open [[aidea-houston-industrial-park]] until 2026.",
    { allowed, slugs }).ok);
check("the composite reports the citation first",
  checkSentence("See [[nope]] about 9.91 Bcf.", { allowed, slugs }).reason === "citation");
check("the composite catches a numeral when citations are clean",
  checkSentence("Storage was 9.91 Bcf.", { allowed, slugs }).reason === "numeral");
check("the composite catches a verdict when the numbers are real",
  checkSentence("There is enough gas.", { allowed, slugs }).reason === "verdict");

// ---------------------------------------------------------------- splitting
section("sentence splitting");
{
  const { sentences, remainder } = splitSentences("One. Two. Three");
  check("complete sentences are released", sentences.length === 2, JSON.stringify(sentences));
  check("the tail is held back as remainder", remainder === "Three", remainder);
}
{
  const { sentences } = splitSentences("Storage was 6.54 Bcf on the 7th. Next. ");
  check("a decimal does not split a sentence", sentences[0] === "Storage was 6.54 Bcf on the 7th.",
    JSON.stringify(sentences[0]));
}

// ------------------------------------------------------------- house voice
//
// The four banned marks and the assistant tics. Unlike everything above, a hit
// here is REWRITTEN rather than refused, so the red cases assert the repair
// rather than a rejection. The last group is the important one: a repair that
// could move a digit would undo the strongest control in this file.
section("the house rewrite");
const same = (a, b, label) => check(label, plainly(a) === b,
  `${JSON.stringify(plainly(a))} wanted ${JSON.stringify(b)}`);

same("The picture: storage held 6.54 Bcf.", "The picture, storage held 6.54 Bcf.",
  "a colon becomes a comma");
same("It gives 6.54 Bcf; it does not give the change.",
  "It gives 6.54 Bcf. It does not give the change.",
  "a semicolon becomes two sentences, second one capitalised");
same("The Assembly votes — the date is published.",
  "The Assembly votes, the date is published.", "an em dash becomes a comma");
same("Two items, — and a third.", "Two items, and a third.",
  "a dash after a comma does not double it");
same("The window ran 2024–2025 in full.", "The window ran 2024-2025 in full.",
  "a dash between digits keeps the range readable");
same("It isn’t published, they said “no”.",
  "It isn't published, they said \"no\".", "curly quotes are straightened");
same("Great question. The Assembly decides.", "The Assembly decides.",
  "an opener with no content is dropped");
same("It's worth noting that the window is open.", "The window is open.",
  "throat clearing goes and the sentence is lifted to a capital");
same("Certainly! The Assembly decides.", "The Assembly decides.",
  "an assistant flourish goes");

// The half arrived stream. A colon at the very end of the buffer is left
// alone, because the character after it has not landed yet and rewriting a
// URL's colon would break the link it is part of.
same("https://alaskaaihq.com/docket/ is the page.",
  "https://alaskaaihq.com/docket/ is the page.", "a URL survives intact");
same("The record says", "The record says", "a bare fragment is untouched");
check("a colon at the end of the buffer waits for its next character",
  plainly("The figures are:") === "The figures are:", plainly("The figures are:"));

// THE ONE THING THIS MUST NEVER DO.
{
  const cases = [
    "Storage held 6.83 Bcf, 52.5 percent of 13.0 Bcf, up 41.1 MMcf.",
    "It ran 2024–2025; storage held 6.54 Bcf: that is 50 percent.",
    "See [[enstar-cook-inlet-gas-storage]] and [[eo-14318-data-center-permitting]].",
  ];
  const moved = cases.filter((c) =>
    numerals(plainly(c)).join(",") !== numerals(c).join(","));
  check("no rewrite changes a single figure", moved.length === 0, JSON.stringify(moved));
  check("no rewrite touches a citation",
    plainly(cases[2]) === cases[2], plainly(cases[2]));
}

// And the rewrite has to be what the checker sees, or a reader could be shown
// a sentence in a form nothing verified.
{
  const { sentences } = splitSentences("The picture: it held 6.54 Bcf. Next. ");
  check("splitSentences hands back rewritten text",
    sentences[0] === "The picture, it held 6.54 Bcf.", JSON.stringify(sentences[0]));
}

console.log();
console.log(failures === 0 ? "checks clean" : `checks FAILED (${failures})`);
process.exit(failures === 0 ? 0 : 1);
