# Visual UI Director 2.1 — ANALYZE & DEFINE

Visual UI Director is not a component-library generator. It is an AI visual design director: it understands reference mechanisms, makes design judgments, builds a strategy, and produces a complete UI Design Manual with deterministic visual specifications before implementing UI. Rendered screenshots then guide critique and iteration.

It supports Web, iOS, iPadOS, watchOS, Android, Wear OS, and Windows with one brand language and native platform behavior.

## Quick start

Install the folder in your Codex skills directory and invoke:

~~~text
$visual-ui-director Design an iPhone cooking app for young Chinese office workers. I do not know what style I want.
~~~

For persistent work:

~~~bash
python3 scripts/design_workspace.py init \
  --root /path/to/project \
  --project "Dinner Now" \
  --platform ios \
  --main-target-device 'iPhone 6.3"' \
  --mode guided
~~~

The end-to-end flow is:

~~~text
Product Framing
↓
PHASE 1 — FIND · Reference Discovery
↓
Gate A — Reference Lock
↓
PHASE 2 — ANALYZE & DEFINE
Reference Analysis → Design Judgment → Cross-reference Synthesis
→ Design Strategy → Visual DNA → UI Design Manual
→ Visual Specimens → Representative Screen → Coherence Validation
↓
Gate B — Strategy & Design Manual Lock
↓
PHASE 3 — MAKE
Screen Intent → Composition → Implementation → Render → Critique → Iterate
↓
Gate C — Quality Lock
~~~

## Modes

### Guided mode

Use when the user is unsure of the look. The skill forms three meaningfully different directions, searches and presents references, waits for the user's selection, then builds and validates the system.

### Reference-led mode

Use when the user already has screenshots or links. Record each reference's bounded contribution and rejected traits. Example: photography and spacing are selected; navigation and colors are rejected.

### Direct mode

Use only when the user explicitly asks to skip exploration. Gate A can be an explicitly proposed baseline when no external reference is available. Analysis, judgment, strategy, DNA, the complete manual and visual specimens remain required; only after validation can Gate B be assumed. Direct never means skipping design thinking or Gate C.

## Visual DNA example

~~~text
1. Warm lifestyle photography is the primary emotional carrier.
2. White space separates decisions more often than borders.
3. Brand green is reserved for primary actions and positive state.
4. Rounded forms feel soft but mature, never toy-like.
5. Recipe decisions use one dominant crop rather than equal card grids.
6. Icons support imagery and never compete with it.
7. The home screen uses an edge-to-edge seasonal image as its memorable gesture.
~~~

These are observable identity rules, not token values or vague adjectives.

## Gate A and the Reference Contract

Record a primary reference plus no more than two secondary references. Use a pipe to separate the source from its contribution:

~~~bash
python3 scripts/design_workspace.py select \
  --root /path/to/project \
  --primary "Behance case study URL|overall composition and hierarchy" \
  --secondary "Editorial spread URL|photography crop only" \
  --like "generous whitespace" \
  --avoid "purple gradient" \
  --do-not-copy "navigation structure" \
  --non-negotiable "warm food photography"
~~~

This writes REFERENCE_CONTRACT.md so rejected traits cannot silently return later.

## Phase 2: the design brain

Every important finding follows **WHAT → WHY → EFFECT → FIT → ADAPT → RULE**, with source labels and failure signals. Analysis covers creative thesis, color, typography, layout, geometry, components, iconography, imagery/material, motion/states, responsive/platform adaptation, density and signature gestures. Primary controls the overall grammar; secondary references remain within their contracted contribution.

Strategy explains **why**. Visual DNA defines **stable observable behavior**. The manual specifies **how**. Tokens own values; specimen configuration chooses what to display. A project-specific inventory avoids forcing desktop tables onto a watch or bottom tabs onto a dashboard.

```bash
python3 scripts/design_workspace.py phase2 start --root /path/to/project --version v1
# Complete the analysis, judgments, strategy, DNA, manual, TOKENS.json and SPECIMENS.json.
python3 scripts/design_workspace.py phase2 render --root /path/to/project --version v1
# Render representative-screen.svg/png/jpg into evidence/ using the real product system.
# Inspect every sheet and screen; complete REVIEW.json with evidence and actual findings.
python3 scripts/design_workspace.py phase2 review --root /path/to/project --version v1 --reviewed-by "reviewer in current session"
python3 scripts/design_workspace.py phase2 validate --root /path/to/project --version v1
```

The standard-library renderer generates palette, type, spacing/geometry, layout atlas, components, icons and style tile sheets. It fails on missing token references and detected text overflow. It does not invent a representative screen or perform aesthetic review. Read the [configuration schema](references/phase-2/specimen-schema.md) and inspect the [complete fictional Margin example](examples/phase-2/README.md).

## Gate B — Strategy & Design Manual Lock

Present strategy, DNA, all disciplines, seven visual sheets and the representative screen. After user approval in Guided/Reference-led, or a validated assumption in Direct:

```bash
python3 scripts/design_workspace.py approve --root /path/to/project --gate b --version v1
python3 scripts/design_workspace.py status --root /path/to/project --require implement
```

Gate B rejects missing documents, obvious template content, invalid DNA, missing or stale sheets, fake images, out-of-bound contribution records, configured contrast failures and incomplete/stale coherence reviews. Review assertions still require honest visual judgment; file hashes cannot prove aesthetic fit or interaction correctness.

Existing `--style-tile`, `--representative-screen`, and `--wireframe` options remain accepted. Use paths matching reviewed evidence; an unseen import cannot bypass the review snapshot. The required generated style-tile.svg and layout-atlas.svg remain canonical, even when additional evidence is supplied.

A locked version is immutable for global rules. Tokens, documents, references or evidence changing after lock block implementation and Gate C until a new version is reviewed:

```bash
python3 scripts/design_workspace.py phase2 upgrade --root /path/to/project --version v2
python3 scripts/design_workspace.py phase2 start --root /path/to/project --version v2
```

Single-page exceptions continue to use the existing `override` command. The original standard remains recoverable. See [migration](MIGRATION.md) for old projects.

## Screenshot QA and score

The Screenshot Critic reports Visual DNA match, strengths, problems, top fixes, generic UI risk, platform fit, critical issues, and re-render need.

Example:

~~~text
Screen: Home
Target: iPhone 6.3"
Visual DNA Match: Strong
Score: 84 / 100
Problems:
1. Hero region still follows a generic centered template.
2. Secondary cards compete with the primary decision.
3. H2/body contrast is too weak.
Top Fixes:
1. Increase image dominance and offset the title.
2. Remove non-interactive card borders.
3. Increase type-scale and weight contrast.
Generic UI Risk: Medium
Platform Fit: Strong
Required Re-render: Yes
~~~

Persist a complete ten-dimension score:

~~~bash
python3 scripts/design_workspace.py score \
  --root /path/to/project \
  --screen Home \
  --target 'iPhone 6.3"' \
  --screen-type hero \
  --screenshot /path/to/home.png \
  --critique /path/to/home-critique.md \
  --dimension "Visual Identity=4" \
  --dimension "Hierarchy=4" \
  --dimension "Composition=4" \
  --dimension "Spacing Rhythm=4" \
  --dimension "Typography=4" \
  --dimension "Color Discipline=5" \
  --dimension "Imagery Consistency=5" \
  --dimension "Component Coherence=4" \
  --dimension "Platform Appropriateness=4" \
  --dimension "Memorability=4" \
  --generic-risk Medium \
  --top-fix "Strengthen the hero gesture"
~~~

The values above total 84/100, below the 88-point hero threshold, so Gate C will refuse delivery until a later score passes.

## Drift and page overrides

Audit structured metadata across many screens:

~~~bash
python3 scripts/design_workspace.py audit \
  --root /path/to/project \
  --manifest /path/to/screens.json \
  --baseline Home
~~~

Record intentional exceptions without changing the whole system:

~~~bash
python3 scripts/design_workspace.py override \
  --root /path/to/project \
  --screen "Onboarding Welcome" \
  --override "Hero typography may exceed master H1" \
  --reason "First-launch emotional impact" \
  --scope "Only this screen" \
  --does-not-change "Brand colors" \
  --does-not-change "Photography direction"
~~~

## Gate C

Gate C validates approved direction, Visual DNA, rendered screenshots, critiques, score thresholds, resolved critical issues, re-score requirements, and platform QA:

~~~bash
python3 scripts/design_workspace.py approve \
  --root /path/to/project \
  --gate c \
  --platform-qa ios \
  --known-deviation "Legacy settings screen remains on v1 components"
~~~

Use status and history to inspect the decision trail:

~~~bash
python3 scripts/design_workspace.py status --root /path/to/project
python3 scripts/design_workspace.py history --root /path/to/project
~~~

## Decision workspace and complete UI Design Manual

```text
.design-director/
├── project.json                 # gates, current version, integrity locks
├── references.json
├── decisions.json
├── REFERENCE_CONTRACT.md
├── reference-board.md
├── visual-dna.md                # compatibility alias to current VISUAL_DNA.md
├── standards/
│   ├── current                  # version pointer
│   └── v1/
│       ├── REFERENCE_ANALYSIS.md
│       ├── DESIGN_JUDGMENT.md
│       ├── REFERENCE_INFLUENCE.md
│       ├── DESIGN_STRATEGY.md
│       ├── VISUAL_DNA.md
│       ├── MASTER.md
│       ├── COLOR.md
│       ├── TYPOGRAPHY.md
│       ├── LAYOUT.md
│       ├── SPACING_GEOMETRY.md
│       ├── SPACING.md           # compatibility router
│       ├── COMPONENTS.md
│       ├── ICONOGRAPHY.md
│       ├── IMAGERY.md
│       ├── MOTION.md
│       ├── RESPONSIVE.md
│       ├── PAGE_PATTERNS.md
│       ├── DO_DONT.md
│       ├── TOKENS.json
│       ├── SPECIMENS.json
│       ├── REVIEW.json          # scoped review assertions and evidence binding
│       ├── LOCK.json            # receipt generated by Gate B
│       ├── PLATFORM_OVERRIDES/
│       ├── PAGE_OVERRIDES/
│       └── evidence/
│           ├── color-palette-board.svg
│           ├── typography-specimen.svg
│           ├── spacing-geometry-sheet.svg
│           ├── layout-atlas.svg
│           ├── component-specimen.svg
│           ├── icon-style-sheet.svg
│           ├── style-tile.svg
│           ├── render-manifest.json
│           └── representative-screen.svg/png/jpg
├── screenshots/
├── critiques/
├── scores/
├── overrides/                  # canonical records from the existing override CLI
└── history/
```

This is a design manual plus visual specification, not a catalog of unused components. Bounded motion, imagery, icon or component omissions need an explicit reason and alternative; required discipline documents and sheets remain present.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/design_workspace.py --help
python3 scripts/render_design_specimens.py --help
python3 examples/phase-2/build_example.py --root /tmp/margin-example
```

Python 3.9+; no new package dependency. See [migration notes](MIGRATION.md) for 1.x/2.0 projects and [SKILL.md](SKILL.md) for orchestration. The unchanged Screenshot Critic, Visual Score, Visual Drift and Gate C still govern delivery.
