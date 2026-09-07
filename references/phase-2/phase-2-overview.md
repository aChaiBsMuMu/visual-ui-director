# PHASE 2 — ANALYZE & DEFINE

Mission: turn REFERENCE_CONTRACT into Design Strategy + Visual DNA + a complete, scope-aware UI Design Manual + visual specimens. Phase 1 asks whose references; Phase 2 decides why and how; Phase 3 executes the locked answer.

## 2.0 Preconditions

Run `phase2 start --root PROJECT --version v1` after Gate A. Confirm product, users, task, content shape, platform, target device and smallest supported surface. Require one primary, at most two bounded secondary contributions, Selected Traits, Rejected Traits and Do Not Copy (explicit none is valid). Direct may assume a reference lock and record an explicit proposed baseline when no external reference exists, but cannot skip analysis or the manual. Use `select` to record that baseline; never call a proposal an observed reference.

## Dependency order

1. Evidence: inventory sources and classify Observed / Inferred / Proposed.
2. Deep analysis: [twelve dimensions and reasoning chain](deep-reference-analysis.md).
3. Cross-reference synthesis: [influence boundaries](cross-reference-synthesis.md), with provisional fit judgments.
4. Design judgment: [decisions and tradeoffs](design-judgment.md); resolve synthesis conflicts, rather than silently blending them.
5. [Design strategy](design-strategy.md): why this product takes this direction.
6. [Visual DNA](../visual-dna.md): 5–8 stable, screenshot-testable behaviors.
7. [UI Design Manual](design-manual.md): how each behavior is implemented.
8. [Visual specimens](visual-specimens.md): render text specifications as inspectable sheets.
9. Representative screen: real or near-real content, formal tokens, a named pattern and specified components; choose the greatest system risk or identity test.
10. Coherence validation and [Gate B](gate-b-validation.md).

Persist per-version REFERENCE_ANALYSIS.md, DESIGN_JUDGMENT.md and REFERENCE_INFLUENCE.md before strategy. REVIEW.json contains verification metadata, evidence links, scope exceptions and the hash of the loaded reference contract; it is not a second design parameter store. Do not create another DESIGN_SYSTEM directory.

The complete delivery is analysis, judgment, strategy, DNA, manual, tokens, seven SVG sheets and a representative screen. Missing substantive work is a blocker even in Direct mode.
