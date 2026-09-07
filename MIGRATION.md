# Migrating to the Phase 2 design manual (2.1)

No existing CLI command was removed: init, status, select, approve, score, audit, override, history and migrate keep their entry points. `approve --gate b` and its evidence arguments remain accepted. New `phase2 start|render|review|validate|upgrade` commands add analysis, deterministic specimens, review binding and versioning. Workspace schema becomes 3; release version is 2.1.

## Preserve the previous version

The repository pre-upgrade version is tagged `backup-pre-phase2-20260907`; v2.0.0 also remains available. Before migrating an actual product workspace, copy it or use your repository backup. `phase2 upgrade` preserves the source standard and creates a new draft; `init --force` now moves the previous workspace to a dated backup instead of overwriting it in place.

## Existing .design-director (2.0)

Read-only status/history and existing score/audit/override records remain usable. Old Gate B approval is not silently treated as proof of a complete Phase 2 manual. `status --require implement` and Gate C require a validated current lock, including Direct mode.

```bash
python3 scripts/design_workspace.py phase2 upgrade --root /path/to/project --version v2
python3 scripts/design_workspace.py phase2 start --root /path/to/project --version v2
```

Then:

1. Review the Reference Contract. Every reference needs a source and contribution; no more than two secondaries. Resolve any old “unspecified” contribution with `select`. Direct may record an explicit proposed baseline without waiting for manual selection.
2. Retain authored decisions from the old standard. Complete the new analysis, judgment, influence map and design strategy before the new DNA and manual.
3. The old root visual-dna.md is saved to history/visual-dna-before-phase2.md and carried into the new version, then replaced by a compatibility symlink. The version's VISUAL_DNA.md becomes the sole owner. Add the required source/pass/failure review records for its 5–8 principles.
4. Legacy SPACING.md remains in the source version. Consolidate its authored rules into new SPACING_GEOMETRY.md; the new SPACING.md is a router, not a second editable standard. MASTER and the other old documents are preserved for deliberate completion, never replaced with generic choices.
5. Retain existing token namespaces and values; adapt the scoped renderer configuration to semantic token references. Add typography/shadow/icon role shapes as documented in the specimen schema. Do not replace a project's palette with the example palette.
6. Complete SPECIMENS.json, render all sheets, render the representative screen, and complete REVIEW.json after inspection. Run `phase2 review`, then `phase2 validate`, then approve Gate B. Supplemental CLI evidence paths must match already reviewed content; new evidence must be inspected and included before locking.
7. Resume Phase 3, preserving score thresholds, screenshot critique, platform QA and page override history.

Once locked, changing global inputs makes the lock stale; create v3 rather than overwriting v2. Updating the Reference Contract also invalidates implementation eligibility until a new version is approved. Bounded page exceptions continue through `override`; they do not silently change the global tokens.

## What the validator does and does not prove

It enforces files, meaningful sections, obvious placeholder rejection, source boundaries in structured records, 5–8 distinct DNA entries with tests, token/config integrity, required evidence formats, contrast pairs, review coverage and SHA-256 freshness. It cannot infer whether an asserted design rationale is true, a font is installed, or an interaction works. Actual visual and runtime review remain required.

## Existing .visual-ui (1.x)

Back up the project, then run:

~~~bash
python3 scripts/design_workspace.py migrate --root /path/to/project
~~~

The command preserves the original .visual-ui directory and creates a new .design-director workspace. Legacy references and standards are carried forward where possible, but the new Phase 2 contract additionally requires:

1. Review and complete REFERENCE_CONTRACT.md.
2. Complete the full Phase 2 analysis, strategy, 5–8 DNA principles and design manual.
3. Render the seven spec sheets and representative screen, complete coherence review, and reapprove Gate B.
4. Run Screenshot Critic and record a complete score.
5. Pass Gate C before claiming production-ready visual implementation.

The 1.x source release remains recoverable independently; migration never deletes it.
