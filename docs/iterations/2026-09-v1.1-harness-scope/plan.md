---
iteration: 2026-09-v1.1-harness-scope
release_target: instructions/v1.1.0
status: complete
---

# Harness scope correction

## Goal

Keep the user-level instructions harness from being applied to ordinary
projects that happen to maintain skills, context, or project instructions.

## Scope

- Narrow the repository-role and harness-maintenance procedures to the core
  harness repository and its personal overlays.
- Clarify that ordinary projects use their own project-level instructions.
- Add an abstract regression case for a project that ships skills.

## Out of scope

- Changes to project-level `AGENTS.md` files outside this harness.
- Changes to company or personal reference applicability.
- Automatic detection of every possible project type.

## Completion criteria

- The live design and bootstrap state the harness-only boundary.
- The agent manual does not imply inheritance by ordinary projects.
- Regression proves that an application repository with an instruction-related
  task does not load harness maintenance documents.
