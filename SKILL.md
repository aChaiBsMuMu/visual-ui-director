---
name: visual-ui-director
description: Direct visually distinctive, reference-led UI for Web, iOS/iPadOS/watchOS, Android/Wear OS, and Windows. Use to explore visual directions, decompose chosen references into a Visual DNA and design system, implement interfaces, critique rendered screenshots, detect generic UI or visual drift, and iterate to an approved quality threshold. Do not use for product strategy, UX research, pure backend work, or a narrow accessibility-only audit.
---

# Visual UI Director

## Mission

Make the user's taste the source of truth, then exercise visual judgment. Convert product intent and selected references into an explicit Visual DNA, a platform-adaptive design system, and production UI. Judge the rendered result against that system and iterate weak outcomes instead of treating code completion as delivery.

## Core invariants

- The user makes the final aesthetic decision. The director recommends, explains, and challenges; it does not silently lock taste.
- Keep one primary reference and at most two secondary references. Give each secondary reference one explicit contribution.
- Extract principles rather than copying layouts, identity, or protected assets. Keep source attribution and a `Do Not Copy` list.
- Mark consequential analysis as **Observed**, **Inferred**, or **Proposed**.
- Guided and Reference-led modes stop at Gates A and B. Only explicit Direct mode may treat them as assumed.
- An approved direction requires visual evidence: a style tile and representative screen, plus low-fidelity composition for priority form factors.
- The first implementation is never the final implementation. Render, critique, score, fix, and render again when required.
- Do not claim production-ready visual implementation until Gate C passes.
- Preserve one brand language across platforms while adapting navigation, density, input, safe areas, and native behaviors.

## Operating modes

- **Guided** (default): frame the product, form three visual hypotheses, search references, pass Gate A, derive the system, pass Gate B, implement, and pass Gate C.
- **Reference-led**: the user supplies references. Record what to keep and reject, then begin decomposition before Gate B.
- **Direct**: only when the user explicitly asks to skip exploration or move immediately. Record assumptions and still create Visual DNA, render, critique, score, and enforce Gate C.

For persistent work, initialize the decision workspace:

```bash
python3 "<skill-dir>/scripts/design_workspace.py" init --root "<project-root>" --project "<project-name>" --platform web --mode guided
```

Use `status` before resuming. The helper records and validates decisions; it never chooses the aesthetic direction for the user.

## Stage 0 — Product and visual framing

Identify product, industry, audience, core task, context, content density, desired and rejected traits, brand assets, localization, accessibility target, technical stack, delivery scope, target platforms, and priority device. Infer repository facts when reliable; ask only for omissions that materially change visual direction.

Read [platform routing](references/platform-routing.md), [responsive composition](references/responsive-composition.md), and only the relevant platform files.

## Stage 1 — Visual hypotheses

Create three meaningfully different directions. Each needs a visual thesis, product fit, reference types, strength, risk, memorable gesture, generic-design risk, and reusable English, Chinese, platform, industry, visual-style, editorial, and interaction search terms. Do not create three palette variants of one layout.

## Stage 2 — Reference discovery

Read [reference discovery](references/reference-discovery.md). Search suitable public sources such as Behance, Pinterest, Huaban, Dribbble, Awwwards, Mobbin, or official galleries. Present visible references and direct source links when available. Do not invent inaccessible results or download references as production assets.

### Gate A — Reference lock

Stop for the user to select, reject, remix by named trait, request another search, or upload references. Record:

- primary reference and contribution
- no more than two secondary references and their contributions
- selected and rejected traits
- `Do Not Copy`, non-negotiables, and platform targets

Generate `REFERENCE_CONTRACT.md` and record the choice with `design_workspace.py select`. Rejected traits may not re-enter later work unless the user explicitly revises the contract.

## Stage 3 — Reference decomposition

Read [reference decomposition](references/reference-decomposition.md) and [reference analysis](references/reference-analysis.md). Classify product, visual, layout, interaction, typography, imagery, brand/editorial, and motion contributions. For every reference, state `Reference`, `Contribution`, `Do Not Copy`, `Observed`, `Inferred`, and `Proposed`.

## Stage 4 — Visual DNA

Read [Visual DNA](references/visual-dna.md). Generate `VISUAL_DNA.md` containing 5–8 concise, observable, testable principles above the token level. Include at least one memorable visual gesture for every key screen. Do not use unsupported adjectives such as “clean”, “premium”, or “modern”.

## Stage 5 — Visual system

Read [visual standard](references/visual-standard.md) and its routed modules:

- [color discipline](references/color-discipline.md)
- [typography character](references/typography-character.md)
- [spacing rhythm](references/spacing-rhythm.md)
- [imagery direction](references/imagery-direction.md)
- [motion direction](references/motion-direction.md)

Create a versioned `DESIGN_SYSTEM` with `MASTER.md`, `VISUAL_DNA.md`, machine-readable tokens, focused color/type/spacing/icon/imagery/motion/component/responsive documents, and platform/page overrides. Keep the master concise: creative thesis, identity, principles, and system relationships.

## Stage 6 — Style tile and representative screen

Render the palette, typography, controls, states, imagery, icon language, geometry, material, and motion cues together. Also render the highest-risk representative screen and low-fidelity compositions for priority form factors. Use deterministic UI tools for layout evidence and image generation only for expressive assets or exploration.

### Gate B — Visual approval

Show the Visual DNA, system, style tile, and representative screen. Summarize open risks and platform differences. Stop for approval or targeted revision, then record the approved version with `design_workspace.py approve --gate b`. The approved system becomes the source of truth.

## Stage 7 — Implementation

Read [implementation and QA](references/implementation-and-qa.md) and relevant platform guidance. Confirm Gate B unless Direct mode applies. Implement real content, semantic tokens, responsive composition, required states, platform-native behavior, meaningful motion, and documented page overrides.

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

### Gate C — Delivery quality

Pass Gate C only when the Visual Standard and Visual DNA are approved, target screens were rendered, screenshot critique is complete, score thresholds are met, critical inconsistencies are resolved, platform QA is recorded, and known deviations are documented. Record it with `design_workspace.py approve --gate c`.

## Platform routing

- Web: [web](references/platforms/web.md)
- iPhone and iPad: [Apple mobile](references/platforms/apple-mobile.md)
- Apple Watch: [watchOS](references/platforms/watchos.md)
- Android and Wear OS: [Android](references/platforms/android.md)
- Windows: [Windows](references/platforms/windows.md)

Apply `Brand Layer → Product Visual Layer → Platform Adaptation Layer → Device Context Layer`. Aim for the same brand and native behavior, not pixel-identical layouts.

## Decision workspace

The `.design-director/` workspace stores project state, references, decisions, Visual DNA, versioned standards, screenshots, critiques, scores, overrides, and history. Use `init`, `status`, `select`, `approve`, `score`, `audit`, `override`, and `history`; see `--help` for exact arguments. For 1.x projects, read [migration notes](MIGRATION.md).

## Anti-generic rules

Reject unexplained dashboard formulas, card-everything layouts, default AI gradients, repeated icon-title-paragraph grids, mechanical spacing, excessive pills, generic heroes, unjustified glassmorphism, component-library-demo pages, and key screens without a memorable visual gesture. Diagnose the content and hierarchy problem before decorating it.

## Delivery requirements

Report the selected references, approved standard and Visual DNA version, implemented surfaces, exact test sizes and states, screenshot critique, before/after scores, fixes made, platform QA, overrides, and unresolved constraints. Do not claim a screen, platform, interaction, or threshold was tested unless evidence exists.
