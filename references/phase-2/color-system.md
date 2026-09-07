# Color behavior and palette

Derive roles and distribution before choosing values. Distinguish base (canvas, surface, elevated surface, primary/secondary/tertiary text, border, divider), brand (primary, secondary, soft, strong, hover, pressed, container) and semantic (success, warning, error, info, focus, disabled, selected) palettes. A small product can alias roles rather than invent unused colors; document why.

COLOR.md records for every used color: role, token reference, foreground pair, usage, frequency, Do and Don't. TOKENS.json owns values; prose may display a generated value but must not become an independently edited palette. Brand and success are separate semantics even when a product explicitly aliases their values. Error and destructive meanings must not be overwritten by brand color.

Estimate Neutral / Brand / Semantic / Image Color distribution only when evidence permits. Label visual estimates Inferred, record measurement method for Observed proportions, and never manufacture exact percentages. Set a budget for high-area neutrals, limited accents and state-only colors.

Check actual critical text/background pairs and focus/control boundaries for the project's accessibility target, including alternate themes. Record ratios and roles. The renderer verifies configured foreground pairs numerically; disabled or non-text exceptions need an explicit rationale and applicable threshold, not a silently weakened default. Render [color-palette-board.svg](visual-specimens.md) with token, HEX, role, foreground pair, usage and Do/Don't.
