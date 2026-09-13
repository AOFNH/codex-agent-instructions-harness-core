---
title: Instructions and Context Harness — Agent Manual
version: 1.0.0
audience: coding agents
status: current
---

# Instructions and Context Harness: Agent Manual

Use this manual only when maintaining user-level instructions, a reference
catalog, routing protocol, or this harness. For first-time creation of a
personal repository from core, read `PERSONAL-OVERLAY-GUIDE.md` first. Ordinary
application development does not require either guide. In a personal overlay,
apply the procedures below only to overlay-owned files; inherited core files
remain read-only and core changes go through upstream.

## 1. Maintenance boundaries

- Runtime behavior is defined by the root `AGENTS.md`, selected
  `agent-references/` files, and project-level instructions.
- `docs/design/current.md` and `docs/iterations/` record design and history;
  they are not runtime rules automatically.
- `harness/fixtures/` contains de-identified regression data and must not refer
  to current device state.
- `agent-references/catalog.d/*.yaml` contains mergeable catalog fragments; a
  personal overlay adds its own fragment and does not modify an upstream
  fragment.
- Do not modify production configuration, authentication files, browser state,
  real business repositories, or host Codex runtime state.
- Do not read or write the host's real `CODEX_HOME`, path mappings, or secrets
  to make a test pass.

## 2. Starting an iteration

1. Work in an isolated branch or worktree.
2. Confirm the checkout's Git root and that the worktree has no unrelated
   changes.
3. Read `docs/design/current.md`, the current iteration directory, and this
   manual.
4. Run structural validation and regression first and record the baseline.
5. Modify runtime files, the catalog, fixtures, or documentation.
6. Run all checks again and inspect expected results and provenance.
7. Review de-identification, the Git allowlist, and the complete diff.
8. In the core repository, commit behavior, fixtures, design, and acceptance
   records as one atomic change. In an overlay, commit only the overlay files
   that belong to the change; do not copy or revise inherited core records.

## 3. Running validation

Run from the repository root:

```bash
python3 harness/scripts/validate.py --root .
python3 harness/scripts/route_regression.py --root .
```

The scripts read only the catalog and fixtures in the current checkout. They do
not read host path mappings, real repositories, or external services.

The environment requires Python 3 and `PyYAML`. Install dependencies in an
isolated environment according to `harness/requirements.txt`, or use an
equivalent environment already provided by the maintainer. Do not modify a
business repository or commit dependency caches here.

## 4. Handling structural failures

Investigate in this order:

1. YAML syntax and top-level structure;
2. ID, owner, authority, status, and `applies_to`;
3. catalog fragment paths and reference files;
4. fixture `load`/`exclude` references to registered IDs;
5. conflicts between `target_repo` and `reference_only` repositories;
6. absolute paths, credentials, real URLs, or host state in versioned files.

Fix the data or reference first. Do not skip the script.

## 5. Handling regression results

The regression script checks:

- route status;
- company;
- target repository;
- reference-only repositories;
- the complete `load` and `exclude` instruction-ID sets.

It does not compare an agent's natural-language wording. After a failure,
determine whether the cause is:

- a runtime rule change;
- an obsolete fixture;
- incorrect catalog metadata;
- a harness defect; or
- model/client behavior changing.

Change an expected result only when product strategy has actually changed, and
record the reason in the current iteration's `decisions.md`. Do not change an
expected value merely to make the test green.

## 6. Adding a de-identified case

When adding a case from a real problem:

1. Keep only routing relationships, evidence strength, and conflict structure.
2. Replace companies, repositories, products, paths, URLs, users, and versions
   with stable synthetic identifiers.
3. Delete transcripts, logs, screenshots, credentials, and host configuration.
4. Write the logical expected result and record why it is correct.
5. Run structural validation, regression, and sensitive-information scans.
6. Commit the case and its decision in the same iteration change.

Never commit real information first and plan to de-identify it later.

## 7. Updating design documents

In the core repository, update `docs/design/current.md` when any of these
changes:

- routing evidence priority;
- `confirmed`/`provisional`/`blocked` semantics;
- owner, authority, lifecycle, or dependency rules;
- boundaries between instructions, fixtures, and the harness.

Do not create a new design version for wording, formatting, or implementation
details that leave the contract unchanged. In a personal overlay, do not edit
the inherited design document; send a core-contract change upstream instead.

The current iteration record should preserve motivation, trade-offs, failure
causes, and acceptance results. Historical records do not replace the current
design.

## 8. Commit and release

- Select files explicitly with the Git allowlist; never use `git add -A`.
- In the core repository, check runtime files, catalog, fixtures, documents,
  and harness together for every behavior change. In an overlay, check the
  overlay catalog and references, plus the inherited validation suite, without
  modifying inherited core files.
- Do not commit auth, config, session, log, cache, SQLite, memory, plugin,
  skill, shell-snapshot, or `local/` files.
- Use conventional commits for ordinary fixes. Create an
  `instructions/vX.Y.Z` tag only for a complete snapshot release.
- Tags support reproduction, not daily company switching. For historical
  reproduction, check out the tag and use an isolated `CODEX_HOME`.

## 9. Stop conditions

Stop side-effect operations and record the issue when any of these occurs:

- the target repository or company ownership cannot be confirmed;
- source repository, remote, and workspace/domain evidence conflicts;
- a fixture requires real paths or sensitive data to express the case;
- expected results disagree with the current design without a decision record;
- the harness can run only by reading host state;
- the Git allowlist cannot clearly distinguish files to commit from files to
  exclude.
