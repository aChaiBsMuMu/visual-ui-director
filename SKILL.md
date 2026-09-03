---
name: visual-ui-director
description: Create visually distinctive, reference-led UI for web, mobile, watch, and desktop products. Use when a user wants to explore visual references, turn selected references into an actionable UI visual standard, or implement and visually validate an interface across Web, iOS/iPadOS/watchOS, Android, or Windows. Do not use for pure backend work or a narrow accessibility-only audit.
---

# Visual UI Director

Make the user's taste the source of truth. Lead a UI project through reference selection, visual-standard approval, implementation, and rendered visual QA without treating an industry template or style label as the design answer.

## Core invariants

- The user owns the aesthetic decision. Recommendations help them choose; they do not silently choose for them.
- Keep one primary reference. Use at most two secondary references, each assigned to explicit traits. Do not blend images indiscriminately.
- Do not reproduce a third-party work pixel-for-pixel or reuse its protected assets. Extract principles, not identity.
- Label uncertain inferences. A static image cannot prove its original font, exact token values, responsive behavior, or motion.
- In Guided and Reference-led modes, stop at each approval gate unless the user explicitly asked to skip it.
- A visual standard must include rendered evidence such as a style tile, wireframe, or representative UI region; prose alone is insufficient.
- After implementation, inspect rendered screenshots at relevant sizes and fix the highest-impact visual mismatch before delivery.
- Platform conventions constrain the shared visual language. Never force one platform's navigation, density, hit targets, or input model onto another.

## Select an operating mode

- **Guided** (default): discover references, obtain reference approval, build a visual standard, obtain standard approval, then implement.
- **Reference-led**: the user already supplied one or more references; begin with reference analysis, then obtain standard approval before implementation.
- **Direct**: only when the user explicitly asks to skip exploration or move fast. Record assumptions, create a lightweight visual standard, and proceed without the two pauses.

For work that persists artifacts in a project, initialize the decision workspace:

```bash
python3 "<skill-dir>/scripts/design_workspace.py" init --root "<project-root>" --project "<project-name>" --platform web --mode guided
```

Use `status` before resuming a later session. The helper records decisions; it never decides on the user's behalf.

## Stage 0: frame the problem

Identify what materially affects visual direction:

- product, industry, audience, core task, context of use, and content density
- target surfaces and priority device; one visual language may have multiple platform adaptations
- existing brand assets, constraints, real content, localization, accessibility target, and repository stack
- desired traits, rejected traits, competitors to approach or avoid, and delivery scope

Detect the implementation environment from the repository when possible. Technology affects implementation, not the aesthetic thesis. Ask only for missing information that would materially change the result.

Read [references/platform-routing.md](references/platform-routing.md), then load only the relevant platform files.

## Stage 1: discover references and obtain approval

Read [references/reference-discovery.md](references/reference-discovery.md).

1. Form three meaningfully different visual hypotheses from the brief.
2. Build Chinese and English search terms for each hypothesis.
3. Search suitable public design sources. Prefer a real source page and record its URL; use image search for broad discovery and a browser for visible site context when available.
4. Filter out duplicates, low-resolution images, isolated decorative shots, structurally impossible concepts, and references that cannot support the user's content.
5. Present a reference board with normally 3–5 images per direction and 9–12 images total. For a narrow request, use fewer.
6. Explain the composition, palette, type character, density, imagery, motion potential, strengths, and risks of each direction.

If a source is unavailable, do not invent results. Provide the exact search terms and ask the user to upload or select references. Never download a reference image as a production asset.

### Gate A — Reference Decision

Stop and let the user select, reject, remix by named trait, request another search, or upload their own reference. Record:

- primary reference
- optional secondary references and the single trait each contributes
- selected and rejected traits
- non-negotiables and known platform targets

When artifacts are being persisted, record the explicit selection with `design_workspace.py select`. Do not enter Stage 2 in Guided mode until the user has made this decision.

## Stage 2: derive and validate the visual standard

Read [references/reference-analysis.md](references/reference-analysis.md) and [references/visual-standard.md](references/visual-standard.md).

Analyze the chosen reference set as one system:

- creative thesis, emotional intent, brand character, and memorable gesture
- hierarchy, reading path, grid, composition, whitespace, density curve, and responsive transformation
- semantic palette and contrast, typography, icon grammar, spacing, radii, borders, elevation, material, imagery, and motion
- components, states, content behavior, and platform-specific adaptations

Separate three kinds of statements:

- **Observed**: visible in the reference.
- **Inferred**: likely but not provable from the available artifact.
- **Proposed**: a new decision required for this product.

Create a versioned standard containing:

- `MASTER.md` with the creative thesis and rules
- machine-readable semantic tokens
- a low-fidelity layout for each priority form factor
- a rendered style tile
- one representative mid-fidelity application when visual risk is high
- source attribution and a decision log

Use deterministic HTML/SVG/Figma or the project's UI stack for wireframes and style tiles when structural accuracy matters. Use image generation for imagery or expressive exploration, not for precise UI specifications.

### Gate B — Standard Approval

Show the visual artifacts and summarize open risks. Stop for approval or revision. Once approved, record the version with `design_workspace.py approve`. The approved standard becomes the source of truth; later deviations require an explicit page override or a revised standard.

## Stage 3: implement the approved direction

Read [references/implementation-and-qa.md](references/implementation-and-qa.md) and the relevant platform file(s).

1. Check the decision workspace. In Guided or Reference-led mode, do not implement if Gate B is unconfirmed.
2. Read the approved standard, page overrides, real content, and existing code conventions.
3. Implement responsive structure, components, states, and meaningful motion in the detected stack.
4. Preserve platform-native behavior while mapping shared brand tokens appropriately.
5. Render the interface on the target sizes; include compact and expanded conditions where relevant.
6. Compare screenshots to the approved thesis, style tile, and composition rules.
7. Fix the highest-impact problems: weak focal point, generic template patterns, rhythm, inconsistent imagery/type/icons, broken responsive composition, or missing interaction states.
8. Run accessibility, interaction, performance, and stack-specific checks in proportion to scope.

## Platform routing

- Web and responsive browser UI: [references/platforms/web.md](references/platforms/web.md)
- iPhone and iPad: [references/platforms/apple-mobile.md](references/platforms/apple-mobile.md)
- Apple Watch: [references/platforms/watchos.md](references/platforms/watchos.md)
- Android phones, tablets, foldables, and Wear OS: [references/platforms/android.md](references/platforms/android.md)
- Windows desktop: [references/platforms/windows.md](references/platforms/windows.md)

When a product spans platforms, keep shared brand primitives in the master standard and put navigation, typography mapping, spacing/density, hit targets, window/safe-area behavior, and platform components in named overrides.

## Deliver with evidence

State the selected references, approved standard version, implemented surfaces, test sizes, visual changes made after screenshot review, and unresolved constraints. Do not claim a platform or interaction was tested unless it was actually rendered or exercised.
