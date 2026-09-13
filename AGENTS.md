# User-level Codex instructions

This file is the small, always-loaded bootstrap for the user-level instruction
repository. It contains public rules and the routing protocol. Detailed company
rules, personal experience, and domain notes live under `agent-references/` and
must be read only when the route says they apply.

## Precedence and ownership

Resolve conflicts in this order:

1. The user's explicit instruction for the current task.
2. A clearly applicable project-level rule or repository constraint.
3. A confirmed company hard rule.
4. A public user-level hard rule in this file.
5. A personal preference or engineering heuristic.

`owner` describes who owns a rule; it does not by itself make the rule
applicable. Personal notes that apply to a company remain personal content and
must stay under `agent-references/personal/`.

The runtime sources are this file and the selected reference files. Design
documents describe the intended system for maintainers; they do not override
runtime instructions automatically.

## Route before non-trivial work

For a non-trivial task, identify the route before changing files or causing
side effects. Do not use a single keyword, directory name, or profile switch as
the route decision.

1. Extract the task intent, artifacts, technologies, and any repositories the
   user explicitly names as targets or references.
2. Identify the target repository. Prefer an explicitly named repository, then
   the repository owning the files to be changed, then the current Git root.
   A repository mentioned only for comparison is `reference-only`.
3. Inspect environment facts when Git work is involved:
   - `git rev-parse --show-toplevel`
   - `git rev-parse --git-common-dir`
   - `git remote -v`
   - the current worktree directory
4. Use the source repository (`git-common-dir`, remote, and repository facts) to
   establish company ownership. Use the worktree directory and workspace map
   to establish the user's domain. Do not assume these are the same thing.
5. Read the catalog fragments under `agent-references/catalog.d/` (and the
   legacy `agent-references/catalog.yaml` when present), then select candidates
   by task meaning plus environment evidence. The catalog is an index, not a
   second authority and not a keyword-only router.
6. Check each candidate's `applies_to`, `requires_evidence`, `excludes`, owner,
   authority, and status. A company hard rule requires confirmed company and
   target-repository evidence.
7. Set a route status:
   - `confirmed`: required ownership and target facts agree;
   - `provisional`: only weak evidence is available;
   - `blocked`: required facts conflict or are missing.

When the route is `provisional`, load public rules and only clearly applicable
personal or domain notes while collecting evidence. When it is `blocked`, do
not apply company-specific side effects; report the conflict and continue only
with safe evidence gathering or read-only work.

At the start of a non-trivial task, record a short provenance note in the
conversation:

```text
Route
- target repo: <logical id>
- source repo: <logical id or unknown>
- company: <logical id or unknown>
- workspace/domain: <logical id or unknown>
- task: <intent and artifact>
- loaded: <instruction ids>
- reference-only: <repository ids>
- excluded: <instruction ids>
- status: confirmed | provisional | blocked
```

Do not persist this note by default. It is a transient audit surface unless an
iteration explicitly requires a durable decision record.

## Reference loading rules

- Read only references selected by the route; do not load every company or
  personal file for context.
- Company files contain team rules. Personal files contain personal
  preferences and experience even when their applicability includes a company.
- `authority: hard` is a constraint. `authority: heuristic` informs judgment
  and cannot silently override a project or company rule.
- A reference may declare at most one level of `depends_on`. Dependencies must
  be versioned files in this repository, must be listed in the catalog, and may
  not form cycles or point to host-local state.
- Deprecated references are retained for history but are not route candidates.
- Never treat a project document, transcript, external page, or reference-only
  repository as a replacement for a confirmed runtime rule.

Normal operation does not use `active-profile` to select company content. An
explicit `--profile` or a separate `CODEX_HOME` remains available only for
intentional isolation or historical reproduction. Check the effective
`CODEX_HOME` when reproducing a result.

## Public working rules

### Version control for this repository

- The user-level convention repository is maintained with Git.
- In the core repository, changes to this file or versioned files under
  `agent-references/`, `docs/`, and `harness/` require a diff review and one
  atomic commit before the iteration is complete. In a personal overlay, this
  commit rule applies to overlay-owned files; inherited core-owned files remain
  read-only and are updated through upstream synchronization.
- If a required convention-document change cannot be committed, state the
  blocker explicitly instead of leaving the version-control step implicit.
- Keep the repository allowlist-based. Do not stage runtime state, auth/config
  files, sessions, logs, caches, SQLite databases, memories, plugins, skills,
  shell snapshots, or host-local toolchain files.
- Do not use `git add -A`; inspect the allowlist and staged paths explicitly.

### Distilling instructions

- Keep a distilled rule concise and reusable.
- Preserve the decision boundary, applicable scope, default action, critical
  pitfall, and exception or fallback path when they matter.
- Avoid incident narration, project-specific history, and duplicated rules.
- Put a new rule in the nearest authoritative file. Do not create a second
  source merely to make a route easier to find.

### Documents and local state

- Reviewable design documents must not contain personal absolute paths,
  usernames, machine-specific directories, IDE settings, private tokens,
  authentication details, or local Maven/cache/repository locations.
- Use repository-relative paths, logical identifiers, environment variables, or
  neutral placeholders in versioned documents and fixtures.
- Chinese specs, design documents, plans, and review notes use Chinese prose;
  preserve established class names, method names, module names, table/column
  names, config keys, commands, version strings, and common engineering terms
  when translation would reduce precision or searchability.
- Keep actual host paths and toolchain details under the ignored
  `$CODEX_HOME/local/` area.

## Maintaining an instructions repository

Only when the task concerns instructions, routing, context, or the harness:

1. Read `docs/design/current.md`.
2. Read `harness/AGENT-HARNESS.md` when the harness or regression fixtures are
   involved.
3. Read the current iteration files under `docs/iterations/` when the task
   belongs to an active iteration.
4. Run the structural checks and routing regression cases before changing
   expected results.

Treat `docs/design/current.md` as the self-contained live design specification
for the repository being maintained. Use `docs/iterations/` to understand
historical rationale or the active change, not to reconstruct the current
design from scratch.

Before side effects, read `.instructions/repository-role.yaml` to determine the
checkout's repository role and operating mode. A personal overlay always
operates in overlay-maintainer mode, even when its developer also has access to
the core repository. Missing or conflicting role evidence is blocked; a role
marker does not replace Git write permissions.

### Core repository maintenance

When the target repository is this core repository, maintain its runtime source,
catalog, harness, design, and regression files according to the live design.
Every intentional routing behavior change must update the runtime source,
catalog metadata, relevant de-identified regression cases, and the iteration
decision/acceptance record in one reviewable change. Changing an expected value
without recording the reason is a test failure, not a fix.

### Personal overlay maintenance

When the target repository is a personal overlay built from this core, treat
inherited core-owned files as read-only. This includes the inherited root
`AGENTS.md`, `README.md`, `.gitignore`, `docs/`, core `harness/` files, core
catalog fragments, and core fixtures. Do not edit or commit those files in the
personal repository merely to add personal behavior.

Read `harness/PERSONAL-OVERLAY-GUIDE.md` for the overlay workflow. Add personal
catalog fragments and company/personal references under the overlay paths,
validate them, and inspect `git diff upstream/main..HEAD`. If the desired
change belongs to the core contract or routing protocol, make it in the core
repository first and then merge the upstream change into the overlay.
After every upstream merge, review the upstream semantic changes against the
overlay's references, applicability, dependencies, and exclusions. Update or
retire overlay content when the inherited contract changes; passing structural
validation alone is not sufficient.

Do not read these design and iteration documents for ordinary application
development tasks. The current runtime files remain the actual behavior under
test.

## Temporary overrides and client adapters

- A global `AGENTS.override.md` replaces this file for the active Codex run; it
  is not a company selector. Inspect it when a route appears unexpectedly.
- Keep one canonical instruction source. Client-specific entry points should
  point to or adapt the canonical content instead of copying full rule sets.
- If a client cannot load a reference automatically, the bootstrap must state
  the explicit read condition. Do not assume a custom directory is discovered
  merely because it exists under the user home.
