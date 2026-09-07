# Deterministic visual specimens

Use Python standard-library SVG, HTML/CSS, Figma or the product stack for accurate spec sheets. Image generation is for photography, illustration, texture and mood, never palette, type, wireframe, component or icon grids.

`phase2 render --root PROJECT --version v1` reads TOKENS.json and SPECIMENS.json, then emits color-palette-board.svg, typography-specimen.svg, spacing-geometry-sheet.svg, layout-atlas.svg, component-specimen.svg, icon-style-sheet.svg and style-tile.svg. Standalone: `python3 scripts/render_design_specimens.py --standard PATH`. Rendering never approves the design or fabricates a representative screen.

Use [the schema contract](specimen-schema.md). All style parameters resolve token references; examples and pattern regions remain scope-specific config. Renderer metadata hashes both input files and output bytes, so Gate B rejects stale or altered generated sheets. Numeric contrast reports are generated for configured pairs; meaningful pair coverage still requires review.

Style tile integrates palette, real type samples, buttons/core components/states, icons, imagery or reasoned absence, geometry, border/surface/material and a motion cue. It uses the same primitives/config as individual sheets. Do not create a second visual system.

Representative screen is separately rendered with realistic content and official tokens, a named pattern and component inventory. Choose a page exposing the greatest risk or strongest identity; record selection rationale, viewport, smallest-screen check and mapping to strategy/DNA/manual in REVIEW.json. Verify all target form factors in the atlas and render the smallest supported layout in real UI when its content risk warrants it.

Open actual SVGs in a browser or render them to pixels. Check text, font fallback, clipping, non-empty shapes, dimensions and intelligible labels. SVG syntax validation is necessary but does not prove visual quality, interaction, correct font availability or semantic coherence.
