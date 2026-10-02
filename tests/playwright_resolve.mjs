/* playwright_resolve.mjs -- the browser suites' one way to find playwright
 * (2026-10-02, run No.75).
 *
 * WHY THIS EXISTS. The ESM suites used to say `import { chromium } from
 * 'playwright'`. An ESM bare specifier resolves ONLY by walking up node_modules
 * from the importing file: it ignores NODE_PATH and it ignores the global npm
 * root. CI satisfies that with `npm install --no-save playwright` in the repo
 * root. A routine run has no repo node_modules, only the global install, so the
 * import failed and two runs in a row (2026-10-01, 2026-10-02) linked
 * node_modules to a scratch directory under /tmp to get past it. Every command
 * that touched that link resolved outside the project, the harness stopped to
 * ask, and No.75 sat about nine hours waiting for a human who was not there.
 * The FIELD_NOTES remedy written the day before, NODE_PATH="$(npm root -g)",
 * is right for the CommonJS suites and does nothing for these four.
 *
 * WHAT IT DOES. createRequire() gives a CommonJS require anchored at this file,
 * which DOES honour NODE_PATH and the repo's node_modules (CI unchanged). If
 * neither has playwright it tries the global root of the node that is running,
 * <prefix>/lib/node_modules, the layout of every Linux node install. Nothing is
 * linked, copied or written anywhere. Run the suites through
 * `python3 scripts/browser_suites.py`, which builds the site under out/.
 */
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';

const require = createRequire(import.meta.url);

function load() {
  try {
    return require('playwright');
  } catch (e) {
    if (e.code !== 'MODULE_NOT_FOUND') throw e;
  }
  const global = join(dirname(dirname(process.execPath)), 'lib', 'node_modules', 'playwright');
  try {
    return require(global);
  } catch (e) {
    throw new Error('playwright is not installed in the repo, on NODE_PATH, or at ' + global +
      '. Install it (npm install --no-save playwright, as CI does) rather than linking ' +
      'node_modules to a directory outside the repo.');
  }
}

export const { chromium, devices } = load();
