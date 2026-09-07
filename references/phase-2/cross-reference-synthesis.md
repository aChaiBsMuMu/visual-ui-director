# Cross-reference synthesis

Primary controls overall visual grammar. A secondary contributes only the exact trait approved by Gate A. Its attractive unassigned colors, corners, fonts or effects must not leak in. Do not average incompatible references. Reject a contribution when product fit fails; explain any proposed replacement.

Write REFERENCE_INFLUENCE.md with a REFERENCE INFLUENCE MAP:

| Design dimension | Source | Contract contribution | Allowed | Rejected | Adaptation | Judgment ID |
|---|---|---|---|---|---|---|

Cover all twelve analysis dimensions; multiple rows are allowed. Example: Primary → color and type; Secondary A → photography crop only; Secondary B → navigation density only. Secondary A glassmorphism remains rejected. Explain conflicts in DESIGN_JUDGMENT.md.

REVIEW.json records machine-checkable influence entries: source `primary`, `secondary:1`, `secondary:2`, or `proposed`; exact contribution; dimension; decision `allowed`, `adapted` or `rejected`; rationale and judgment ID. This is a review index into the prose, not a second manual. A rejected decision can document an out-of-bound trait; an allowed/adapted secondary must match its contracted contribution. Semantic leakage still requires visual review: a hash or exact string comparison cannot prove design intent.
