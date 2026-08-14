// Flatten the worker's four modules into one pasteable file.
//
// WHY THIS EXISTS. Deploying with wrangler needs a terminal, a Node install and
// a working local checkout. That is a fine ask for a laptop and a poor one for
// a Chromebook whose Linux container will not start. Cloudflare's dashboard can
// create a Worker from a single pasted file, so this produces exactly that:
// bundled.js, one module, no imports, byte for byte the same logic.
//
// WHY IT IS GENERATED AND NOT HAND WRITTEN. A hand assembled copy drifts from
// the modules the tests run against, and the first sign of the drift would be a
// reader getting an answer the guard no longer checks. This runs from the same
// four files the tests import, and it FAILS LOUDLY on a name collision rather
// than silently letting one definition win. deep.js and answer.js both export a
// function called verify, which is exactly the collision that would quietly
// point the answer lane at the archive lane's checker.
//
// Run: node workers/ask/bundle.mjs
// Test: node workers/ask/test-bundle.mjs

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

// Dependency order. checks.js depends on nothing, deep.js and answer.js depend
// on checks.js, worker.js depends on both.
const MODULES = ["checks.js", "deep.js", "answer.js", "worker.js"];

// Renames applied to a module's own top level declarations before it is
// appended, so two modules may keep the names that read best in their own file.
const RENAME = {
  "deep.js": { verify: "verifyArchiveAnswer" },
};

const IMPORT_RE = /^\s*import\s[^;]*?from\s*["']\.\/[^"']+["'];?\s*$/gm;

// `deep.foo(...)` has to become `foo(...)` once deep.js is inlined.
const NAMESPACE_CALL = /\bdeep\.([A-Za-z_$][\w$]*)/g;

function topLevelNames(src) {
  const names = new Set();
  const re = /^export\s+(?:async\s+)?(function|const|let|var|class)\s+([A-Za-z_$][\w$]*)/gm;
  const re2 = /^(?:async\s+)?(function|const|let|var|class)\s+([A-Za-z_$][\w$]*)/gm;
  for (const m of src.matchAll(re)) names.add(m[2]);
  for (const m of src.matchAll(re2)) names.add(m[2]);
  return names;
}

function renameIdent(src, from, to) {
  // Word boundaries only, and not after a dot, so obj.verify is left alone.
  return src.replace(new RegExp(`(?<!\\.)\\b${from}\\b`, "g"), to);
}

const seen = new Map();          // name -> module that declared it
const parts = [];
const collisions = [];

for (const file of MODULES) {
  let src = readFileSync(join(HERE, file), "utf8");
  src = src.replace(IMPORT_RE, "");
  src = src.replace(NAMESPACE_CALL, "$1");

  for (const [from, to] of Object.entries(RENAME[file] || {})) {
    src = renameIdent(src, from, to);
  }

  for (const name of topLevelNames(src)) {
    if (seen.has(name)) collisions.push(`${name}: ${seen.get(name)} and ${file}`);
    else seen.set(name, file);
  }

  parts.push(`// ${"=".repeat(66)}\n// ${file}\n// ${"=".repeat(66)}\n\n${src.trim()}\n`);
}

if (collisions.length) {
  console.error("name collisions, add them to RENAME rather than shipping this:");
  for (const c of collisions) console.error("  " + c);
  process.exit(1);
}

const header = `// GENERATED FILE. Do not edit.
//
// The ask worker's four modules flattened into one, so it can be created by
// pasting into the Cloudflare dashboard without a terminal. Regenerate with:
//
//   node workers/ask/bundle.mjs
//
// Edit checks.js, deep.js, answer.js or worker.js instead. The tests run
// against those; test-bundle.mjs runs the same assertions against this, so the
// two cannot drift without something going red.

`;

const out = join(HERE, "bundled.js");
writeFileSync(out, header + parts.join("\n"));
console.log(`bundled.js  <-  ${MODULES.join(", ")}  (${seen.size} top level names, no collisions)`);
