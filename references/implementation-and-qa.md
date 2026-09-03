# Implementation and visual QA

## Before implementation

- Confirm the approved standard version or explicit Direct-mode assumptions.
- Inspect the repository, existing components, tokens, assets, fonts, and target platform configuration.
- Identify real content lengths and required states. Do not invent a grid of generic cards just to match a reference.
- Decide which assets are usable, must be generated, need user supply, or require licensing.

## Implementation discipline

- Build shared semantic tokens first, then platform aliases and page overrides.
- Reuse sound project components when they can express the standard; refactor only when the visual or interaction contract requires it.
- Keep one primary visual idea per surface. Avoid decoration that cannot be explained by the thesis.
- Implement loading, empty, error, disabled, focused, selected, destructive, and reduced-motion states in proportion to scope.
- Treat mobile, watch, and compact windows as recompositions, not scaled-down desktop artboards.

## Rendered review loop

1. Run the real interface.
2. Capture screenshots at the target sizes and relevant themes/states.
3. Compare against the creative thesis, reference decision, style tile, low-fidelity composition, and platform override.
4. Rank issues by visual impact.
5. Fix the highest-impact issue and any severe usability/accessibility defects.
6. Capture again and verify the change did not break another target.

Review for:

- weak or competing focal points
- generic hero/card/dashboard templates
- flat section rhythm or accidental density
- inconsistent type, icon, imagery, radius, border, or shadow language
- content that does not fit the selected composition
- secondary references leaking into unassigned traits
- breakpoint collapse, unsafe areas, clipping, overlap, or hidden controls
- ambiguous states, missing feedback, focus, contrast, and motion problems

## Delivery evidence

Report what was actually rendered, viewport/device or window sizes, themes/states, accessibility checks, deviations from the approved standard, and remaining asset or platform constraints. Do not turn an unchecked checklist into a claim of testing.
