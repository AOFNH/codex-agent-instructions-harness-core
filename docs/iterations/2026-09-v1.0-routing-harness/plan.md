---
iteration: 2026-09-v1.0-routing-harness
release_target: instructions/v1.0.0
status: complete
---

# Routing and Regression Harness Iteration Plan

## Goal

Restructure user-level instructions into public rules, company rules, personal
notes, and a verifiable routing system. Establish de-identified regression data
and an agent-facing harness manual that do not depend on host state.

## Scope

- Trim the root `AGENTS.md` to public rules, routing protocol, and maintenance
  boundaries.
- Move company rules and personal notes into reference directories with clear
  ownership.
- Establish catalog metadata, lifecycle rules, and one-level dependency
  constraints.
- Establish the current design document and this iteration's decision and
  acceptance records.
- Establish logical, de-identified routing fixtures.
- Establish an agent-facing harness manual and structural validation scripts.

## Out of scope

- Business project code or project-level instructions.
- Production configuration, authentication, browser state, or host Codex
  runtime state.
- A daily `active-profile` company switch.
- Automatic injection of design documents into ordinary development tasks.
- A claim that a small set of semantic examples proves all natural-language
  routing decisions.

## Completion criteria

- Runtime files, catalog, fixtures, design documents, and harness manual have
  clear boundaries.
- Fixtures do not depend on real paths, remotes, user identities, credentials,
  or host files.
- Structural validation detects duplicate IDs, broken references, invalid
  owner/status values, and unredacted identifiers.
- Routing regression covers target/reference repositories, worktree/source-repo
  differences, insufficient company evidence, and personal-note applicability.
- The Git allowlist includes only intended convention, reference, design, and
  harness files.
- Another agent can reproduce the change from a clean checkout by following the
  harness manual.
