# Visual standard

Create a practical digital visual-identity package, not a prose-only mood description. Use a version such as `v0.1` while drafting and mark the approved version explicitly.

## Required master sections

1. Scope, target platforms, source references, and evidence labels
2. Creative thesis, emotional target, signature moment, preserve/avoid rules
3. Content hierarchy, grid, composition, whitespace, and density curve
4. Semantic colors with light/dark mappings and tested foreground pairs
5. Typography roles, multilingual fallback, numeric styles, line length, and fluid behavior
6. Spacing, sizing, radii by role, strokes, elevation, material, and imagery
7. Icon grammar and recommended production library
8. Motion principles, tokens, interaction mapping, interruption, and reduced motion
9. Core components and required states
10. Platform adaptations and named page/surface overrides
11. Accessibility and implementation risks
12. Decision log and approval status

## Semantic token contract

Provide machine-readable tokens where code will be implemented. Prefer semantic names such as:

```json
{
  "color": {
    "bg.canvas": "#F7F5F0",
    "bg.surface": "#FFFFFF",
    "text.primary": "#171713",
    "text.secondary": "#5F625A",
    "action.primary": "#245B45",
    "focus.ring": "#2B73FF"
  },
  "radius": {
    "control": "10px",
    "surface": "18px",
    "overlay": "24px"
  },
  "motion": {
    "feedback": "120ms",
    "transition": "240ms"
  }
}
```

Add platform aliases only where units or native roles differ. Avoid raw color names tied to one current palette.

## Required rendered artifacts

### Low-fidelity layout

Produce layouts for the priority form factors. Show hierarchy, regions, major controls, real content shape, scroll/fixed behavior, and responsive transformation. Use deterministic HTML, SVG, Figma, or the implementation stack when accuracy matters.

### Style tile

Render the selected palette, type hierarchy, buttons, inputs, surfaces, tags, icons, imagery treatment, state colors, radii, borders, and elevation together. A token table without this combined view is insufficient.

### Representative application

When the style is novel, image-dependent, dense, or spans very different surfaces, render one mid-fidelity region before approval. Choose the region with the greatest visual risk, not the easiest component.

## Approval presentation

Show the artifacts, summarize observed/inferred/proposed decisions, identify unresolved assets or licensing questions, and name any platform adaptation that will intentionally differ from the reference. Invite targeted revision by dimension instead of asking only “Is this okay?”
