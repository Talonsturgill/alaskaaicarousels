// Tests for the answer checks. Run: node workers/ask/test.mjs
//
// Every control gets a green case AND a red case. A check that cannot fail
// certifies nothing, and these are the only thing standing between what a
// fired routine writes and a claim published under the site's name.

import {
  normalise, numerals, checkVerdict, checkCitations, checkNumerals,
  checkSentence, splitSentences,
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

console.log();
console.log(failures === 0 ? "checks clean" : `checks FAILED (${failures})`);
process.exit(failures === 0 ? 0 : 1);
