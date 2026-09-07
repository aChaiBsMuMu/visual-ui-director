# 静读 / Margin — Color

Fictional demonstration; proposed design, not a sampled production system.

## Base Palette

Canvas, surface and elevated are separate neutral roles; text, muted and tertiary carry decreasing content priority. Border marks editable boundaries; divider marks quiet groups. Values are token references under color.semantic.

## Brand Palette

Brand is reserved for the committed reading action. Brand strong is pressed emphasis; brand soft is a selected filter container. Hover aliases brand strong. A second independent brand hue is intentionally unnecessary for this single reading task.

## Semantic Palette

Success, warning, error, info and focus preserve their state meanings. Disabled uses disabled_bg with disabled foreground; selected aliases brand_soft. Destructive actions, if later added, require an error-family rule rather than brand substitution.

## Usage and Foreground Pairs

Each rendered palette-board row supplies the token, its foreground pair, use and frequency. Body uses text/canvas; primary CTA uses on_brand/brand; all states retain readable pairings. Do not use brand as generic metadata ink.

## Color Distribution

Inferred from the synthetic reference: neutral paper occupies most of the viewport and a single accent region recedes from the title. No measured percentage is claimed. There is no image-color contribution in this product.

## Color Budget

Large area: warm neutral canvas. Accent: one reading CTA or current selection per decision region. Brand cannot signal failure and cannot decorate every icon. See the visual budget in DESIGN_STRATEGY.md.

## Accessibility

Configured pairs are numerically checked by the renderer at the declared threshold. Focus is also judged as a boundary in the specimen. Test actual text, fallback and browser zoom before production; numeric pairing alone is insufficient.
