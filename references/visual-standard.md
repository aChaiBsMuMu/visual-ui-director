# Visual standard

Create a versioned, implementable digital visual-identity package. Keep Visual DNA above the token level and split detailed disciplines into focused documents.

## Target structure

~~~text
DESIGN_SYSTEM/
├── MASTER.md
├── VISUAL_DNA.md
├── TOKENS.json
├── COLOR.md
├── TYPOGRAPHY.md
├── SPACING.md
├── ICONOGRAPHY.md
├── IMAGERY.md
├── MOTION.md
├── COMPONENTS.md
├── RESPONSIVE.md
├── PLATFORM_OVERRIDES/
└── PAGE_OVERRIDES/
~~~

MASTER.md contains only the creative thesis, visual identity, core principles, system relationships, scope, source references, and approval status. Do not turn it into an encyclopedia.

## Routed disciplines

- [Visual DNA](visual-dna.md)
- [Color discipline](color-discipline.md)
- [Typography character](typography-character.md)
- [Spacing rhythm](spacing-rhythm.md)
- [Imagery direction](imagery-direction.md)
- [Motion direction](motion-direction.md)
- [Responsive composition](responsive-composition.md)

Iconography defines family, fill/stroke, weight, corners, optical size, active state, container use, accessible labels, and a licensed production source. Components define content rules and necessary states rather than merely cataloging shapes.

## Semantic token contract

Provide machine-readable semantic tokens when code will be implemented. Prefer names such as color.bg.canvas, color.text.primary, color.action.primary, radius.control, radius.surface, motion.feedback, and motion.transition. Add platform aliases only where native roles or units differ. Raw palette names may exist as primitives but must not be the only interface.

## Required visual evidence

- Low-fidelity composition for every priority form factor, showing hierarchy, regions, real content shape, fixed/scrolling behavior, and transformation rules.
- A rendered style tile combining color, type, controls, states, imagery, icons, geometry, borders, elevation, and motion cues.
- One representative mid-fidelity screen chosen for visual risk.

Use deterministic HTML/SVG/Figma or the product stack for structural evidence. Use image generation for expressive imagery and exploration, not precise UI specifications.

## Page overrides

An exceptional screen records Screen, Override, Reason, Scope, and Does Not Change. A page need must not silently mutate the global system.

## Approval

Present Visual DNA, the focused system documents, style tile, representative screen, evidence labels, unresolved assets/licensing questions, and intentional platform differences. Invite revision by dimension. Gate B approval freezes the version until an explicit revision or override.
