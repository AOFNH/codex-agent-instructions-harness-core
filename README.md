# Codex Instructions Core

This repository is the upstream, agent-first core for a user-level Codex
instructions and context system. It defines the small bootstrap that agents
load automatically, the routing contract for selecting additional references,
and a portable harness for checking routing behavior.

Most files are written for agents and maintainers rather than for end users.
The root [`AGENTS.md`](AGENTS.md) is the runtime entry point. It explains how
to identify the target repository, confirm company and workspace evidence, and
load only the references that apply. Design notes and iteration records under
`docs/` explain why the system is shaped this way; they are not runtime rules.

## Repository layout

- `AGENTS.md` — public bootstrap and routing protocol;
- `agent-references/catalog.d/` — mergeable reference catalog fragments;
- `docs/design/` — current maintenance contract;
- `docs/iterations/` — historical design and acceptance records;
- `harness/` — agent manual, schema, fixtures, and validation scripts.

Company-specific rules and personal notes belong in overlay repositories. An
overlay adds its own catalog fragment and references while inheriting this core;
it should not modify upstream-owned files.

## Validate a checkout

From the repository root, run:

```bash
python3 harness/scripts/validate.py --root .
python3 harness/scripts/route_regression.py --root .
```

The checks use only files in the checkout and do not require host paths,
credentials, external services, or a live Codex runtime.
