#!/usr/bin/env bash
# Install Playwright and Chromium for a CI job, without letting somebody else's
# apt mirror decide whether this repo's tests get to run.
#
# WHY THIS EXISTS. Every browser gate here ran `npx playwright install
# --with-deps chromium`, and --with-deps means apt, and apt means Google's
# chrome-stable deb repository. On 2026-08-14 that repository was mid-sync and
# served a Packages.gz one byte off its published size, so apt refused it and
# the install exited 100. A second attempt twenty minutes later hung on the
# same step for nine minutes. Two failures in one afternoon, neither of them
# about this repo's code, both of them red lights a person had to come look at.
#
# A gate that fails for reasons nobody controls is a gate everybody learns to
# ignore, which is the same argument the gas watch workflow makes for keeping
# its own self test hermetic.
#
# WHAT THIS DOES INSTEAD. The browser BINARY comes from Playwright's own CDN and
# has never been the problem, so that install is unconditional. The system
# libraries are what apt is for, and on GitHub's ubuntu-latest image they are
# almost always already present, so this asks for them, retries a couple of
# times with a pause, and then carries on ANYWAY rather than failing the job.
#
# That is deliberate and it is not a way of hiding a broken install. If a
# library really is missing, chromium fails to launch and the test that needs
# it goes red on its own, with an error about the browser rather than an error
# about a mirror. The failure still surfaces. It just surfaces as a fact about
# this repo instead of a fact about somebody's CDN.
#
# Usage:  bash .github/workflows/browser.sh [playwright-version]
set -uo pipefail

VERSION="${1:-1}"

set -e
npm install --no-save "playwright@${VERSION}"
set +e

# System libraries. Best effort, bounded, and never fatal.
for attempt in 1 2 3; do
  if timeout 240 npx playwright install-deps chromium; then
    echo "system libraries in place on attempt ${attempt}"
    break
  fi
  if [ "${attempt}" -eq 3 ]; then
    echo "::warning::apt could not be reached in three attempts. Continuing" \
         "with whatever the runner image already has. If a library really is" \
         "missing, the browser will fail to launch and the test will say so."
    break
  fi
  echo "apt attempt ${attempt} failed, waiting before the next one"
  sleep $((attempt * 20))
done

# The browser itself, from Playwright's CDN. This one has to work.
set -e
npx playwright install chromium
echo "chromium ready"
