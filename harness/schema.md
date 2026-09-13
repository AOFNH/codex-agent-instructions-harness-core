# Harness Data Contract

## Purpose

`fixtures/` stores de-identified, portable routing regression data. It tests
routing boundaries without copying any device's current path, Git remote, user
identity, or runtime configuration. The reference catalog supports fragments
so upstream and personal overlays can evolve independently.

## Fixture top-level structure

- `schema_version`: fixture data-structure version; increment the major version
  for incompatible changes;
- `cases`: list of regression scenarios;
- `case_id`: stable, unique logical identifier.

## Case structure

### `task`

Stores abstract intent, domain, and topic. Do not put production request text,
real product names, or internal identifiers in a fixture.

### `environment`

All values are logical identifiers:

- `workspace_domain`: user-defined work domain;
- `target_repo`: repository expected to be modified;
- `source_repo`: source repository behind the worktree;
- `remote_company`: company identifier abstracted from the remote;
- `reference_repos`: repositories used only for comparison;
- `explicit_company`: company explicitly named by the user, or `unknown` when
  absent.

Do not use absolute paths, real URLs, usernames, tokens, authentication data,
or current branch names.

### `expected`

The following must be validated:

- `route_status`: `confirmed`, `provisional`, or `blocked`;
- `company`;
- `target_repo`;
- `reference_only`;
- `load` and `exclude` instruction-ID sets.

`load` and `exclude` must cover every fixture-catalog ID exactly once. `load`
is the set this case should load; `exclude` is the set it explicitly must not
load.

Natural-language report wording may differ, but these logical results may not.
When `maintenance_docs_loaded` is present, it must match whether the task is an
instructions-maintenance task.

## Adding a case

1. Extract routing relationships and conflict structure from the real problem.
2. Replace companies, repositories, paths, and products with stable synthetic
   identifiers.
3. Delete the original transcript, logs, screenshots, and host configuration.
4. Write the expected result and explain it in the iteration decision record.
5. Run structural validation, then routing regression.
6. Do not change expected values only to remove a failure without a decision
   record.
