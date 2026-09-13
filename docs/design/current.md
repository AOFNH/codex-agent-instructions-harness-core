---
title: Live Design Specification — User-level Agent Instructions and Context Architecture
document_kind: normative-current-design
audience: agents and maintainers
status: current
contract_version: 1.0.0
last_updated: 2026-09-13
---

# User-level Agent Instructions and Context Architecture

## 1. Purpose and boundary

This project maintains user-level instructions, personal experience notes, and
routing validation for multiple agent clients. It is not a replacement for a
business project and is not a runtime configuration center.

The runtime sources of truth are:

- root `AGENTS.md`: public hard rules, routing protocol, and loading boundary;
- `agent-references/`: company rules, personal notes, and domain content selected
  by the route;
- the target project's `AGENTS.md`, code, and configuration: project facts and
  local constraints.

`docs/` serves maintainers and agents performing instructions maintenance. This
file is the self-contained, normative description of the design currently in
effect. Iteration records preserve historical intent, decisions, and acceptance
evidence; version control does not make any document runtime instructions
automatically.

## 2. Four content classes

| Class | Owner | Typical location | Default behavior |
|---|---|---|---|
| Public rules | Personal public | root `AGENTS.md` | Loaded globally |
| Company rules | Company | `agent-references/company/` | Loaded only after company evidence is confirmed |
| Personal notes | Personal | `agent-references/personal/` | Selected by task and applicability |
| Project rules and context | Project team | project `AGENTS.md` and other project-defined context files | Loaded by project mechanisms |

Applicability to a company does not change ownership. Experience collected by a
person while working on a company project remains personal content.

Host paths, toolchains, authentication state, caches, and other host facts are
local state. They do not enter versioned instructions, design documents, or
fixtures.

## 3. Routing model

Routing uses two stages: semantic candidate discovery followed by environmental
fact confirmation. It does not use a single keyword table or `active-profile`
as a company switch.

### 3.0 Repository roles and agent operating modes

Every checkout declares its repository role under `.instructions/`:

- `.instructions/repository.yaml` identifies the inherited core as
  `repository_kind: core` with `core_change_authority: maintainer-only`;
- a personal overlay adds `.instructions/overlay.yaml` with
  `repository_kind: personal-overlay` and `core_change_authority: none`.

The overlay marker takes precedence for a personal checkout; the inherited core
marker remains read-only. An agent operating in a core checkout uses
`core-maintainer` mode. An agent operating in a personal checkout uses
`overlay-maintainer` mode and may edit only overlay-owned files. A person having
core developer access does not turn a personal checkout into a core checkout;
core changes still happen in the core repository.

Role metadata is a routing and safety declaration, not proof of write access.
Before a side effect, the agent must confirm the marker, target repository,
source repository, remotes, and the user's explicit task. Conflicting or
missing evidence is `blocked`. Git hosting permissions and branch protection
remain the final authority for core writes.

### 3.1 Target and reference repositories

Evidence priority for the target repository:

```text
repository explicitly named for modification by the user
> repository owning the target files
> current Git root
```

A repository used only for comparison, migration, or verification is marked
`reference-only`. It cannot change the target repository's company ownership
or rule set.

### 3.2 Company and workspace/domain

Evidence priority for company ownership:

```text
user's explicit statement
> source repo remote, git-common-dir, and repository facts
> project context
> workspace path
> keywords or directory names
```

The current worktree location is the main evidence for workspace/domain and is
combined with task semantics. A worktree path and a source-repository path
represent different dimensions and cannot substitute for one another.

### 3.3 Route status

- `confirmed`: target repository, source repository, remote, and task semantics
  agree; applicable company hard rules may be loaded.
- `provisional`: only weak evidence is available; load public rules and clearly
  applicable personal/domain notes while collecting evidence.
- `blocked`: required facts are missing or conflict; do not perform side effects
  that depend on company ownership. Continue only with safe evidence gathering
  or read-only work.

Every non-trivial task should report target repo, source repo, company,
workspace/domain, loaded references, reference-only repositories, excluded
references, and status in the conversation.

## 4. Reference metadata

`agent-references/catalog.d/*.yaml` contains mergeable candidate-index
fragments. `agent-references/catalog.yaml` remains supported for the legacy
layout. The catalog is an index, not a second business authority. Each
candidate describes at least:

```yaml
id: personal.company-a-experience
owner: personal
authority: heuristic
status: current
applies_to:
  company: [company-a]
  domain: [backend]
  task: [review, concurrency]
requires_evidence: [company]
excludes: [reference-only]
```

Rules:

- `owner` distinguishes company and personal ownership;
- `authority: hard` expresses a constraint, while `heuristic` informs judgment;
- `status: deprecated` files are retained for history and are not route
  candidates;
- a missing `requires_evidence` condition prevents loading;
- a reference may have at most one `depends_on` level, and dependencies must be
  registered in this repository without cycles;
- references may not depend on host-local files, the current branch, or
  unregistered documents.

## 5. Official mechanism boundary

Codex global scope automatically reads only the first non-empty
`AGENTS.override.md` or `AGENTS.md`; project scope merges files along the path
from Git root to the current directory. Custom `agent-references/` files are
not discovered automatically and must be explicitly requested by the bootstrap
rules.

The official default project-instruction merge limit is 32 KiB. Official
documentation does not define directory depth as a quality limit; in practice,
control root-file size, candidate count, and explicit read count.

`AGENTS.override.md` is a temporary same-level replacement, not a company
selector. `--profile` and a separate `CODEX_HOME` are reserved for intentional
isolation or historical reproduction.

## 6. Versions and lifecycle

Manage three version dimensions separately:

- `contract_version`: compatibility version for this design and routing
  protocol;
- `schema_version`: data-structure version for the catalog and harness
  fixtures;
- Git release tag: reproducible snapshot of a complete instruction set, for
  example `instructions/v1.0.0`.

Daily routing uses the current branch and does not depend on tags. To reproduce
historical behavior, check out the relevant tag and use an isolated
`CODEX_HOME`.

An iteration that changes routing behavior must update runtime files, catalog,
de-identified fixtures, design documents, and acceptance records together. A
repair that does not change behavior may update only implementation and
verification records.

## 7. Iterations and sources of truth

Core and personal overlays have different maintenance ownership. Core changes
to the bootstrap, routing protocol, shared catalog, harness, fixtures, or live
design are made in the core repository and then merged by overlays. An overlay
may add its own catalog fragments and company/personal references, but inherited
core-owned files remain read-only there. The boundary is checked with
`git diff upstream/main..HEAD`.

Work on each instructions iteration in an isolated branch or worktree:

1. Read this file, the current iteration record, and relevant harness manual.
2. Modify runtime files or test data.
3. Run structural checks and routing regression.
4. Review de-identification, the allowlist, and the complete diff.
5. Save implementation, tests, and decisions in one atomic commit.
6. Create a tag only when a snapshot must be released.

`docs/design/current.md` is the live maintenance contract and should be
understood without reconstructing every historical iteration. `docs/iterations/`
stores historical decisions, plans, and acceptance evidence. Historical
documents do not override the live design or current runtime rules
automatically.

## 8. Quality boundary

The harness can prevent regressions in known routing scenarios. It cannot prove
that every natural-language task will route correctly. Update regression
expected values only after an explicit strategy change and a decision record.

Versioned documents and fixtures must be de-identified. They must not contain
confidential company details, user identities, personal paths, credentials,
private URLs, or device state. Directory separation within one Git repository is
not a security boundary; where company access boundaries exist, split the
repositories or use isolated `CODEX_HOME` directories.
