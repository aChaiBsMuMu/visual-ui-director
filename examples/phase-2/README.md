# Margin: a complete fictional Phase 2 example

**静读 / Margin** is a bilingual web reader whose task is choosing and finishing one essay after work. All sources and design decisions here are fictional instructional fixtures, not claims about an external product, user study or production launch. Do not copy its fonts, colors, spacing, component inventory or patterns into unrelated projects.

Run from the repository root (Python 3.9+, standard library only):

```bash
python3 examples/phase-2/build_example.py --root /tmp/margin-example
python3 scripts/design_workspace.py phase2 validate --root /tmp/margin-example
```

The script refuses an existing workspace, initializes Direct mode, records a synthetic reference baseline, supplies an authored manual, renders seven sheets plus two compact representative SVGs, and validates the fixture. It does **not** approve Gate B. Its prefilled review assertions are demonstration data; a real project needs actual inspection and `phase2 review` before approval.

## Causal chain

1. **Reference observation** — the fictional editorial study puts one title in the largest visual region. Precise font and motion details remain unknown.
2. **Design judgment J-01** — one large title suits a reader choosing one essay; an equal preview grid would increase comparison pressure. This would be a poor fit for a simultaneous data-comparison task.
3. **Design strategy** — “Give one thoughtful essay enough space to earn attention.” Prioritize comprehension, then reading continuity, then discovery; allow one committed accent in the decision region.
4. **Visual DNA** — one essay title leads the first glance, while saving and navigation recede. Fail if multiple previews become equally loud.
5. **Manual rule** — Hero Decision gives the title the dominant region; compact stacks title → synopsis → action. Read uses the primary semantic action treatment; save is secondary. Exact values live in TOKENS.json.
6. **Visual specimen** — the layout atlas shows those regions, the component sheet contrasts reading and saving, and the representative screen combines real bilingual content with the same tokens.

## Inspect the output

- [Design Strategy](manual/DESIGN_STRATEGY.md) → [Visual DNA](manual/VISUAL_DNA.md) → [Master](manual/MASTER.md)
- [Reference Analysis](manual/REFERENCE_ANALYSIS.md), [Judgment](manual/DESIGN_JUDGMENT.md), [Influence Map](manual/REFERENCE_INFLUENCE.md)
- [Color board](manual/evidence/color-palette-board.svg)
- [Typography specimen](manual/evidence/typography-specimen.svg)
- [Spacing / geometry sheet](manual/evidence/spacing-geometry-sheet.svg)
- [Layout atlas](manual/evidence/layout-atlas.svg)
- [Component specimen](manual/evidence/component-specimen.svg)
- [Icon style sheet](manual/evidence/icon-style-sheet.svg)
- [Style tile](manual/evidence/style-tile.svg)
- [390-wide representative](manual/evidence/representative-screen.svg) and [320-wide content stress](manual/evidence/representative-screen-small.svg)

These are deterministic SVG spec sheets and a static integrated specimen, not a working application. Runtime navigation, accessibility semantics and motion timing still need Phase 3 implementation and QA. The example intentionally excludes decorative imagery; an image-led product must provide an actual authorized image and evaluate its crop/material direction.

## Configuration ownership

[Tokens](manual/TOKENS.json) owns values; [Specimens](manual/SPECIMENS.json) selects examples using references. [Review](manual/REVIEW.json) demonstrates evidence assertions and provenance. Its contract hash and review snapshot are filled when building an isolated workspace. The checked-in standalone manual has no real project approval.
