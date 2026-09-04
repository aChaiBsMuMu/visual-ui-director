#!/usr/bin/env python3
"""Manage Visual UI Director 2.0 decisions, evidence, scores, and drift."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
WORKSPACE_NAME = ".design-director"
LEGACY_WORKSPACE_NAME = ".visual-ui"
VALID_MODES = {"guided", "reference-led", "direct"}
VALID_PLATFORMS = {"web", "ios", "ipados", "watchos", "android", "wearos", "windows"}
DIMENSIONS = (
    "Visual Identity",
    "Hierarchy",
    "Composition",
    "Spacing Rhythm",
    "Typography",
    "Color Discipline",
    "Imagery Consistency",
    "Component Coherence",
    "Platform Appropriateness",
    "Memorability",
)
SCREEN_THRESHOLDS = {"standard": 80, "key": 85, "hero": 88}
DRIFT_FIELDS = {
    "radius": "Radius drift",
    "brand_color_budget": "Color drift",
    "type_scale": "Type hierarchy drift",
    "imagery_style": "Imagery drift",
    "icon_style": "Icon drift",
    "card_signature": "Component drift",
}
STANDARD_DOCS = {
    "COLOR.md": "# Color\n\nDefine roles, budgets, frequency, priority, prohibitions, state pairs, and platform aliases.\n",
    "TYPOGRAPHY.md": "# Typography\n\nDefine role character, hierarchy, measure, line height, weight contrast, numerics, alignment, and fallbacks.\n",
    "SPACING.md": "# Spacing\n\nDefine micro, component, section, macro, and hero rhythms plus responsive compression.\n",
    "ICONOGRAPHY.md": "# Iconography\n\nDefine family, fill/stroke, weight, corners, optical size, states, containers, labels, and source.\n",
    "IMAGERY.md": "# Imagery\n\nDefine medium, subject, angle, crop, lighting, grade, background, aspect ratios, and fallbacks.\n",
    "MOTION.md": "# Motion\n\nDefine purpose, personality, entry, exit, feedback, transitions, loading, interruption, and reduced motion.\n",
    "COMPONENTS.md": "# Components\n\nDefine content behavior, visual relationships, and required states.\n",
    "RESPONSIVE.md": "# Responsive Composition\n\nDefine focal hierarchy, transformations, and content-failure thresholds by target.\n",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return cleaned or "item"


def workspace(root: str) -> Path:
    return Path(root).expanduser().resolve() / WORKSPACE_NAME


def legacy_workspace(root: str) -> Path:
    return Path(root).expanduser().resolve() / LEGACY_WORKSPACE_NAME


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    except Exception:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
        raise


def atomic_json(path: Path, payload: Any) -> None:
    atomic_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_template(name: str, destination: Path, project: str) -> None:
    content = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
    atomic_text(destination, content.replace("{{PROJECT_NAME}}", project))


def load_workspace(root: str) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    directory = workspace(root)
    if not directory.exists():
        legacy = legacy_workspace(root)
        if legacy.exists():
            raise SystemExit(
                f"Found a 1.x workspace at {legacy}. Run migrate --root {Path(root).resolve()} first."
            )
        raise SystemExit(f"No Visual UI Director workspace at {directory}. Run init first.")
    required = ("project.json", "references.json", "decisions.json")
    missing = [name for name in required if not (directory / name).exists()]
    if missing:
        raise SystemExit(f"Incomplete workspace; missing: {', '.join(missing)}")
    return (
        directory,
        read_json(directory / "project.json"),
        read_json(directory / "references.json"),
        read_json(directory / "decisions.json"),
    )


def save_project(directory: Path, project: dict[str, Any]) -> None:
    project["updated_at"] = now_iso()
    atomic_json(directory / "project.json", project)


def record_event(directory: Path, decisions: dict[str, Any], event: str, details: dict[str, Any]) -> None:
    decisions.setdefault("events", []).append({"at": now_iso(), "event": event, "details": details})
    atomic_json(directory / "decisions.json", decisions)


def init_workspace(
    root: str,
    project_name: str,
    mode: str,
    platforms: list[str],
    main_target_device: str | None,
    force: bool = False,
) -> Path:
    directory = workspace(root)
    if directory.exists() and not force:
        raise SystemExit(f"Workspace already exists at {directory}; use --force only after reviewing it.")
    directory.mkdir(parents=True, exist_ok=True)
    for name in (
        "screenshots", "critiques", "scores", "overrides", "history",
        "standards/v1/evidence", "standards/v1/PLATFORM_OVERRIDES", "standards/v1/PAGE_OVERRIDES",
    ):
        (directory / name).mkdir(parents=True, exist_ok=True)

    direct = mode == "direct"
    created = now_iso()
    project = {
        "schema_version": 2,
        "project_name": project_name,
        "mode": mode,
        "target_platforms": list(dict.fromkeys(platforms)),
        "main_target_device": main_target_device,
        "current_design_version": "v1",
        "quality_threshold": 80,
        "approval_state": {
            "gate_a": "assumed" if direct else "pending",
            "gate_b": "assumed" if direct else "draft",
            "gate_c": "pending",
        },
        "platform_qa": [],
        "created_at": created,
        "updated_at": created,
    }
    references = {
        "primary": None,
        "secondary": [],
        "selected_traits": [],
        "rejected_traits": [],
        "do_not_copy": [],
        "non_negotiables": [],
        "platform_targets": project["target_platforms"],
    }
    decisions = {
        "schema_version": 2,
        "events": [{"at": created, "event": "workspace_initialized", "details": {"mode": mode}}],
    }
    atomic_json(directory / "project.json", project)
    atomic_json(directory / "references.json", references)
    atomic_json(directory / "decisions.json", decisions)
    copy_template("reference-board.md", directory / "reference-board.md", project_name)
    copy_template("reference-contract.md", directory / "REFERENCE_CONTRACT.md", project_name)
    copy_template("visual-dna.md", directory / "visual-dna.md", project_name)
    copy_template("visual-standard.md", directory / "standards/v1/MASTER.md", project_name)
    copy_template("tokens.json", directory / "standards/v1/TOKENS.json", project_name)
    for name, content in STANDARD_DOCS.items():
        atomic_text(directory / "standards/v1" / name, content)
    atomic_text(directory / "standards/current", "v1\n")
    return directory


def init_cmd(args: argparse.Namespace) -> None:
    directory = init_workspace(
        args.root, args.project, args.mode, args.platform, args.main_target_device, args.force
    )
    print(f"Created Visual UI Director 2.0 workspace at {directory}")


def parse_reference(value: str) -> dict[str, str]:
    parts = [part.strip() for part in value.split("|", 1)]
    return {"reference": parts[0], "contribution": parts[1] if len(parts) == 2 else "unspecified"}


def reference_contract(project: dict[str, Any], refs: dict[str, Any], confirmed_by: str) -> str:
    secondary = "\n".join(
        f"- {item['reference']} — {item['contribution']}" for item in refs["secondary"]
    ) or "- None"
    lines = lambda values: "\n".join(f"- {value}" for value in values) or "- None recorded"
    return f"""# {project['project_name']} — Reference Contract

Status: Confirmed
Confirmed by: {confirmed_by}
Confirmed at: {now_iso()}

## Primary Reference

{refs['primary']['reference']}

Contribution: {refs['primary']['contribution']}

## Secondary References

{secondary}

## Selected Traits

{lines(refs['selected_traits'])}

## Rejected Traits

{lines(refs['rejected_traits'])}

## Do Not Copy

{lines(refs['do_not_copy'])}

## Non-negotiables

{lines(refs['non_negotiables'])}

## Platform Targets

{lines(refs['platform_targets'])}
"""


def select_cmd(args: argparse.Namespace) -> None:
    directory, project, _, decisions = load_workspace(args.root)
    secondary = [parse_reference(value) for value in (args.secondary or [])]
    if len(secondary) > 2:
        raise SystemExit("Use no more than two secondary references.")
    refs = {
        "primary": parse_reference(args.primary),
        "secondary": secondary,
        "selected_traits": args.like or [],
        "rejected_traits": args.avoid or [],
        "do_not_copy": args.do_not_copy or [],
        "non_negotiables": args.non_negotiable or [],
        "platform_targets": project["target_platforms"],
        "confirmed_by": args.confirmed_by,
        "confirmed_at": now_iso(),
    }
    atomic_json(directory / "references.json", refs)
    atomic_text(directory / "REFERENCE_CONTRACT.md", reference_contract(project, refs, args.confirmed_by))
    project["approval_state"]["gate_a"] = "confirmed"
    project["approval_state"]["gate_b"] = "draft"
    project["approval_state"]["gate_c"] = "pending"
    save_project(directory, project)
    record_event(directory, decisions, "gate_a_confirmed", {"primary": refs["primary"], "secondary": secondary})
    print("Gate A confirmed and REFERENCE_CONTRACT.md updated.")


def dna_principles(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if re.match(r"^\s*\d+\.\s+\S", line) and "{{" not in line
    ]


def copy_evidence(source: str, destination_dir: Path, label: str) -> str:
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"{label} evidence does not exist: {path}")
    target = destination_dir / f"{slug(label)}{path.suffix.lower()}"
    shutil.copy2(path, target)
    return target.name


def approve_gate_b(args: argparse.Namespace, directory: Path, project: dict[str, Any], decisions: dict[str, Any]) -> None:
    if project["mode"] != "direct" and project["approval_state"]["gate_a"] != "confirmed":
        raise SystemExit("Gate A is not confirmed.")
    principles = dna_principles(directory / "visual-dna.md")
    if not 5 <= len(principles) <= 8:
        raise SystemExit("visual-dna.md must contain 5–8 numbered, non-placeholder principles.")
    version_dir = directory / "standards" / args.version
    master = version_dir / "MASTER.md"
    tokens = version_dir / "TOKENS.json"
    if not master.exists() or not tokens.exists():
        raise SystemExit(f"{version_dir} must contain MASTER.md and TOKENS.json.")
    missing_docs = [name for name in STANDARD_DOCS if not (version_dir / name).exists()]
    if missing_docs:
        raise SystemExit("Design system is missing: " + ", ".join(missing_docs))
    atomic_text(version_dir / "VISUAL_DNA.md", (directory / "visual-dna.md").read_text(encoding="utf-8"))
    evidence_dir = version_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence = {
        "style_tile": copy_evidence(args.style_tile, evidence_dir, "style-tile"),
        "representative_screen": copy_evidence(args.representative_screen, evidence_dir, "representative-screen"),
        "wireframe": copy_evidence(args.wireframe, evidence_dir, "wireframe"),
    }
    atomic_text(directory / "standards/current", args.version + "\n")
    project["current_design_version"] = args.version
    project["approval_state"]["gate_b"] = "confirmed"
    project["approval_state"]["gate_c"] = "pending"
    project["visual_dna_approved"] = True
    project["gate_b_confirmed_by"] = args.confirmed_by
    save_project(directory, project)
    record_event(directory, decisions, "gate_b_confirmed", {"version": args.version, "evidence": evidence})
    print(f"Gate B confirmed for {args.version}.")


def score_files(directory: Path) -> list[Path]:
    return sorted((directory / "scores").glob("*.json"))


def latest_scores(directory: Path) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for path in score_files(directory):
        item = read_json(path)
        latest[item["screen"]] = item
    return latest


def approve_gate_c(args: argparse.Namespace, directory: Path, project: dict[str, Any], decisions: dict[str, Any]) -> None:
    if project["approval_state"]["gate_b"] not in {"confirmed", "assumed"}:
        raise SystemExit("Gate B is not approved.")
    if not 5 <= len(dna_principles(directory / "visual-dna.md")) <= 8:
        raise SystemExit("Gate C requires 5–8 completed Visual DNA principles.")
    if not project.get("visual_dna_approved") and project["mode"] != "direct":
        raise SystemExit("Visual DNA approval is missing.")
    if not any(path.is_file() for path in (directory / "screenshots").iterdir()):
        raise SystemExit("No rendered screenshot evidence found.")
    if not any(path.is_file() for path in (directory / "critiques").iterdir()):
        raise SystemExit("No screenshot critique evidence found.")
    scores = latest_scores(directory)
    if not scores:
        raise SystemExit("No visual-quality scores found.")
    failures = []
    for screen, item in scores.items():
        if item["score"] < item["required_threshold"]:
            failures.append(f"{screen}: {item['score']} < {item['required_threshold']}")
        if item.get("critical_issues"):
            failures.append(f"{screen}: unresolved critical issues")
    if failures:
        raise SystemExit("Gate C score requirements failed: " + "; ".join(failures))
    history_by_screen: dict[str, int] = {}
    for path in score_files(directory):
        item = read_json(path)
        history_by_screen[item["screen"]] = history_by_screen.get(item["screen"], 0) + 1
    needs_rerender = [
        screen
        for screen, item in scores.items()
        if 80 <= item["score"] < 90 and history_by_screen.get(screen, 0) < 2
    ]
    if needs_rerender:
        raise SystemExit("Screens scored 80–89 require a recorded re-render and re-score: " + ", ".join(needs_rerender))
    platform_qa = sorted(set(args.platform_qa or []))
    missing_platforms = sorted(set(project["target_platforms"]) - set(platform_qa))
    if missing_platforms:
        raise SystemExit("Missing platform QA evidence for: " + ", ".join(missing_platforms))
    project["platform_qa"] = platform_qa
    project["known_deviations"] = args.known_deviation or []
    project["approval_state"]["gate_c"] = "confirmed"
    project["gate_c_confirmed_by"] = args.confirmed_by
    project["gate_c_confirmed_at"] = now_iso()
    save_project(directory, project)
    record_event(directory, decisions, "gate_c_confirmed", {"scores": scores, "platform_qa": platform_qa})
    print("Gate C confirmed. The recorded visual implementation meets its delivery threshold.")


def approve_cmd(args: argparse.Namespace) -> None:
    directory, project, _, decisions = load_workspace(args.root)
    if args.gate == "b":
        approve_gate_b(args, directory, project, decisions)
    else:
        approve_gate_c(args, directory, project, decisions)


def parse_dimensions(values: list[str]) -> dict[str, int]:
    normalized = {re.sub(r"[^a-z]", "", name.lower()): name for name in DIMENSIONS}
    result: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Dimension must use NAME=1..5: {value}")
        raw_name, raw_score = value.rsplit("=", 1)
        key = re.sub(r"[^a-z]", "", raw_name.lower())
        if key not in normalized:
            raise SystemExit(f"Unknown dimension: {raw_name}")
        try:
            number = int(raw_score)
        except ValueError as exc:
            raise SystemExit(f"Invalid dimension score: {value}") from exc
        if not 1 <= number <= 5:
            raise SystemExit(f"Dimension score must be 1–5: {value}")
        result[normalized[key]] = number
    missing = [name for name in DIMENSIONS if name not in result]
    if missing:
        raise SystemExit("Missing dimensions: " + ", ".join(missing))
    return result


def score_cmd(args: argparse.Namespace) -> None:
    directory, project, _, decisions = load_workspace(args.root)
    dimensions = parse_dimensions(args.dimension)
    score = sum(dimensions.values()) * 2
    required = max(project.get("quality_threshold", 80), SCREEN_THRESHOLDS[args.screen_type])
    evidence = {
        "screenshot": copy_evidence(args.screenshot, directory / "screenshots", f"{args.screen}-{stamp()}"),
        "critique": copy_evidence(args.critique, directory / "critiques", f"{args.screen}-{stamp()}"),
    }
    payload = {
        "recorded_at": now_iso(),
        "screen": args.screen,
        "target": args.target,
        "screen_type": args.screen_type,
        "dimensions": dimensions,
        "total_50": sum(dimensions.values()),
        "score": score,
        "rating": "Excellent" if score >= 90 else "Strong" if score >= 80 else "Acceptable" if score >= 70 else "Weak" if score >= 60 else "Must Iterate",
        "required_threshold": required,
        "visual_dna_match": args.dna_match,
        "generic_ui_risk": args.generic_risk,
        "platform_fit": args.platform_fit,
        "top_fixes": args.top_fix or [],
        "critical_issues": args.critical_issue or [],
        "evidence": evidence,
        "required_rerender": score < 90 or bool(args.critical_issue),
    }
    path = directory / "scores" / f"{stamp()}-{slug(args.screen)}.json"
    atomic_json(path, payload)
    project["last_score"] = {"screen": args.screen, "score": score, "recorded_at": payload["recorded_at"]}
    project["approval_state"]["gate_c"] = "pending"
    save_project(directory, project)
    record_event(directory, decisions, "visual_score_recorded", {"screen": args.screen, "score": score})
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def override_cmd(args: argparse.Namespace) -> None:
    directory, project, _, decisions = load_workspace(args.root)
    payload = {
        "recorded_at": now_iso(),
        "screen": args.screen,
        "override": args.override,
        "reason": args.reason,
        "scope": args.scope,
        "does_not_change": args.does_not_change or [],
    }
    path = directory / "overrides" / f"{slug(args.screen)}.json"
    atomic_json(path, payload)
    project["approval_state"]["gate_c"] = "pending"
    save_project(directory, project)
    record_event(directory, decisions, "page_override_recorded", payload)
    print(f"Recorded page override at {path}")


def load_overridden_screens(directory: Path) -> set[str]:
    return {read_json(path).get("screen", "") for path in (directory / "overrides").glob("*.json")}


def audit_cmd(args: argparse.Namespace) -> None:
    directory, _, _, decisions = load_workspace(args.root)
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = read_json(manifest_path)
    screens = manifest.get("screens", [])
    if not screens:
        raise SystemExit("Audit manifest must contain a non-empty screens array.")
    names = [item.get("screen") or item.get("name") for item in screens]
    if any(not name for name in names):
        raise SystemExit("Every audit screen requires a screen or name.")
    baseline_name = args.baseline or names[0]
    if baseline_name not in names:
        raise SystemExit(f"Baseline screen not found: {baseline_name}")
    baseline = screens[names.index(baseline_name)]
    overridden = load_overridden_screens(directory)
    findings: list[dict[str, Any]] = []
    for item, name in zip(screens, names):
        for field, label in DRIFT_FIELDS.items():
            if field in baseline and field in item and item[field] != baseline[field] and name not in overridden:
                findings.append({
                    "screen": name,
                    "type": label,
                    "baseline": baseline[field],
                    "observed": item[field],
                    "severity": "medium",
                    "action": "Align with baseline or record a bounded page/platform override.",
                })
        if str(item.get("dna_match", "strong")).lower() not in {"strong", "true"}:
            findings.append({
                "screen": name,
                "type": "Visual DNA drift",
                "baseline": "strong",
                "observed": item.get("dna_match"),
                "severity": "high",
                "action": "Restore the approved Visual DNA or revise it explicitly.",
            })
        if item.get("override_required") and name not in overridden:
            findings.append({
                "screen": name,
                "type": "Unrecorded page override",
                "baseline": "documented override",
                "observed": "missing",
                "severity": "high",
                "action": "Record the exception with the override command.",
            })
    report = {
        "generated_at": now_iso(),
        "baseline_screen": baseline_name,
        "screen_count": len(screens),
        "finding_count": len(findings),
        "status": "drift_detected" if findings else "coherent",
        "findings": findings,
    }
    json_path = directory / "history" / f"{stamp()}-visual-drift.json"
    atomic_json(json_path, report)
    record_event(directory, decisions, "visual_drift_audit", {"finding_count": len(findings), "report": json_path.name})
    print(json.dumps(report, ensure_ascii=False, indent=2))


def status_cmd(args: argparse.Namespace) -> None:
    directory, project, refs, _ = load_workspace(args.root)
    gates = project["approval_state"]
    can_decompose = project["mode"] == "direct" or gates["gate_a"] == "confirmed"
    can_implement = project["mode"] == "direct" or gates["gate_b"] == "confirmed"
    result = {
        "project": project["project_name"],
        "schema_version": project["schema_version"],
        "mode": project["mode"],
        "platforms": project["target_platforms"],
        "main_target_device": project.get("main_target_device"),
        "current_design_version": project["current_design_version"],
        "gates": gates,
        "reference_primary": refs.get("primary"),
        "visual_dna_principles": len(dna_principles(directory / "visual-dna.md")),
        "score_records": len(score_files(directory)),
        "latest_scores": latest_scores(directory),
        "overrides": len(list((directory / "overrides").glob("*.json"))),
        "can_decompose": can_decompose,
        "can_implement": can_implement,
        "can_deliver": gates["gate_c"] == "confirmed",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.require == "decompose" and not can_decompose:
        raise SystemExit(2)
    if args.require == "implement" and not can_implement:
        raise SystemExit(3)
    if args.require == "deliver" and not result["can_deliver"]:
        raise SystemExit(4)


def history_cmd(args: argparse.Namespace) -> None:
    directory, _, _, decisions = load_workspace(args.root)
    payload = {
        "events": decisions.get("events", []),
        "scores": [read_json(path) for path in score_files(directory)],
        "overrides": [read_json(path) for path in sorted((directory / "overrides").glob("*.json"))],
        "audits": [read_json(path) for path in sorted((directory / "history").glob("*-visual-drift.json"))],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def migrate_cmd(args: argparse.Namespace) -> None:
    legacy = legacy_workspace(args.root)
    if not legacy.exists():
        raise SystemExit(f"No 1.x workspace found at {legacy}.")
    if workspace(args.root).exists():
        raise SystemExit(f"A 2.0 workspace already exists at {workspace(args.root)}.")
    state_path = legacy / "decision.json"
    if not state_path.exists():
        raise SystemExit("Legacy decision.json is missing.")
    old = read_json(state_path)
    directory = init_workspace(
        args.root,
        old.get("project", Path(args.root).resolve().name),
        old.get("mode", "guided"),
        old.get("platforms", ["web"]),
        None,
    )
    project = read_json(directory / "project.json")
    refs = read_json(directory / "references.json")
    decisions = read_json(directory / "decisions.json")
    old_ref = old.get("reference_decision", {})
    if old_ref.get("status") in {"confirmed", "assumed"}:
        project["approval_state"]["gate_a"] = old_ref["status"]
        refs.update({
            "primary": {"reference": old_ref.get("primary"), "contribution": "overall grammar"} if old_ref.get("primary") else None,
            "secondary": [{"reference": value, "contribution": "legacy unspecified"} for value in old_ref.get("secondary", [])[:2]],
            "selected_traits": old_ref.get("selected_traits", []),
            "rejected_traits": old_ref.get("rejected_traits", []),
        })
    old_standard = old.get("visual_standard", {})
    project["approval_state"]["gate_b"] = "draft"
    project["legacy_standard_status"] = old_standard.get("status")
    legacy_standard = legacy / "design-standard"
    if legacy_standard.exists():
        for source in legacy_standard.iterdir():
            if source.is_file():
                target_name = "MASTER.md" if source.name.lower() == "master.md" else "TOKENS.json" if source.name.lower() == "tokens.json" else source.name
                shutil.copy2(source, directory / "standards/v1" / target_name)
    atomic_json(directory / "references.json", refs)
    if refs.get("primary"):
        atomic_text(directory / "REFERENCE_CONTRACT.md", reference_contract(project, refs, "migrated from 1.x"))
    save_project(directory, project)
    record_event(directory, decisions, "legacy_workspace_migrated", {"source": str(legacy)})
    print(f"Migrated 1.x decisions into {directory}. The legacy workspace was preserved.")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a .design-director workspace")
    init.add_argument("--root", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--platform", action="append", required=True, choices=sorted(VALID_PLATFORMS))
    init.add_argument("--main-target-device")
    init.add_argument("--mode", default="guided", choices=sorted(VALID_MODES))
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=init_cmd)

    select = sub.add_parser("select", help="Record Gate A and create the Reference Contract")
    select.add_argument("--root", required=True)
    select.add_argument("--primary", required=True, help="REFERENCE|CONTRIBUTION")
    select.add_argument("--secondary", action="append", help="REFERENCE|CONTRIBUTION; at most two")
    select.add_argument("--like", action="append")
    select.add_argument("--avoid", action="append")
    select.add_argument("--do-not-copy", action="append")
    select.add_argument("--non-negotiable", action="append")
    select.add_argument("--confirmed-by", default="user in current conversation")
    select.set_defaults(func=select_cmd)

    approve = sub.add_parser("approve", help="Record Gate B or validate and record Gate C")
    approve.add_argument("--root", required=True)
    approve.add_argument("--gate", required=True, choices=["b", "c"])
    approve.add_argument("--version", default="v1")
    approve.add_argument("--style-tile")
    approve.add_argument("--representative-screen")
    approve.add_argument("--wireframe")
    approve.add_argument("--platform-qa", action="append", choices=sorted(VALID_PLATFORMS))
    approve.add_argument("--known-deviation", action="append")
    approve.add_argument("--confirmed-by", default="user in current conversation")
    approve.set_defaults(func=approve_cmd)

    score = sub.add_parser("score", help="Record a ten-dimension screenshot critique score")
    score.add_argument("--root", required=True)
    score.add_argument("--screen", required=True)
    score.add_argument("--target", required=True)
    score.add_argument("--screen-type", default="standard", choices=sorted(SCREEN_THRESHOLDS))
    score.add_argument("--dimension", action="append", required=True, help="NAME=1..5; provide all ten")
    score.add_argument("--screenshot", required=True)
    score.add_argument("--critique", required=True)
    score.add_argument("--dna-match", default="Strong", choices=["Strong", "Partial", "Weak"])
    score.add_argument("--generic-risk", default="Low", choices=["Low", "Medium", "High"])
    score.add_argument("--platform-fit", default="Strong", choices=["Strong", "Partial", "Weak"])
    score.add_argument("--top-fix", action="append")
    score.add_argument("--critical-issue", action="append")
    score.set_defaults(func=score_cmd)

    audit = sub.add_parser("audit", help="Detect visual drift from structured screen metadata")
    audit.add_argument("--root", required=True)
    audit.add_argument("--manifest", required=True)
    audit.add_argument("--baseline")
    audit.set_defaults(func=audit_cmd)

    override = sub.add_parser("override", help="Record a bounded page-level override")
    override.add_argument("--root", required=True)
    override.add_argument("--screen", required=True)
    override.add_argument("--override", required=True)
    override.add_argument("--reason", required=True)
    override.add_argument("--scope", required=True)
    override.add_argument("--does-not-change", action="append")
    override.set_defaults(func=override_cmd)

    status = sub.add_parser("status", help="Show gates, scores, and stage availability")
    status.add_argument("--root", required=True)
    status.add_argument("--require", choices=["decompose", "implement", "deliver"])
    status.set_defaults(func=status_cmd)

    history = sub.add_parser("history", help="Show decisions, scores, overrides, and audits")
    history.add_argument("--root", required=True)
    history.set_defaults(func=history_cmd)

    migrate = sub.add_parser("migrate", help="Migrate a preserved .visual-ui 1.x workspace")
    migrate.add_argument("--root", required=True)
    migrate.set_defaults(func=migrate_cmd)
    return result


def main() -> None:
    args = parser().parse_args()
    if args.command == "approve" and args.gate == "b":
        missing = [
            name
            for name in ("style_tile", "representative_screen", "wireframe")
            if not getattr(args, name)
        ]
        if missing:
            raise SystemExit("Gate B requires evidence arguments: " + ", ".join(missing))
    args.func(args)


if __name__ == "__main__":
    main()
