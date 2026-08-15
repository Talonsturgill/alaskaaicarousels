// Verification for answers the ask box is about to publish.
//
// These run on the model's output BEFORE a word of it reaches the page, one
// sentence at a time, so nothing unverified is ever shown and the reader still
// sees text appear progressively. Four controls, weakest last:
//
//   1. numerals    A reply may only contain numbers that appear in the record.
//                  This is the page's own numeral lint (gaswatch_build.py)
//                  moved from build time to answer time, and it is the
//                  strongest control here: an invented figure is arithmetically
//                  incapable of passing.
//   2. citations   Every [[slug]] must be a docket item that exists. A
//                  plausible-looking link to an item nobody wrote cannot ship.
//   3. verdict     No adequacy call on the gas position, in either direction.
//                  CLAUDE.md: "It NEVER publishes a safety verdict. Not a
//                  shortfall prediction, not an all clear, not a blackout call."
//   4. corpus      Not enforced here, but the reason the others hold: the
//                  record contains measured past readings and no forecast at
//                  all, so there is nothing for a forecast to be built out of.
//
// HONEST LIMIT. Controls 1 and 2 are set-membership tests and hold absolutely.
// Control 3 is a pattern match on free text and is the weakest of the four:
// it is a backstop for a model that has already been told not to, not a proof.
// It is written to catch assertions rather than topic words, because a reader
// asking "what does the gas watch actually measure?" deserves an answer that
// is allowed to contain the word shortfall.

// One spelling per number. Must agree exactly with normalise() in
// scripts/ask_corpus.py, which builds the allow-list this checks against; a
// divergence between the two would reject true figures. Pinned by a test that
// compares both implementations over the same inputs.
export function normalise(tok) {
  tok = String(tok).replace(/,/g, "");
  // Padding zeros go. The zero in FRONT of a decimal point does not: 0.8469 becoming .8469
  // leaves a token NUMERAL_RE cannot match at all, so a figure written back that way would
  // slip past this gate entirely.
  tok = /^0\./.test(tok) ? "0" + tok.replace(/^0+/, "") : (tok.replace(/^0+/, "") || "0");
  if (tok.includes(".")) {
    tok = tok.replace(/0+$/, "").replace(/\.$/, "") || "0";
  }
  return tok;
}

// A THOUSANDS SEPARATOR IS PART OF THE NUMBER, NOT A BREAK IN IT, and this line has to agree
// with scripts/ask_corpus.py's NUMERAL_RE exactly or the allow-list and the checker are
// measuring different things. It used to be /\d+(?:\.\d+)?/g on both sides, which read "4,700"
// as a 4 and a 700 and authorised both. The pack carries 35 comma grouped figures, and the
// split admitted six numerals appearing nowhere in the record on their own: 150, 300, 566,
// 700, 950 and 967, which are exactly the round figures a model invents.
const NUMERAL_RE = /\d(?:[\d,]*\d)?(?:\.\d+)?/g;

export function numerals(text) {
  return (text.match(NUMERAL_RE) || []).map(normalise);
}

// An assertion about whether the gas holds out, in either direction. Ordered
// roughly most to least specific. Each one targets a predicate, not a noun, so
// mentioning a shortfall is fine and calling one is not.
const VERDICT = [
  /\b(?:will|wo n't|won'?t|will not|going to|gonna)\s+(?:\w+\s+){0,2}?(?:run\s+out|run\s+short|be\s+enough|have\s+enough)/i,
  /\bthere\s+(?:is|are|will\s+be)\s+(?:\w+\s+){0,2}?(?:enough|sufficient|adequate|plenty)\b/i,
  /\b(?:enough|sufficient|adequate|plenty\s+of)\s+(?:gas|supply|storage|fuel|inventory)\b/i,
  /\b(?:supply|storage|inventory|the\s+region|southcentral|alaska)\s+(?:is|are|will\s+be)\s+(?:\w+\s+){0,1}?(?:adequate|sufficient|fine|safe|secure|okay|ok)\b/i,
  /\ball\s+clear\b/i,
  /\bblack\s?outs?\b/i,
  /\bno\s+(?:risk|danger)\s+of\b/i,
  /\b(?:we|you|alaskans?)\s+(?:will|should|wo n't|won'?t|will not)\s+(?:\w+\s+){0,2}?(?:make it|be fine|be okay|be ok|freeze|run out)/i,
  /\b(?:shortfall|shortage|curtailment)\s+(?:is|will\s+be|of)\s+(?:\w+\s+){0,2}?(?:likely|coming|expected|certain|imminent|unlikely)\b/i,
  /\b(?:is|are|will\s+be)\s+(?:not\s+)?safe\b/i,
];

// A sentence that DECLINES to make the call necessarily contains the words of
// the call it is declining to make. "The record does not say whether there
// will be enough gas" trips the first pattern above and is exactly the
// sentence we want the model to write. Without this exemption the guard would
// block its own correct refusal, which is how a safety check ends up teaching
// a model to answer instead.
const DISCLAIMED =
  /\b(?:does\s+not|doesn'?t|do\s+not|don'?t|cannot|can'?t|could\s+not|couldn'?t|will\s+not|wo\s?n'?t|no\s+one|nobody)\s+(?:\w+\s+){0,2}?(?:say|says|state|publish|publishes|predict|predicts|forecast|forecasts|tell|know|answer|claim)\b/i;
const NO_SUCH_THING =
  /\bn(?:o|ot\s+a)\s+(?:public\s+)?(?:forecast|prediction|projection|verdict|guarantee|assurance)\b/i;

export function checkVerdict(text) {
  if (DISCLAIMED.test(text) || NO_SUCH_THING.test(text)) return { ok: true };
  for (const re of VERDICT) {
    const m = text.match(re);
    if (m) return { ok: false, reason: "verdict", hit: m[0].trim() };
  }
  return { ok: true };
}

const CITE_RE = /\[\[([^\]]+)\]\]/g;

export function checkCitations(text, slugs) {
  const unknown = [];
  for (const m of text.matchAll(CITE_RE)) {
    if (!slugs.has(m[1])) unknown.push(m[1]);
  }
  return unknown.length ? { ok: false, reason: "citation", unknown } : { ok: true };
}

export function checkNumerals(text, allowed) {
  // Citation slugs can carry digits (eo-14318, adl-422741). They are checked
  // as slugs, so stripping them here stops a valid citation from being read as
  // an unauthorised figure.
  const prose = text.replace(CITE_RE, " ");
  const bad = numerals(prose).filter((n) => !allowed.has(n));
  return bad.length ? { ok: false, reason: "numeral", offending: bad } : { ok: true };
}

// The composite the streaming loop calls. Cheapest and strictest first, so a
// failure reports the most actionable cause.
export function checkSentence(text, { allowed, slugs }) {
  const c = checkCitations(text, slugs);
  if (!c.ok) return c;
  const n = checkNumerals(text, allowed);
  if (!n.ok) return n;
  return checkVerdict(text);
}

// HOW THE HOUSE PUNCTUATES, APPLIED TO A MACHINE THAT DOES NOT.
//
// Em dashes, en dashes, semicolons and colons are the four marks that make a
// sentence read as written by a language model rather than said by a person,
// and the first two are already banned everywhere else this repo publishes
// (CLAUDE.md, config/brand.yaml, scripts/caption_check.py). The model is told
// all four in the prompt. This is what happens when it forgets.
//
// REPAIRED, NOT REJECTED, AND THAT IS A DELIBERATE LINE. The checks above cut
// an answer at the first sentence that fails, because a wrong number and an
// invented citation are claims about the world and a smoothed over one is
// worse than a visible stop. A semicolon is not a claim about anything. Ending
// an answer over a punctuation mark would punish the reader for the model's
// typing, so this rewrites and says nothing.
//
// The rewrite runs BEFORE the sentence is checked and before it is sent, so
// the text a reader sees is the exact text that passed. There is no window in
// which a checked sentence is edited.
//
// Nothing here can touch a figure. Every rule below either replaces a mark
// with another mark or lifts a letter to a capital. The one rule that goes
// near digits, a dash between two numbers, keeps them both and leaves a
// hyphen, because turning 2024-2025 into "2024, 2025" would change what it
// says and this file's whole job is that nothing does.
const FILLER = [
  // Whole sentences that carry no content. Removed entirely.
  /^(?:great|good|excellent|interesting)\s+question[.!]?\s*/i,
  /^(?:certainly|absolutely|sure thing|sure|of course|indeed)[,.!]\s*/i,
  /^i hope (?:this|that) helps[.!]?\s*/i,
  /^happy to help[.!]?\s*/i,
  // Throat clearing in front of a real sentence. The clause goes, what
  // follows it is lifted to a capital and keeps its meaning intact.
  /^(?:it'?s |it is )?(?:worth |important |also worth )?(?:noting|mentioning|pointing out) that\s+/i,
  /^(?:please )?(?:do )?note that\s+/i,
  /^to (?:be clear|answer your question|directly answer)[,:]?\s+/i,
  /^in (?:conclusion|summary|short)[,:]?\s+/i,
  /^at its core[,:]?\s+/i,
  /^that (?:being )?said[,:]?\s+/i,
];

export function plainly(text) {
  let t = String(text)
    // House straight quotes, same rule the site builder enforces on itself.
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/…/g, "...")
    // A range keeps its reading. This is the only rule that sees a digit.
    .replace(/(\d)\s*[—–]\s*(\d)/g, "$1-$2")
    // Any other dash was standing in for a comma, so it becomes one. The
    // leading [,\s]* absorbs a comma already sitting there, which is how
    // ", and, then" would otherwise happen.
    .replace(/[,\s]*[—–]\s*/g, ", ")
    // A semicolon joins two sentences that wanted to be two sentences.
    .replace(/;\s+([a-z])/g, (_, c) => ". " + c.toUpperCase())
    .replace(/;(?=\s)/g, ".")
    // A colon reads as a slide heading. A comma reads as a person talking.
    // Only when whitespace follows, which is what keeps 12:30 and https://
    // whole, and what makes this safe to run on a half arrived stream: a
    // colon at the end of the buffer is left until its next character lands.
    .replace(/:(?=\s)/g, ",")
    // Tidying after the two rules above, which can leave a comma doubled, a
    // comma in front of a full stop, or a comma opening the answer when the
    // model started a line with a dash.
    .replace(/,\s*,/g, ",")
    .replace(/,\s*([.!?])/g, "$1")
    .replace(/^[,\s]+/, "");
  for (const re of FILLER) {
    const before = t;
    t = t.replace(re, "");
    if (t !== before) t = t.charAt(0).toUpperCase() + t.slice(1);
  }
  return t;
}

// Split on sentence ends only where a space follows, so decimals (6.54 Bcf)
// and abbreviated dockets stay whole. A trailing fragment is returned as the
// remainder for the next chunk rather than checked early.
//
// The house rewrite runs here rather than at the three call sites, because
// three places to remember is three places to forget, and a sentence that
// reached a reader unrewritten would be the one nobody noticed.
export function splitSentences(buffer) {
  const parts = plainly(buffer).split(/(?<=[.!?])\s+/);
  const remainder = parts.pop() ?? "";
  return { sentences: parts, remainder };
}
