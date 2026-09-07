# UI Design Manual and source ownership

The canonical manual lives in `.design-director/standards/<version>/`. It contains MASTER.md, DESIGN_STRATEGY.md, VISUAL_DNA.md, COLOR.md, TYPOGRAPHY.md, LAYOUT.md, SPACING_GEOMETRY.md, COMPONENTS.md, ICONOGRAPHY.md, IMAGERY.md, MOTION.md, RESPONSIVE.md, PAGE_PATTERNS.md, DO_DONT.md, TOKENS.json, SPECIMENS.json, REVIEW.json, the three analysis/judgment/influence records, PLATFORM_OVERRIDES/, PAGE_OVERRIDES/ and evidence/.

MASTER is a brief entry, with Creative Thesis, Product Character, Design Priorities, Design Tensions, DNA Summary, Color Summary, Typography Summary, Layout Grammar, Geometry Summary, Component/Icon/Imagery/Motion Character, Signature Gestures, Platform Rules, Source Documents and Approval Status. Link detail rather than copying it. Approval state is authoritatively recorded in project.json and the lock; master points there and states the requested revision status.

Contract = selected source boundaries. Analysis = reference mechanisms. Judgment = fit and tradeoffs. Strategy = chosen approach and why. DNA = stable observable behavior. Manual = implementation rules. Tokens = sole parameter values. Specimens config = what to show (token references, text and geometry relationships, not shadow palettes). Visual specimens = generated views. Representative screen = integrated proof. REVIEW.json = review assertions and evidence, not design values.

Root visual-dna.md is a compatibility symlink to the current version's VISUAL_DNA.md. SPACING.md is a compatibility router. `phase2 upgrade --version v2` copies a legacy/current version into a new draft without overwriting the source. Global changes after Gate B need a new version. Bounded page exceptions use existing `override`; its JSON record remains canonical, without duplicating those records inside PAGE_OVERRIDES. The latter can hold pre-lock page guidance; the root overrides/ records are the canonical Phase 3 exceptions.

DO_DONT.md records project-specific paired good/bad behaviors, visible failure signals, J/DNA IDs and specimen or screen regions. Do not use a fixed checklist as a substitute for judgment.

RESPONSIVE.md applies Brand → Product Visual → Platform Adaptation → Device Context. Brand owns color intent/type/icon/material character; Product owns task hierarchy; Platform owns navigation, native controls, input and text roles; Device owns window, safe area, density, pointer/touch/watch context. Same identity does not require pixel identity. Load only applicable [platform routes](../platform-routing.md).
