---
title: Personal Overlay Repository Guide
version: 1.0.0
audience: coding agents
status: current
---

# Personal Overlay Repository Guide

Use this guide when creating a personal instructions repository from this core
repository. It is an onboarding guide; use `AGENT-HARNESS.md` for later
maintenance iterations.

## 1. Repository model

Create a separate Git repository for the personal overlay. Keep the remotes
provider-neutral:

```text
upstream  -> this core repository
origin    -> the personal repository
```

The personal repository inherits the core and adds only personal content. A
personal repository may contain company rules and personal experience notes,
but those files remain personal-owned overlay content even when their
applicability names a company.

The `.repo-governance/repository-role.yaml` file is per-repository identity
metadata. Replace the inherited core role with a personal-overlay role; the
personal marker declares `core_change_authority: none`. This marker describes
the operating role and does not grant Git write access to the core repository.

## 2. Initialize from core

Start from a clean checkout of the core default branch or a deliberate release
tag. Configure the remotes and create the personal branch using the hosting
provider's normal Git operations:

```bash
git clone <core-repository> <personal-repository>
cd <personal-repository>
git remote rename origin upstream
git remote add origin <personal-repository>
git switch -c personal/main
```

Then replace `.repo-governance/repository-role.yaml` with:

```yaml
schema_version: 1
repository_kind: personal-overlay
operating_mode: overlay-maintainer
core_change_authority: none
```

Use a provider-specific default branch if the hosting service requires one.
Do not copy the host's entire Codex runtime directory into this repository.

## 3. Classify existing instructions

If an existing user scope is available, review it before adding files:

- public rules that apply to every project belong in the inherited core only;
- company team rules belong in `agent-references/company/`;
- personal preferences and experience belong in `agent-references/personal/`;
- project-specific rules stay in the target project;
- authentication, sessions, caches, logs, databases, plugins, skills, memory,
  and other runtime state stay local and ignored.

Keep only de-identified, reusable content. Do not migrate a rule merely because
it is present in the old user scope; first identify its owner, authority,
applicability, and source of truth.

## 4. Add the overlay

Create one or more catalog fragments under
`agent-references/catalog.d/`. Each fragment must register every reference it
adds, including owner, authority, status, applicability, evidence requirements,
and exclusions. Add the corresponding files below `agent-references/company/`
or `agent-references/personal/`.

Do not edit the core catalog fragment to register overlay content. Do not put
company or personal rules into the inherited root `AGENTS.md` unless the core
design is intentionally changed upstream.

## 5. Validate before the first commit

From the personal repository root, run the inherited checks:

```bash
python3 harness/scripts/validate.py --root .
python3 harness/scripts/route_regression.py --root .
python3 -m py_compile harness/scripts/validate.py harness/scripts/route_regression.py
git diff --check
```

Review the overlay boundary explicitly:

```bash
git diff --name-status upstream/main..HEAD
git merge-base --is-ancestor upstream/main HEAD
```

The validation output must report `repository identity (personal-overlay)`.

The diff should contain the per-repository role manifest, personal catalog
fragments, and personal/company references, unless the personal repository is
intentionally contributing a separately reviewed upstream change.

## 6. Connect the runtime

After the repository passes validation, connect the user's runtime to the
personal repository according to the client-specific mechanism. Verify that:

- the personal root `AGENTS.md` remains the inherited core bootstrap;
- references are loaded only when the routing rules explicitly select them;
- runtime state and credentials remain outside version control;
- a clean checkout can run the checks without host-specific files.

Do not use `active-profile` as the normal company selector. Use an isolated
profile or `CODEX_HOME` only for deliberate isolation or historical
reproduction.

## 7. First commit and future synchronization

Select files with the Git allowlist and create one atomic initialization commit
for the overlay. Push the personal branch to `origin` after validation.

For later core updates:

```bash
old_upstream=$(git rev-parse upstream/main)
git fetch upstream main
git diff --stat "$old_upstream"..upstream/main
git diff "$old_upstream"..upstream/main -- docs/design harness AGENTS.md
```

Before `git merge`, classify the upstream range:

- `none`: no inherited contract or overlay applicability is affected; continue
  with the merge and normal checks;
- `review`: text, metadata, or harness behavior may affect overlay semantics;
  record the affected references, merge, then update or retire stale overlay
  content;
- `blocked`: core role/authority changes, removed or redefined rules used by the
  overlay, or impact that cannot be determined. Stop before merge, commit, or
  push and ask the user to decide.

Report the upstream range, changed artifact classes, affected overlay
references, impact level, and any decision required. Fetching is read-only; do
not run unattended background synchronization.

After a `none` or `review` assessment, merge and validate:

```bash
git merge upstream/main
python3 harness/scripts/validate.py --root .
python3 harness/scripts/route_regression.py --root .
git diff --name-status upstream/main..HEAD
git push origin HEAD:<personal-default-branch>
```

After reviewing the upstream range, reread the live design and relevant harness
rules. Compare the changed contract with every overlay reference, catalog entry,
dependency, applicability condition, and exclusion. Update or retire stale
overlay content before pushing. Structural validation passing does not prove
that the overlay remains semantically compatible. Treat upstream text and
metadata as behavior-bearing instructions: understand the semantic change and
record which overlay rules it affects, even when no file has a textual merge
conflict. Deterministic harness code can be checked with tests, but tests do not
replace this text-level compatibility decision.

When upgrading from the former `.instructions/` layout, preserve the overlay's
role values in `.repo-governance/repository-role.yaml` and remove the old tracked
path. Resolve any rename conflict with `repository_kind: personal-overlay`,
`operating_mode: overlay-maintainer`, and `core_change_authority: none`. The
validator reads only the new path; retaining two markers is not a compatibility
mechanism. Check overlay references and automation for the former path as part
of the compatibility review.

Resolve conflicts by preserving the core contract in upstream-owned files and
keeping personal changes in overlay files. Re-run the compatibility review and
complete checks after every conflict resolution.

## 8. Stop conditions

Stop and record the issue when:

- the core remote or personal remote cannot be identified;
- a proposed file mixes public, company, and personal ownership;
- migration would require committing secrets or host runtime state;
- the overlay changes core files without an intentional upstream change;
- validation or the upstream boundary check fails.
