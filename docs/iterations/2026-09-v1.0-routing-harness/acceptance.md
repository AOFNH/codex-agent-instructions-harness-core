---
iteration: 2026-09-v1.0-routing-harness
release_target: instructions/v1.0.0
status: complete
---

# Iteration Acceptance Record

## Structural acceptance

- [x] Root `AGENTS.md` contains only public rules, routing protocol, and
  maintenance boundaries.
- [x] Every runtime reference has `owner`, `authority`, `status`, and
  `applies_to` metadata.
- [x] Catalog paths, IDs, and actual files correspond one-to-one.
- [x] No reference dependency is deeper than one level and no cycle exists.
- [x] Versioned files contain no personal paths, credentials, or host state.
- [x] `.gitignore` still blocks runtime, auth, cache, SQLite, and local state.

## Routing regression

- [x] Explicit target and reference-only repositories.
- [x] Worktree path differs from source repository.
- [x] Confirmed company evidence.
- [x] Provisional company evidence.
- [x] Blocked company evidence.
- [x] Applicable personal preference and inapplicable personal experience.
- [x] Unrelated company rules are excluded.
- [x] Ordinary application development does not load project design documents.

## Reproducibility

- [x] Another agent can run structural validation from a clean checkout by
  following the manual.
- [x] Regression does not read host configuration directories or real
  repositories.
- [x] Model or client wording changes do not affect fixture expectations.
- [x] Every expected-result change has a corresponding decision record.

## Results

Validated successfully:

- `python3 harness/scripts/validate.py --root .`: runtime catalog 0 entries and
  fixture catalog 5 entries.
- `python3 harness/scripts/route_regression.py --root .`: 9 abstract routing
  cases passed.
- `python3 -m py_compile harness/scripts/validate.py
  harness/scripts/route_regression.py`: passed.
- `git diff --check`: passed.
- The structural and routing checks were repeated from a clean checkout:
  passed.
