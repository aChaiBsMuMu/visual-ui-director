# Specimen schema v1

The renderer supports Python 3.9+ and uses no external packages. TOKENS.json keeps existing `color`, `typography`, `space`, `size`, `radius`, `border`, `shadow`, `motion`, `platform` namespaces; add scoped roles freely. Set `meta.status` to `ready` only when authored. There is no universal color, spacing step, radius, font or component inventory.

A reference is `{namespace.path}`. Nested aliases are supported with cycle detection. Colors resolve to opaque six-digit HEX; numbers are finite unitless logical SVG units. Platform-specific unit conversions belong to platform overrides. Transparent material can be described in the manual; this renderer's contrast checker requires an opaque composited pair. Do not silently flatten transparency and claim it was validated.

Typography `typography.roles.NAME` has `font_family`, `font_size`, `weight`, `line_height` (absolute units), `tracking`, `color`; each may alias another token. `shadow.ROLE` is an object with `dx`, `dy`, `blur`, `color`, `opacity`. Icon cap and join are tokens with SVG enum values. Remaining scalar parameters can live anywhere under semantic paths.

## SPECIMENS.json

Required top-level fields: schema_version: 1, status: ready, title, languages, colors, typography, geometry, patterns, components, icons, imagery, motion_cue. See the executable [Margin example](../../examples/phase-2/README.md) and [configuration template](../../assets/templates/phase-2/specimens.json).

- `colors[]`: group (`Brand`, `Neutral`, `Semantic`), role, token, pair, usage, frequency, do, dont. Default min_contrast = 4.5. Any other threshold requires contrast_reason describing the text/non-text role and applicable requirement. Both token and pair are token references. All semantic palette roles used in the product should be represented, including alias roles.
- `typography[]`: role (key in typography.roles), sample (actual language content). Display/H1/H2/Title/Body/Label/Caption/Numeric are scope-selected role names, not prescribed fonts or sizes.
- `geometry.spacing[]`, `geometry.radii[]`: label, token. `borders[]`: label, width and color references. `surfaces[]`: label, color, radius and shadow references. Include explicit zero-elevation samples when appropriate.
- `patterns[]`: id, name, purpose, reading_path, density, scrolling, avoid, transformation, regions. Each region has x/y/w/h in normalized 0–100 relationships, label and level (`primary`, `secondary`, `tertiary`, `background`). These are diagram relationships, not competing production pixel tokens. Define separate compact/expanded variants as applicable. Keep labels short enough for regions; the renderer fails on overflow.
- `components[]`: id, kind (`button`, `surface`, `input`, `navigation`, `tabs`, `chip`, `feedback`, `text`), name, why, content_rule, typography role name, width/height/padding token references, states. Each state has name, label and bg/fg/border/border_width/radius references; optional focus color reference. Navigation/tabs may include `items` labels, `active_index`, `active_fg` token reference and `focus_index` so only the actual item receives selected/focus emphasis. Multiple component entries can represent variants. `omitted_states` maps non-applicable state names to reasons. The manual supplies full anatomy, transitions, interactions, platform differences and design judgment. Unsupported anatomy requires extending the renderer or using the product stack; the built-in primitive is never proof of a runtime interaction.
- `icons[]`: name, source, accessible_label, container_rule, grid/stroke/cap/join token references, sizes (references), paths (SVG path geometry), states mapping applicable default/active/selected to color reference, fill (`outline`/`filled`), optional container and radius references. Use omitted_states with reasons for non-applicable icon states, such as a back action that is never selected. Production source is explicit; custom fixture paths do not impersonate a library.
- `imagery`: mode `image` with a local relative PNG/JPEG file and caption, or mode `none` with product-specific reason. Actual image data is embedded, never fetched by the SVG.
- `motion_cue`: descriptive state/continuity diagram text referencing the motion rules; exact parameter values stay in tokens.

Empty components/icons require components_omission/icons_omission explaining the product scope, plus a matching bounded review exception. This does not waive the corresponding document or sheet. Colors/type/layout cannot be omitted.

## Review and locks

REVIEW.json uses the [review template](../../assets/templates/phase-2/review.json): context, loaded contract hash, influence index, DNA tests, scoped exceptions, 15 coherence checks, representative mapping and reviewer. Each check cites an existing relative file plus optional anchor and a substantive reason. Evidence presence is machine-verifiable; truth of a review judgment requires actual inspection.

`evidence/render-manifest.json` is generated, with input/output SHA-256 and contrast results. Do not edit it to bypass stale evidence; re-render. Gate B additionally freezes all manual/evidence inputs in project.json's version lock. LOCK.json is a readable receipt. Existing CLI parameter names remain valid.

Run `phase2 review --reviewed-by "reviewer"` after actual inspection and completed checks. It records reviewed_inputs hashes. Any later manual or evidence edit requires another inspection and review seal, even if specimens were regenerated.
