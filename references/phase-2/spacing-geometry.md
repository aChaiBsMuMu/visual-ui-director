# Spacing and geometry

SPACING_GEOMETRY.md owns spacing scale and micro, component, group, section, macro and hero roles; control/surface/hero radius; stroke, border, divider, elevation, shadow, blur, translucency, containers, image masks and surface relationships. Numeric values live in tokens.

Explain differences by purpose: a tappable control may need a different shape from a content surface or image mask. Equal radii across roles require a reason; pills are not the default. Likewise distinguish an input boundary, a divider and an elevated transient panel. Neither shadow nor border belongs on every content group. State when whitespace replaces containment and when a surface needs an explicit boundary.

Specify compression and invariants at the smallest context. Render spacing lengths, radius comparisons, border styles, surface levels, actual shadow samples and relationship labels in spacing-geometry-sheet.svg. Explain shadow-free and blur-free choices with explicit zero/none tokens or a bounded rationale.
