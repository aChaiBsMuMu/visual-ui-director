# Visual UI Director 2.0

Visual UI Director is not a component-library generator. It is a reference-led, judgment-driven workflow that turns product intent and user taste into a Visual DNA, a platform-adaptive design system, and production UI—then judges rendered screenshots and iterates until the agreed visual-quality threshold is met.

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
Product framing → 3 visual hypotheses → reference discovery → Gate A
→ reference decomposition → Visual DNA → design system
→ style tile + representative screen → Gate B
→ implementation → screenshot critic → visual score → fix loop → Gate C
~~~

## Modes

### Guided mode

Use when the user is unsure of the look. The skill forms three meaningfully different directions, searches and presents references, waits for the user's selection, then builds and validates the system.

### Reference-led mode

Use when the user already has screenshots or links. Record each reference's bounded contribution and rejected traits. Example: photography and spacing are selected; navigation and colors are rejected.

### Direct mode

Use only when the user explicitly asks to skip exploration. Gates A and B are recorded as assumptions, but Visual DNA, rendered critique, scoring, iteration, and Gate C still apply.

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

## Gate B

Complete visual-dna.md with 5–8 principles and provide rendered evidence:

~~~bash
python3 scripts/design_workspace.py approve \
  --root /path/to/project \
  --gate b \
  --version v1 \
  --style-tile /path/to/style-tile.png \
  --representative-screen /path/to/home.png \
  --wireframe /path/to/wireframe.svg
~~~

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

## Decision workspace

~~~text
.design-director/
├── project.json
├── references.json
├── decisions.json
├── REFERENCE_CONTRACT.md
├── visual-dna.md
├── standards/
│   ├── v1/
│   └── current
├── screenshots/
├── critiques/
├── scores/
├── overrides/
└── history/
~~~

See [migration notes](MIGRATION.md) for 1.x projects and [SKILL.md](SKILL.md) for orchestration.
