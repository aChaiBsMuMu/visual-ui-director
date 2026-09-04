from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "design_workspace.py"
DIMENSIONS_84 = [4, 4, 4, 4, 4, 5, 5, 4, 4, 4]
DIMENSIONS_90 = [5, 5, 4, 4, 5, 5, 5, 4, 4, 4]
NAMES = [
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
]


class WorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        if ok and result.returncode:
            self.fail(f"command failed: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}")
        if not ok and result.returncode == 0:
            self.fail(f"command unexpectedly passed: {result.args}")
        return result

    def test_guided_cross_platform_gates_scores_and_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.run_cli(
                "init", "--root", temp, "--project", "Dinner Now",
                "--platform", "ios", "--platform", "watchos", "--platform", "web",
                "--main-target-device", 'iPhone 6.3"', "--mode", "guided",
            )
            workspace = root / ".design-director"
            self.assertTrue((workspace / "project.json").exists())
            self.assertTrue((workspace / "standards/v1/IMAGERY.md").exists())
            self.assertTrue((workspace / "standards/v1/PLATFORM_OVERRIDES").is_dir())
            self.run_cli(
                "approve", "--root", temp, "--gate", "b",
                "--style-tile", str(REPO / "README.md"),
                "--representative-screen", str(REPO / "README.md"),
                "--wireframe", str(REPO / "README.md"),
                ok=False,
            )
            self.run_cli(
                "select", "--root", temp,
                "--primary", "primary-url|composition and hierarchy",
                "--secondary", "photo-url|photography only",
                "--like", "warm photography", "--avoid", "purple gradient",
                "--do-not-copy", "navigation", "--non-negotiable", "editorial whitespace",
            )
            refs = json.loads((workspace / "references.json").read_text())
            self.assertEqual(refs["secondary"][0]["contribution"], "photography only")
            self.assertIn("purple gradient", refs["rejected_traits"])
            dna = "# Visual DNA\n\n" + "\n".join(
                f"{index}. Observable principle {index} with a visible pass condition."
                for index in range(1, 7)
            )
            (workspace / "visual-dna.md").write_text(dna)
            evidence = root / "evidence.png"
            critique = root / "critique.md"
            evidence.write_bytes(b"rendered-evidence")
            critique.write_text("# Screenshot Critique\nTop Fixes: three")
            self.run_cli(
                "approve", "--root", temp, "--gate", "b", "--version", "v1",
                "--style-tile", str(evidence),
                "--representative-screen", str(evidence),
                "--wireframe", str(evidence),
            )
            self.record_score(temp, evidence, critique, DIMENSIONS_84)
            self.run_cli(
                "approve", "--root", temp, "--gate", "c",
                "--platform-qa", "ios", "--platform-qa", "watchos", "--platform-qa", "web",
                ok=False,
            )
            self.record_score(temp, evidence, critique, DIMENSIONS_90)
            self.run_cli(
                "override", "--root", temp, "--screen", "Onboarding Welcome",
                "--override", "Larger hero type", "--reason", "First-launch emotion",
                "--scope", "Welcome only", "--does-not-change", "Brand colors",
            )
            manifest = root / "screens.json"
            manifest.write_text(json.dumps({
                "screens": [
                    {"screen": "Home", "radius": "18", "brand_color_budget": "8%", "dna_match": "strong"},
                    {"screen": "Explore", "radius": "24", "brand_color_budget": "20%", "dna_match": "strong"},
                ]
            }))
            audit = self.run_cli("audit", "--root", temp, "--manifest", str(manifest), "--baseline", "Home")
            self.assertIn('"status": "drift_detected"', audit.stdout)
            self.assertIn("Color drift", audit.stdout)
            self.run_cli(
                "approve", "--root", temp, "--gate", "c",
                "--platform-qa", "ios", "--platform-qa", "watchos", "--platform-qa", "web",
                "--known-deviation", "Documented legacy settings screen",
            )
            status = json.loads(self.run_cli("status", "--root", temp).stdout)
            self.assertTrue(status["can_deliver"])
            history = json.loads(self.run_cli("history", "--root", temp).stdout)
            self.assertGreaterEqual(len(history["scores"]), 2)
            self.assertTrue(history["audits"])

    def test_legacy_migration_preserves_source_and_requires_reapproval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy = root / ".visual-ui"
            standard = legacy / "design-standard"
            standard.mkdir(parents=True)
            (standard / "MASTER.md").write_text("# Legacy master")
            (standard / "tokens.json").write_text("{}")
            (legacy / "decision.json").write_text(json.dumps({
                "project": "Legacy Project",
                "mode": "guided",
                "platforms": ["web"],
                "reference_decision": {
                    "status": "confirmed",
                    "primary": "legacy-reference",
                    "secondary": [],
                    "selected_traits": ["editorial spacing"],
                    "rejected_traits": ["glassmorphism"],
                },
                "visual_standard": {"status": "confirmed", "version": "v0.1"},
            }))
            self.run_cli("migrate", "--root", temp)
            self.assertTrue(legacy.exists())
            project = json.loads((root / ".design-director/project.json").read_text())
            self.assertEqual(project["approval_state"]["gate_a"], "confirmed")
            self.assertEqual(project["approval_state"]["gate_b"], "draft")
            self.assertEqual((root / ".design-director/standards/v1/TOKENS.json").read_text(), "{}")

    def record_score(self, root: str, evidence: Path, critique: Path, values: list[int]) -> None:
        args = [
            "score", "--root", root, "--screen", "Home", "--target", 'iPhone 6.3"',
            "--screen-type", "hero", "--screenshot", str(evidence), "--critique", str(critique),
        ]
        for name, value in zip(NAMES, values):
            args.extend(["--dimension", f"{name}={value}"])
        self.run_cli(*args)

    def test_local_markdown_links_exist(self) -> None:
        files = [REPO / "SKILL.md", REPO / "README.md", *sorted((REPO / "references").rglob("*.md"))]
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        missing = []
        for source in files:
            for target in pattern.findall(source.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                clean = target.split("#", 1)[0]
                if clean and not (source.parent / clean).resolve().exists():
                    missing.append(f"{source.relative_to(REPO)} -> {target}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
