#!/usr/bin/env python3
"""Validate the instruction catalog, reference metadata, and regression fixtures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit("PyYAML is required: run this script in an environment that provides the yaml module") from exc

ALLOWED_OWNERS = {"company", "personal", "public"}
ALLOWED_AUTHORITIES = {"hard", "heuristic"}
ALLOWED_STATUSES = {"current", "deprecated"}
ALLOWED_EVIDENCE = {"company", "target-repo", "workspace/domain", "task", "repository"}
FORBIDDEN_PATTERNS = {
    "personal absolute path": re.compile(r"/(?:Users|home|private/tmp|var/folders)/"),
    # Split the literal so the scanner does not flag this pattern's own source.
    "home-relative path": re.compile(r"(?<![\w`])~" + r"/"),
    "URL": re.compile(r"(?i)\bhttps?://"),
    "credential-like token": re.compile(r"\b(?:sk|cr|ghp|xox[baprs])-[-_A-Za-z0-9]{12,}\b"),
    "bearer credential": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]{12,}"),
}


def load_yaml(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"{path}: cannot parse YAML: {exc}") from exc


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    return require_mapping(yaml.safe_load(text[4:end]) or {}, f"{path} frontmatter")


def require_mapping(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected a mapping")
    return value


def validate_entry(entry, label):
    require_mapping(entry, label)
    for key in ("id", "owner", "authority", "status", "applies_to"):
        if key not in entry:
            raise ValueError(f"{label}: missing {key}")
    if not isinstance(entry["id"], str) or not entry["id"].strip():
        raise ValueError(f"{label}: id must be a non-empty string")
    if entry["owner"] not in ALLOWED_OWNERS:
        raise ValueError(f"{label}: invalid owner {entry['owner']!r}")
    if entry["authority"] not in ALLOWED_AUTHORITIES:
        raise ValueError(f"{label}: invalid authority {entry['authority']!r}")
    if entry["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"{label}: invalid status {entry['status']!r}")
    applies = require_mapping(entry["applies_to"], f"{label}.applies_to")
    for key in ("company", "domain", "task"):
        if key in applies and not isinstance(applies[key], list):
            raise ValueError(f"{label}.applies_to.{key}: expected a list")
    for key in ("requires_evidence", "excludes"):
        if key in entry and not isinstance(entry[key], list):
            raise ValueError(f"{label}.{key}: expected a list")
    for evidence in entry.get("requires_evidence", []):
        if evidence not in ALLOWED_EVIDENCE:
            raise ValueError(f"{label}.requires_evidence: invalid value {evidence!r}")
    if "depends_on" in entry:
        deps = entry["depends_on"]
        if not isinstance(deps, list) or len(deps) > 1 or any(not isinstance(dep, str) for dep in deps):
            raise ValueError(f"{label}.depends_on: at most one string dependency is allowed")


def catalog_paths(root: Path):
    refs_root = root / "agent-references"
    legacy = refs_root / "catalog.yaml"
    fragments = sorted((refs_root / "catalog.d").glob("*.yaml")) if (refs_root / "catalog.d").is_dir() else []
    paths = ([legacy] if legacy.is_file() else []) + fragments
    if not paths:
        raise ValueError(f"{refs_root}: no catalog found; add catalog.yaml or catalog.d/*.yaml")
    return paths


def validate_catalog(root: Path):
    paths = catalog_paths(root)
    ids = set()
    referenced_paths = set()
    entries = []
    merged = {"schema_version": None, "entries": entries}
    refs_root = (root / "agent-references").resolve()
    for path in paths:
        doc = require_mapping(load_yaml(path), str(path))
        if not isinstance(doc.get("schema_version"), int):
            raise ValueError(f"{path}: schema_version must be an integer")
        if merged["schema_version"] is None:
            merged["schema_version"] = doc["schema_version"]
        elif merged["schema_version"] != doc["schema_version"]:
            raise ValueError(f"{path}: schema_version disagrees with other catalog fragments")
        fragment_entries = doc.get("entries")
        if not isinstance(fragment_entries, list):
            raise ValueError(f"{path}: entries must be a list")
        for index, entry in enumerate(fragment_entries):
            label = f"{path} entry {index + 1}"
            validate_entry(entry, label)
            entry_id = entry["id"]
            if entry_id in ids:
                raise ValueError(f"{label}: duplicate id {entry_id}")
            ids.add(entry_id)
            entries.append(entry)
            if "path" in entry:
                relative = entry["path"]
                if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
                    raise ValueError(f"{label}: path must be a relative repository path")
                ref = (refs_root / relative).resolve()
                if refs_root not in ref.parents:
                    raise ValueError(f"{label}: path escapes references directory: {relative!r}")
                if ref.suffix != ".md":
                    raise ValueError(f"{label}: runtime reference path must end in .md: {relative!r}")
                if relative in referenced_paths:
                    raise ValueError(f"{label}: duplicate path {relative!r}")
                referenced_paths.add(relative)
                if not ref.is_file():
                    raise ValueError(f"{label}: referenced file not found: {ref}")
                owner = entry["owner"]
                if owner in {"company", "personal"} and Path(relative).parts[0] != owner:
                    raise ValueError(f"{label}: {owner} entry must live under {owner}/: {relative!r}")
                metadata = frontmatter(ref)
                for key in ("id", "owner", "authority", "status"):
                    if metadata.get(key) != entry.get(key):
                        raise ValueError(
                            f"{label}: {key} disagrees with {ref} "
                            f"({entry.get(key)!r} != {metadata.get(key)!r})"
                        )
                if metadata.get("applies_to") != entry.get("applies_to"):
                    raise ValueError(f"{label}: applies_to disagrees with {ref}")
    actual_paths = {
        str(file.relative_to(refs_root))
        for file in refs_root.rglob("*.md")
        if file.is_file()
    }
    if actual_paths != referenced_paths:
        missing = sorted(actual_paths - referenced_paths)
        dangling = sorted(referenced_paths - actual_paths)
        raise ValueError(f"{refs_root}: catalog path set disagrees with runtime files; unindexed={missing}, missing={dangling}")
    by_id = {entry["id"]: entry for entry in entries}
    for entry in entries:
        for dep in entry.get("depends_on", []):
            if dep not in ids:
                raise ValueError(f"{refs_root}: {entry['id']} depends on unknown id {dep}")
            if dep == entry["id"]:
                raise ValueError(f"{refs_root}: {entry['id']} cannot depend on itself")
            if by_id[dep].get("depends_on"):
                raise ValueError(f"{refs_root}: {entry['id']} has a transitive dependency through {dep}")
    return doc, ids


def validate_fixture_catalog(path: Path):
    doc = require_mapping(load_yaml(path), str(path))
    if not isinstance(doc.get("schema_version"), int):
        raise ValueError(f"{path}: schema_version must be an integer")
    entries = doc.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{path}: entries must be a list")
    ids = set()
    for index, entry in enumerate(entries):
        label = f"{path} entry {index + 1}"
        validate_entry(entry, label)
        if entry["id"] in ids:
            raise ValueError(f"{label}: duplicate id {entry['id']}")
        ids.add(entry["id"])
        if "depends_on" in entry:
            deps = entry["depends_on"]
            if not isinstance(deps, list) or len(deps) > 1 or any(not isinstance(dep, str) for dep in deps):
                raise ValueError(f"{label}.depends_on: at most one string dependency is allowed")
    by_id = {entry["id"]: entry for entry in entries}
    for entry in entries:
        for dep in entry.get("depends_on", []):
            if dep not in ids:
                raise ValueError(f"{path}: {entry['id']} depends on unknown id {dep}")
            if by_id[dep].get("depends_on"):
                raise ValueError(f"{path}: {entry['id']} has a transitive dependency through {dep}")
    return doc, ids


def validate_cases(path: Path, fixture_ids):
    doc = require_mapping(load_yaml(path), str(path))
    cases = doc.get("cases")
    if not isinstance(cases, list):
        raise ValueError(f"{path}: cases must be a list")
    case_ids = set()
    for index, case in enumerate(cases):
        label = f"{path} case {index + 1}"
        require_mapping(case, label)
        case_id = case.get("case_id")
        if not case_id or case_id in case_ids:
            raise ValueError(f"{label}: missing or duplicate case_id {case_id!r}")
        case_ids.add(case_id)
        task = require_mapping(case.get("task"), f"{label}.task")
        if not task.get("intent") or not task.get("domain"):
            raise ValueError(f"{label}.task: intent and domain are required")
        if "topics" in task and not isinstance(task["topics"], list):
            raise ValueError(f"{label}.task.topics: expected a list")
        env = require_mapping(case.get("environment"), f"{label}.environment")
        for key in ("workspace_domain", "target_repo", "source_repo", "remote_company"):
            if not env.get(key):
                raise ValueError(f"{label}.environment: {key} is required")
        if not isinstance(env.get("reference_repos", []), list):
            raise ValueError(f"{label}.environment.reference_repos: expected a list")
        expected = require_mapping(case.get("expected"), f"{label}.expected")
        for key in ("route_status", "company", "target_repo", "reference_only", "load", "exclude"):
            if key not in expected:
                raise ValueError(f"{label}.expected: missing {key}")
        if expected["route_status"] not in {"confirmed", "provisional", "blocked"}:
            raise ValueError(f"{label}: invalid route_status")
        for key in ("load", "exclude"):
            if not isinstance(expected[key], list):
                raise ValueError(f"{label}.expected.{key}: expected a list")
            if any(not isinstance(item, str) for item in expected[key]):
                raise ValueError(f"{label}.expected.{key}: IDs must be strings")
            unknown = set(expected[key]) - fixture_ids
            if unknown:
                raise ValueError(f"{label}.expected.{key}: unknown ids {sorted(unknown)}")
        if not isinstance(expected["reference_only"], list):
            raise ValueError(f"{label}.expected.reference_only: expected a list")
        if any(not isinstance(repo, str) for repo in expected["reference_only"]):
            raise ValueError(f"{label}.expected.reference_only: repository IDs must be strings")
        if expected["target_repo"] != env["target_repo"]:
            raise ValueError(f"{label}: expected.target_repo must equal environment.target_repo")
        if "maintenance_docs_loaded" in expected and not isinstance(expected["maintenance_docs_loaded"], bool):
            raise ValueError(f"{label}.expected.maintenance_docs_loaded: expected a boolean")
        load = set(expected["load"])
        exclude = set(expected["exclude"])
        if load & exclude:
            raise ValueError(f"{label}: load and exclude overlap: {sorted(load & exclude)}")
        if load | exclude != fixture_ids:
            uncovered = sorted(fixture_ids - (load | exclude))
            unknown = sorted((load | exclude) - fixture_ids)
            raise ValueError(f"{label}: load/exclude must partition fixture IDs; uncovered={uncovered}, unknown={unknown}")
        refs = set(env.get("reference_repos", []))
        if any(not isinstance(repo, str) or not repo for repo in refs):
            raise ValueError(f"{label}: reference_repos must contain non-empty strings")
        if env["target_repo"] in refs:
            raise ValueError(f"{label}: target_repo is also reference-only")
        if set(expected["reference_only"]) != refs:
            raise ValueError(f"{label}: expected.reference_only must equal environment.reference_repos")
    return doc


def scan_redaction(root: Path):
    paths = [root / "AGENTS.md"]
    for directory in (root / "agent-references", root / "docs", root / "harness"):
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file())
    findings = []
    for path in paths:
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path}: {name}")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        real_catalog, real_ids = validate_catalog(root)
        fixture_catalog, fixture_ids = validate_fixture_catalog(root / "harness/fixtures/catalog.yaml")
        validate_cases(root / "harness/fixtures/routing-cases.yaml", fixture_ids)
        findings = scan_redaction(root)
        if findings:
            raise ValueError("redaction check failed:\n" + "\n".join(findings))
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: runtime catalog ({len(real_ids)} entries)")
    print(f"PASS: fixture catalog ({len(fixture_ids)} entries)")
    print("PASS: routing cases and redaction checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
