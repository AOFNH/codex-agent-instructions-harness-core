---
iteration: 2026-09-v1.1-harness-scope
release_target: instructions/v1.1.0
status: complete
---

# Decisions

## D1: Harness maintenance is repository-scoped

The role manifest, harness design documents, and core/overlay maintenance
procedures apply only to the user-level instructions harness repositories.
Task vocabulary alone cannot activate them in an ordinary project.

This prevents a project such as a skills package from being mistaken for a
personal overlay and being blocked on a role marker it should never contain.

## D2: Keep the project boundary explicit in regression

The regression fixture models a skills project with an instruction-related task
and expects no harness maintenance documents. This preserves the boundary
without relying on real repository names or paths.
