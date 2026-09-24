# CI trigger note, run No.67, 2026-09-24

An addendum to automation_retro.md, written during the Codex review rounds on PR #397.

None of this session's `git push`es to the run branch created a `pull_request`
workflow run. Only the PR's opening did (b92f8e1). `workflow_dispatch` answers
403 "Resource not accessible by integration" for this session's connector. Run
No.66 the day before got a run on every push, so the cause is this session's
push credential, not the workflows.

A commit made through the GitHub API (the one that added this file) is a
separate push event, and it's how CI reaches the current head.

Proposal for the maintainer: if this recurs, Phase 11 should make its LAST
commit before the merge through the API, or the routine should check that a
workflow run exists for the head SHA before reading "green" off an older one.
