#!/usr/bin/env python3
"""Create and validate Visual UI Director decision artifacts."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
WORKSPACE_NAME = ".visual-ui"
VALID_MODES = {"guided", "reference-led", "direct"}
VALID_PLATFORMS = {"web", "ios", "ipados", "watchos", "android", "wearos", "windows"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def workspace(root: str) -> Path:
    return Path(root).expanduser().resolve() / WORKSPACE_NAME


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
        raise


def read_state(root: str) -> tuple[Path, dict]:
    directory = workspace(root)
    path = directory / "decision.json"
    if not path.exists():
        raise SystemExit(f"No Visual UI workspace at {directory}. Run init first.")
    return directory, json.loads(path.read_text(encoding="utf-8"))


def copy_template(name: str, destination: Path, project: str) -> None:
    content = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.replace("{{PROJECT_NAME}}", project), encoding="utf-8")


def init_cmd(args: argparse.Namespace) -> None:
    platforms = list(dict.fromkeys(args.platform))
    directory = workspace(args.root)
    state_path = directory / "decision.json"
    if state_path.exists() and not args.force:
        raise SystemExit(f"Workspace already exists at {directory}; use --force only after reviewing it.")

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "wireframes").mkdir(exist_ok=True)
    (directory / "screenshots").mkdir(exist_ok=True)
    copy_template("reference-board.md", directory / "reference-board.md", args.project)
    copy_template("visual-standard.md", directory / "design-standard" / "MASTER.md", args.project)
    copy_template("tokens.json", directory / "design-standard" / "tokens.json", args.project)

    direct = args.mode == "direct"
    state = {
        "schema_version": 1,
        "project": args.project,
        "mode": args.mode,
        "platforms": platforms,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "reference_decision": {
            "status": "assumed" if direct else "pending",
            "primary": None,
            "secondary": [],
            "selected_traits": [],
            "rejected_traits": [],
            "confirmed_by": "explicit direct mode" if direct else None,
        },
        "visual_standard": {
            "status": "assumed" if direct else "draft",
            "version": "v0.1",
            "confirmed_by": "explicit direct mode" if direct else None,
        },
    }
    atomic_json(state_path, state)
    print(f"Created Visual UI workspace at {directory}")


def select_cmd(args: argparse.Namespace) -> None:
    directory, state = read_state(args.root)
    state["reference_decision"] = {
        "status": "confirmed",
        "primary": args.primary,
        "secondary": args.secondary or [],
        "selected_traits": args.like or [],
        "rejected_traits": args.avoid or [],
        "confirmed_by": args.confirmed_by,
        "confirmed_at": now_iso(),
    }
    state["visual_standard"]["status"] = "draft"
    state["updated_at"] = now_iso()
    atomic_json(directory / "decision.json", state)
    print("Reference decision confirmed; Stage 2 is available.")


def approve_cmd(args: argparse.Namespace) -> None:
    directory, state = read_state(args.root)
    if state["mode"] != "direct" and state["reference_decision"]["status"] != "confirmed":
        raise SystemExit("Gate A is not confirmed; cannot approve the visual standard.")
    master = directory / "design-standard" / "MASTER.md"
    tokens = directory / "design-standard" / "tokens.json"
    if not master.exists() or not tokens.exists():
        raise SystemExit("MASTER.md and tokens.json are required before approval.")
    state["visual_standard"] = {
        "status": "confirmed",
        "version": args.version,
        "confirmed_by": args.confirmed_by,
        "confirmed_at": now_iso(),
    }
    state["updated_at"] = now_iso()
    atomic_json(directory / "decision.json", state)
    print(f"Visual standard {args.version} confirmed; Stage 3 is available.")


def status_cmd(args: argparse.Namespace) -> None:
    _, state = read_state(args.root)
    reference_status = state["reference_decision"]["status"]
    standard_status = state["visual_standard"]["status"]
    can_analyze = state["mode"] == "direct" or reference_status == "confirmed"
    can_implement = state["mode"] == "direct" or standard_status == "confirmed"
    result = {
        "project": state["project"],
        "mode": state["mode"],
        "platforms": state["platforms"],
        "reference_status": reference_status,
        "standard_status": standard_status,
        "can_analyze": can_analyze,
        "can_implement": can_implement,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.require == "analyze" and not can_analyze:
        raise SystemExit(2)
    if args.require == "implement" and not can_implement:
        raise SystemExit(3)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create .visual-ui decision artifacts")
    init.add_argument("--root", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--platform", action="append", required=True, choices=sorted(VALID_PLATFORMS))
    init.add_argument("--mode", default="guided", choices=sorted(VALID_MODES))
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=init_cmd)

    select = sub.add_parser("select", help="Record explicit Gate A reference approval")
    select.add_argument("--root", required=True)
    select.add_argument("--primary", required=True)
    select.add_argument("--secondary", action="append")
    select.add_argument("--like", action="append")
    select.add_argument("--avoid", action="append")
    select.add_argument("--confirmed-by", default="user in current conversation")
    select.set_defaults(func=select_cmd)

    approve = sub.add_parser("approve", help="Record explicit Gate B standard approval")
    approve.add_argument("--root", required=True)
    approve.add_argument("--version", required=True)
    approve.add_argument("--confirmed-by", default="user in current conversation")
    approve.set_defaults(func=approve_cmd)

    status = sub.add_parser("status", help="Show gates and optionally enforce a stage")
    status.add_argument("--root", required=True)
    status.add_argument("--require", choices=["analyze", "implement"])
    status.set_defaults(func=status_cmd)
    return result


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
