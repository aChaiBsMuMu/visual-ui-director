# Visual drift

Use for 15+ screens, multiple contributors, long-running projects, or repeated exceptions.

## Detect

- radius families widening or collapsing
- card anatomy changing without content reason
- brand-color budget or semantic role shifting
- unstable type hierarchy or numeric treatment
- mixed photography, illustration, 3D, or grading
- icon family, weight, fill, or optical-size changes
- layouts reverting to generic templates
- page exceptions without recorded overrides
- screens violating Visual DNA or rejected traits

## Evidence

Compare rendered screens plus structured screen metadata when available. Group differences into intentional override, platform adaptation, or unexplained drift.

Use design_workspace.py audit --manifest screens.json for deterministic checks. The manifest contains a screens array; each screen may include radius, brand_color_budget, type_scale, imagery_style, icon_style, card_signature, dna_match, and override_required.

Output a Visual Drift Report with affected screens, baseline, observed variants, severity, recommended action, and the relevant Visual DNA or system rule.
