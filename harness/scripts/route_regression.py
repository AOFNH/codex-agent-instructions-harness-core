#!/usr/bin/env python3
"""Run deterministic route invariants against the abstract fixture catalog."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: run this script in an environment that provides the yaml module") from exc


def load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def known(value):
    return value not in (None, "", "unknown")


def resolve_route(env):
    explicit = env.get("explicit_company")
    remote = env.get("remote_company")
    if known(explicit) and known(remote) and explicit != remote:
        return "blocked", "conflict"
    company = explicit if known(explicit) else remote if known(remote) else "unknown"
    if not known(company):
        return "provisional", "unknown"
    return "confirmed", company


def applies(entry, task, company, status):
    if entry.get("status") != "current":
        return False
    applies_to = entry.get("applies_to", {})
    companies = applies_to.get("company", [])
    domains = applies_to.get("domain", [])
    tasks = applies_to.get("task", [])
    if company not in companies or task.get("domain") not in domains:
        return False
    task_tokens = {task.get("intent"), *task.get("topics", [])}
    if not task_tokens.intersection(tasks):
        return False
    if entry.get("authority") == "hard" and status != "confirmed":
        return False
    if "target-repo" in entry.get("requires_evidence", []) and status != "confirmed":
        return False
    return True


def maintenance_docs_loaded(case):
    """Model the harness-only maintenance loading boundary from AGENTS.md."""
    task = case["task"]
    environment = case["environment"]
    if environment.get("repository_kind") not in {"core", "personal-overlay"}:
        return False
    tokens = {task.get("intent"), task.get("domain"), *task.get("topics", [])}
    return bool(tokens.intersection({"instructions", "routing", "context", "harness"}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        catalog = load(root / "harness/fixtures/catalog.yaml")
        cases = load(root / "harness/fixtures/routing-cases.yaml")["cases"]
    except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"FAIL: cannot load fixtures: {exc}", file=sys.stderr)
        return 1
    entries = catalog["entries"]
    failures = []
    for case in cases:
        env = case["environment"]
        task = case["task"]
        expected = case["expected"]
        status, company = resolve_route(env)
        predicted = {
            entry["id"]
            for entry in entries
            if applies(entry, task, company, status)
        }
        excluded = {entry["id"] for entry in entries} - predicted
        actual = {
            "route_status": status,
            "company": company,
            "target_repo": env.get("target_repo"),
            "reference_only": sorted(env.get("reference_repos", [])),
            "load": sorted(predicted),
            "exclude": sorted(excluded),
        }
        for key in ("route_status", "company", "target_repo", "reference_only", "load", "exclude"):
            expected_value = expected[key]
            if isinstance(expected_value, list):
                expected_value = sorted(expected_value)
            if actual[key] != expected_value:
                failures.append(
                    f"{case['case_id']}: {key}: expected {expected_value!r}, got {actual[key]!r}"
                )
        if "maintenance_docs_loaded" in expected:
            actual_maintenance = maintenance_docs_loaded(case)
            if actual_maintenance != expected["maintenance_docs_loaded"]:
                failures.append(
                    f"{case['case_id']}: maintenance_docs_loaded: expected "
                    f"{expected['maintenance_docs_loaded']!r}, got {actual_maintenance!r}"
                )
        if status == "blocked" and predicted:
            failures.append(f"{case['case_id']}: blocked route predicted hard-rule loads {sorted(predicted)}")
    if failures:
        print("FAIL: route regression", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS: {len(cases)} abstract route cases")
    print("PASS: target/reference, source/worktree, evidence status, ownership, and task scope invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
