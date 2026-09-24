# CI trigger note, run No.67, 2026-09-24

An addendum to automation_retro.md, written during the Codex review rounds on PR #397.
CORRECTED: an earlier version of this file blamed the session's push credential.
That diagnosis was wrong.

From 09:31 UTC none of this run's pushes created a `pull_request` workflow run.
The cause was a MERGE CONFLICT. At 09:31 the scheduled gas watch collector
committed today's reading and a page rebuild to main (337f8678, fef249b3). That
conflicted with the run branch's regenerated `docs/`, and GitHub creates no
`pull_request` runs for a PR it can't test-merge. The API-made commit that first
added this file got no run for the same reason. Once main was merged in (the
conflicts were generated pages only, resolved by regenerating with site_build.py),
the next push got a full set of runs at once.

`workflow_dispatch` answers 403 "Resource not accessible by integration" for this
session's connector, so dispatch is not a way around it.

Lesson for the routine: the gas watch commits to main every morning. If a run's CI
goes quiet after a push, check the PR's mergeability first, merge main, and
regenerate docs/ before suspecting anything else.
