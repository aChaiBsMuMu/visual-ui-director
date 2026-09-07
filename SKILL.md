---
name: visual-ui-director
description: Direct visually distinctive, reference-led UI for Web, iOS/iPadOS/watchOS, Android/Wear OS, and Windows. Use to explore visual directions, analyze reference mechanisms, exercise design judgment, build strategy and a visual UI Design Manual, implement interfaces, critique rendered screenshots, detect generic UI or visual drift, and iterate to an approved quality threshold. Do not use for product strategy, UX research, pure backend work, or a narrow accessibility-only audit.
---

# Visual UI Director

## Mission

Make the user's taste the source of truth, then exercise visual judgment. Convert product intent and selected references through evidence, judgment and strategy into Visual DNA, a complete visual UI Design Manual, and production UI. Judge the rendered result against that system and iterate weak outcomes instead of treating code completion as delivery.

## Core invariants

- The user makes the final aesthetic decision. The director recommends, explains, and challenges; it does not silently lock taste.
- Keep one primary reference and at most two secondary references. Give each secondary reference one explicit contribution.
- Extract principles rather than copying layouts, identity, or protected assets. Keep source attribution and a `Do Not Copy` list.
- Mark consequential analysis as **Observed**, **Inferred**, or **Proposed**.
- Guided and Reference-led modes stop at Gates A and B. Only explicit Direct mode may record assumed locks, after the same Phase 2 completeness checks.
- An approved direction requires visual evidence: a style tile and representative screen, plus low-fidelity composition for priority form factors.
- The first implementation is never the final implementation. Render, critique, score, fix, and render again when required.
- Do not claim production-ready visual implementation until Gate C passes.
- Preserve one brand language across platforms while adapting navigation, density, input, safe areas, and native behaviors.

## Operating modes

- **Guided** (default): frame the product, form three visual hypotheses, search references, pass Gate A, derive the system, pass Gate B, implement, and pass Gate C.
- **Reference-led**: the user supplies references. Record what to keep and reject, pass Reference Lock, then complete Phase 2 before Gate B.
- **Direct**: only when the user explicitly asks to skip exploration or move immediately. Record a reference baseline and assumptions, then still complete analysis, judgment, strategy, Visual DNA, the design manual and specimens before an assumed Gate B; render, critique, score and enforce Gate C.

For persistent work, initialize the decision workspace:

```bash
python3 "<skill-dir>/scripts/design_workspace.py" init --root "<project-root>" --project "<project-name>" --platform web --mode guided
```

Use `status` before resuming. The helper records and validates decisions; it never chooses the aesthetic direction for the user.

## Stage 0 — Product and visual framing

Identify product, industry, audience, core task, context, content density, desired and rejected traits, brand assets, localization, accessibility target, technical stack, delivery scope, target platforms, and priority device. Infer repository facts when reliable; ask only for omissions that materially change visual direction.

Read [platform routing](references/platform-routing.md), [responsive composition](references/responsive-composition.md), and only the relevant platform files.

## PHASE 1 — FIND · Reference Discovery

### Visual hypotheses

Create three meaningfully different directions. Each needs a visual thesis, product fit, reference types, strength, risk, memorable gesture, generic-design risk, and reusable English, Chinese, platform, industry, visual-style, editorial, and interaction search terms. Do not create three palette variants of one layout.

### Reference discovery

Read [reference discovery](references/reference-discovery.md). Search suitable public sources such as Behance, Pinterest, Huaban, Dribbble, Awwwards, Mobbin, or official galleries. Present visible references and direct source links when available. Do not invent inaccessible results or download references as production assets.

### Gate A — Reference lock

Stop for the user to select, reject, remix by named trait, request another search, or upload references. Record:

- primary reference and contribution
- no more than two secondary references and their contributions
- selected and rejected traits
- `Do Not Copy`, non-negotiables, and platform targets

Generate `REFERENCE_CONTRACT.md` and record the choice with `design_workspace.py select`. Rejected traits may not re-enter later work unless the user explicitly revises the contract.

## PHASE 2 — ANALYZE & DEFINE

Read the [Phase 2 overview](references/phase-2/phase-2-overview.md) after Reference Lock. Run `phase2 start`; Direct bypasses a manual wait, never design thinking. Confirm the product, users, task, content, platforms and smallest target before defining the system.

### 2.1 Evidence

Load the Reference Contract. Preserve Primary / bounded Secondary contributions, Selected Traits, Rejected Traits and Do Not Copy. Mark facts **Observed**, hypotheses **Inferred**, and adaptations **Proposed**. Unknown fonts, exact sizes, breakpoints, motion and interactions must not masquerade as observations.

### 2.2 Deep analysis

Use [deep reference analysis](references/phase-2/deep-reference-analysis.md): **WHAT → WHY → EFFECT → FIT → ADAPT → RULE**, with risk and failure signals. Cover all twelve dimensions, keeping Components and Iconography separate. Persist REFERENCE_ANALYSIS.md.

### 2.3–2.4 Design judgment and cross-reference synthesis

Use [design judgment](references/phase-2/design-judgment.md) and [cross-reference synthesis](references/phase-2/cross-reference-synthesis.md). First map permitted influences, then resolve fit and conflicts explicitly in DESIGN_JUDGMENT.md and REFERENCE_INFLUENCE.md. Primary controls overall grammar; secondary traits cannot exceed Gate A's contribution. Translate adjectives into testable visual behavior and trace decisions to product, user, reference, platform, accessibility or explicit proposed reasoning.

### 2.5 Design strategy

Write [DESIGN_STRATEGY.md](references/phase-2/design-strategy.md): product visual problem, perception → behavior, thesis, priorities, tensions and conflict rules, goal-to-strategy matrix, visual budgets, non-negotiables, risks and anti-patterns. Strategy explains **why**; it precedes DNA and tokens.

### 2.6 Visual DNA

Preserve [5–8 observable, testable principles](references/visual-dna.md) above the token level. DNA states **stable visual behavior**, with pass/failure tests and key-screen gestures. Store it canonically in the versioned manual; the root visual-dna.md is a compatibility alias.

### 2.7 UI Design Manual

Build the [versioned manual](references/phase-2/design-manual.md) under `.design-director/standards/<version>/`; MASTER is a concise visual identity entry. Use project scope to select components and page patterns. Read applicable discipline specifications:

- [Color behavior](references/phase-2/color-system.md) and [type character](references/phase-2/typography-system.md)
- [Layout and page patterns](references/phase-2/layout-composition.md) and [spacing/geometry](references/phase-2/spacing-geometry.md)
- [Components and states](references/phase-2/component-system.md), separately from [icon language](references/phase-2/iconography-system.md)
- [Imagery/material](references/phase-2/imagery-material.md), [motion/states](references/phase-2/motion-states.md), [responsive layers](references/responsive-composition.md)

The manual specifies **how**. TOKENS.json owns parameters; SPECIMENS.json configures examples using token references. Avoid duplicate parameter sources and a generic default manual.

### 2.8 Visual specimens

Render [seven deterministic spec sheets](references/phase-2/visual-specimens.md) with `phase2 render`: color palette board, typography specimen, spacing/geometry sheet, layout atlas, component specimen, icon style sheet and style tile. Show real localized text and relevant states. Inspect rendered output; the style tile integrates the same rules and tokens. Use image generation only for expressive assets.

### 2.9 Representative screen

Render the highest-risk or most identity-defining actual page using near-real content, official tokens, a named layout pattern, components, DNA and strategy. Include priority form-factor composition evidence and test the smallest target. The renderer does not fabricate this integrated screen.

### 2.10 Coherence validation

Review color, type, layout, geometry, components, icons, imagery and motion against one thesis. Check reference boundaries, rejected traits, decorative dependency, content fit, smallest-screen failure, token/specimen agreement and representative/manual agreement. Record evidence and reasoning in REVIEW.json, bind the inspected inputs with `phase2 review`, and run `phase2 validate`.

### GATE B — STRATEGY & DESIGN MANUAL LOCK

Follow [Gate B validation](references/phase-2/gate-b-validation.md). Present strategy, DNA, the full manual, all specimens and representative screen. Guided/Reference-led stop for approval; Direct may record an assumed lock only after identical validation. Use the existing `approve --gate b --version VERSION`. Global visual changes require `phase2 upgrade --version NEW`; bounded page exceptions use `override`. Phase 3 must not reinvent the language.

## PHASE 3 — MAKE

Screen Intent → Composition → Implementation → Render → Critique → Iterate.

## Stage 7 — Implementation

Read [implementation and QA](references/implementation-and-qa.md) and relevant platform guidance. Run `status --require implement` to confirm a current validated Gate B lock in every mode, including Direct. Read the locked strategy/manual and choose a screen intent and named page pattern before composing. Implement real content, semantic tokens, responsive composition, required states, platform-native behavior, meaningful motion, and documented page overrides.

## Stage 8 — Screenshot critic

Read [screenshot critic](references/screenshot-critic.md) and [anti-generic UI](references/anti-generic-ui.md). Render target screens and compare them with the Reference Contract, Visual DNA, approved system, representative screen, and platform layer. Report strengths, problems, top three fixes, generic risk, platform fit, and whether a re-render is required.

## Stage 9 — Visual score

Read [visual quality rubric](references/visual-quality-rubric.md). Score all ten dimensions from 1–5 and convert the total to 100. Persist scores with `design_workspace.py score`.

- `<80`: must iterate.
- `80–89`: fix at least the top three problems and re-render.
- `>=90`: eligible for Gate C when all other evidence exists.
- Key screens target `>=85`; hero, home, and core-decision screens target `>=88`.

## Stage 10 — Iteration

Repeat `implement → render → critique → score → top-three fixes → re-render → re-score`. Also read [visual drift](references/visual-drift.md) when a project has many screens, multiple contributors, or repeated iterations. Use `design_workspace.py audit` and record intentional exceptions with `override` rather than weakening the whole system.

### GATE C — QUALITY LOCK

Pass Gate C only when the Visual Standard and Visual DNA are approved, target screens were rendered, screenshot critique is complete, score thresholds are met, critical inconsistencies are resolved, platform QA is recorded, and known deviations are documented. Record it with `design_workspace.py approve --gate c`.

## Platform routing

- Web: [web](references/platforms/web.md)
- iPhone and iPad: [Apple mobile](references/platforms/apple-mobile.md)
- Apple Watch: [watchOS](references/platforms/watchos.md)
- Android and Wear OS: [Android](references/platforms/android.md)
- Windows: [Windows](references/platforms/windows.md)

Apply `Brand Layer → Product Visual Layer → Platform Adaptation Layer → Device Context Layer`. Aim for the same brand and native behavior, not pixel-identical layouts.

## Decision workspace

The `.design-director/` workspace stores project state, references, decisions, Visual DNA, versioned standards, screenshots, critiques, scores, overrides, and history. Use `init`, `status`, `select`, `approve`, `score`, `audit`, `override`, and `history`, plus `phase2 start|render|review|validate|upgrade`; see `--help` for exact arguments. For 1.x projects, read [migration notes](MIGRATION.md).

## Anti-generic rules

Reject unexplained dashboard formulas, card-everything layouts, default AI gradients, repeated icon-title-paragraph grids, mechanical spacing, excessive pills, generic heroes, unjustified glassmorphism, component-library-demo pages, and key screens without a memorable visual gesture. Diagnose the content and hierarchy problem before decorating it.

## Delivery requirements

Report the selected references, approved standard and Visual DNA version, implemented surfaces, exact test sizes and states, screenshot critique, before/after scores, fixes made, platform QA, overrides, and unresolved constraints. Do not claim a screen, platform, interaction, or threshold was tested unless evidence exists.
