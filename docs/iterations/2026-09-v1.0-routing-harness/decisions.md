---
iteration: 2026-09-v1.0-routing-harness
release_target: instructions/v1.0.0
status: complete
---

# Iteration Decision Record

## D1: Do not use `active-profile` to route company content

**Decision:** Daily routing uses task semantics, target repository, source
repository, remote, worktree, and workspace/domain. A profile is reserved for
explicit isolation or historical reproduction.

**Reason:** Company ownership is part of task context, not a global mode that
the user should switch manually. A profile also mixes model, permission, and
instruction selection.

## D2: Use different evidence for company ownership and workspace/domain

**Decision:** The source repository and remote primarily confirm company
ownership; the current worktree primarily confirms workspace/domain. Do not
silently guess when the evidence conflicts.

**Reason:** A Git worktree can have a different path from its source repository.
Looking only at either path can route a task incorrectly.

## D3: Require `confirmed` status for company hard rules

**Decision:** Load company hard rules only after company and target-repository
evidence is confirmed. In `provisional`, load public rules and clearly
applicable personal/domain notes. In `blocked`, prohibit side effects that
depend on company ownership.

**Reason:** Every reference requires an explicit read, and semantic judgment
alone cannot ensure that hard rules are neither missed nor mixed across
companies.

## D4: Separate design documents from runtime files

**Decision:** Maintainers read `docs/design/current.md` and `docs/iterations/`.
Runtime facts come only from the root `AGENTS.md`, selected references, and
project-level files.

**Reason:** Design history must not become a second runtime authority or add
context cost to ordinary development tasks.

## D5: Use an abstract environment in regression fixtures

**Decision:** Fixtures store only logical repositories, synthetic companies,
workspace/domain, task intent, and expected route sets. They do not store actual
device state.

**Reason:** Device paths and current remotes change and cannot provide a durable
quality baseline. The problem structure is sufficient to test routing boundaries.

## D6: Do not create an independent version system for every reference

**Decision:** Catalog and harness use schema versions; the complete instruction
set uses Git release tags; the design contract uses a contract version.

**Reason:** Multiple independent semantic versions create ambiguity about which
version is active. Git commits are the fine-grained source of truth, while a tag
represents a complete snapshot.

## D7: Assert complete regression results

**Decision:** Every fixture provides complete `load` and `exclude` sets. The
regression script also asserts whether maintenance documents are loaded.

**Reason:** Checking only loaded references misses accidental loads. Without the
maintenance-document assertion, ordinary development tasks can silently gain
the harness context. Complete sets expose new candidates and routing changes
immediately.

## D8: Keep development experience out of the public bootstrap

**Decision:** The root `AGENTS.md` contains only the public protocol for this
instructions repository. Rules distilled from specific development scenarios,
such as dynamic configuration, scheduler controls, and concurrency boundaries,
belong in the applicable personal or company references. Overlay repositories
maintain their own catalog fragments.

**Reason:** Such rules depend on a company's development practices, technology
stack, and operating platform. Putting them in the global bootstrap burdens
unrelated projects and creates a duplicate authority with personal/company
references.
