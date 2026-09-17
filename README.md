# Codex Agent Instructions Harness — Core

This repository is the upstream, agent-first core for a user-level Codex
instructions and context system. It defines the small bootstrap that agents
load automatically, the routing contract for selecting additional references,
and a portable harness for checking routing behavior.

Most files are written for agents and maintainers rather than for end users.
The root [`AGENTS.md`](AGENTS.md) is the runtime entry point. It explains how
to identify the target repository, confirm company and workspace evidence, and
load only the references that apply. Design notes and iteration records under
`docs/` explain why the system is shaped this way; they are not runtime rules.

This core is for the user-level instructions repository and its personal
overlays. It is not a project-level instructions template. An ordinary
application, plugin, or skills repository keeps using its own `AGENTS.md` and
context conventions, even when a task mentions instructions, routing, or a
harness.

## Repository layout

- `AGENTS.md` — public bootstrap and routing protocol;
- `.repo-governance/` — versioned repository governance metadata: roles,
  operating modes, and core-change authority;
- `agent-references/catalog.d/` — mergeable reference catalog fragments;
- `docs/design/current.md` — live design specification;
- `docs/iterations/` — historical design and acceptance records;
- `harness/` — onboarding guide, agent manual, schema, fixtures, and validation
  scripts.

Company-specific rules and personal notes belong in overlay repositories. An
overlay adds its own catalog fragment and references while inheriting this core;
it should not modify upstream-owned files.

## Build your personal instructions repository

This core is intended to be used as the upstream for a separate personal Git
repository:

```text
codex-agent-instructions-harness-core  --upstream-->  your-personal-instructions
                                             --origin-->  your private remote
```

If you already have user-level instructions, the agent should classify and
de-identify them before adding only the reusable company and personal content.
If you are starting from zero, the agent can create the overlay directories and
catalog fragment from an empty repository.

Create or choose the personal repository, then send the following prompt to
your agent. Replace the placeholders before sending it:

```text
Use <core-repository> as the upstream to build my personal Codex instructions
repository at <personal-repository>.

Act as the implementer. First read:
- README.md
- AGENTS.md
- harness/PERSONAL-OVERLAY-GUIDE.md

Set the core repository as upstream and my personal repository as origin.
Review my existing user-level instructions if I provide them, classify reusable
content into company and personal overlays, de-identify it, and keep runtime
state out of Git. If no existing instructions are provided, start with an empty
overlay.

Run the repository validation and routing regression checks, review the diff
against upstream, and complete the implementation and first commit. Report the
files changed, validation results, and any information you need from me.
```

The agent-facing guide contains the full initialization, runtime connection,
and future upstream synchronization procedure. The result should retain the
core bootstrap and harness while adding only the personal repository's catalog
fragment and references.

## Validate a checkout

From the repository root, run:

```bash
python3 harness/scripts/validate.py --root .
python3 harness/scripts/route_regression.py --root .
```

The checks use only files in the checkout and do not require host paths,
credentials, external services, or a live Codex runtime.
