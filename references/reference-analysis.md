# Reference analysis

Analyze the selected set as a coherent visual language. The primary reference controls the overall grammar; secondary references may affect only their assigned traits.

## Evidence labels

Mark consequential conclusions as:

- **Observed** — directly visible or measurable.
- **Inferred** — plausible but not provable from the artifact.
- **Proposed** — created to make the direction work for this product or platform.

Do not claim an exact font family, animation, breakpoint, token, or component behavior from a static screenshot unless reliable supporting evidence exists.

## Analysis frame

### Creative thesis

Define the interface's core metaphor, emotional target, brand personality, signature moment, three principles to preserve, and three clichés to avoid.

### Hierarchy and composition

Describe focal points, reading path, grid, alignment anchors, dominant ratios, controlled rule-breaking, whitespace, section rhythm, density changes, and how the composition transforms rather than merely shrinks.

### Color

Sample representative colors when possible, consolidate near-duplicates, and map them to semantic roles. Include foreground pairs, surfaces, border, focus, destructive, warning, success, and information roles. Validate important foreground/background pairs; do not treat sampled colors as automatically accessible.

### Typography

Analyze classification, width, contrast, x-height, weight, case, tracking, line length, hierarchy, numeric behavior, and multilingual needs. If the exact face is unknown, propose licensed or system-safe visual equivalents and label them as proposed.

### Geometry and material

Separate radii by component role. Analyze strokes, corners, shadows, elevation, blur, translucency, grain, gradients, highlights, image masks, and depth. Explain which effects carry meaning and which are decorative.

### Icons and imagery

Define icon family character, fill/stroke, stroke width, corner treatment, optical size, active states, containers, and accessible labeling. Define imagery medium, crop, camera angle, lighting, subject scale, color grading, texture, and fallback behavior.

### Motion

Infer a motion character from the visual language, then propose interaction-specific behavior. Cover entry, exit, press, hover where applicable, expansion, navigation, data updates, interruption, and reduced-motion outcomes. Do not attach decorative motion presets that contradict the visual thesis.

### Components and states

Map the language onto navigation, buttons, inputs, cards/surfaces, lists, tables or charts, dialogs/sheets, feedback, empty, loading, error, disabled, focus, selected, and destructive states as required by the product.

### Cross-platform translation

Separate invariant brand primitives from adaptive platform behavior. Preserve recognizable color, type character, icon grammar, imagery, material, and signature gestures while remapping navigation, density, control shapes, system typography roles, safe areas, and input behavior.

## Synthesis check

Before drafting the standard, test the proposed parts together:

- Do type, palette, imagery, geometry, and motion express the same thesis?
- Can the actual content fit without fake cards or placeholder copy?
- Is the result distinguishable without relying on one decorative effect?
- Are secondary references causing visible style collage?
- What breaks first on the smallest target surface?
