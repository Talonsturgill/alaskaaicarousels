// The gate between the model's tokens and the reader's screen.
//
// Streaming and verification pull against each other: you cannot check text
// you have already shown, and you cannot show text fast if you check the whole
// answer first. This resolves the tension at the sentence: buffer until a
// sentence is complete, check it, and release it only if it passes. The reader
// waits one sentence rather than a whole answer, and no unverified word is
// ever displayed.
//
// A failure stops the answer where it failed. The sentences already released
// were verified and stay; the rest is withheld and the reader is told. That is
// deliberately visible. Silently dropping a sentence would leave a fluent
// answer with a hole in it, which reads as true and is worse than an obvious
// stop.

import { checkSentence, splitSentences } from "./checks.js";

export function createReleaser({ allowed, slugs, onText, onWithheld }) {
  let buffer = "";
  let released = "";
  let stopped = false;

  async function drain(sentences) {
    for (const s of sentences) {
      const verdict = checkSentence(s, { allowed, slugs });
      if (!verdict.ok) {
        stopped = true;
        await onWithheld(verdict, s);
        return;
      }
      const text = s.trim();
      released += (released ? " " : "") + text;
      await onText(text);
    }
  }

  return {
    /** Feed a chunk of model text. Releases whatever is now complete and clean. */
    async push(chunk) {
      if (stopped) return;
      buffer += chunk;
      const { sentences, remainder } = splitSentences(buffer);
      buffer = remainder;
      await drain(sentences);
    },
    /** The model finished. Release the trailing fragment if it passes. */
    async end() {
      if (stopped || !buffer.trim()) return;
      const tail = buffer;
      buffer = "";
      await drain([tail]);
    },
    get stopped() { return stopped; },
    /** Everything that passed, for the answer cache. Empty if nothing did. */
    get text() { return released; },
  };
}
