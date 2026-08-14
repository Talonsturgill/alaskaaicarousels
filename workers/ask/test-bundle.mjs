// Run the answer lane's whole suite against bundled.js.
//
// bundled.js is what actually runs when the worker is created by pasting into
// the Cloudflare dashboard rather than deployed with wrangler. A bundle that
// has drifted from the modules is a worker whose guard is not the guard
// anybody tested, and that drift is invisible: the file still parses, still
// deploys, and still answers. So the same 40 assertions run twice, once
// against the modules and once against the flattened copy.
//
// It also re-flattens from source first and refuses to run if the checked in
// bundle does not match, because a stale bundle passes its own tests happily.
//
// Run: node workers/ask/test-bundle.mjs

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

const before = readFileSync(join(HERE, "bundled.js"), "utf8");
execFileSync(process.execPath, [join(HERE, "bundle.mjs")], { stdio: "pipe" });
const after = readFileSync(join(HERE, "bundled.js"), "utf8");

if (before !== after) {
  console.log("FAIL  bundled.js is stale. It has been regenerated; commit the result.");
  process.exit(1);
}
console.log("PASS  bundled.js is exactly what the modules produce\n");

process.env.ASK_MODULE = "./bundled.js";
await import("./test-answer.mjs");
