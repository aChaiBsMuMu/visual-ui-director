# Migrating from Visual UI Director 1.x

Version 2.0 preserves Guided, Reference-led, and Direct modes; Gates A and B; one primary plus two secondary references; Observed/Inferred/Proposed analysis; tokens, wireframes, style tiles, rendered QA; and all existing platform routes.

## What changed

- The workspace moves from .visual-ui to .design-director.
- Gate A now creates an explicit Reference Contract.
- Visual DNA becomes a separate 5–8-rule identity layer.
- Visual Standard becomes a versioned, multi-document system.
- Screenshot QA becomes a critique, ten-dimension score, and fix loop.
- Gate C prevents unsupported production-ready claims.
- Score history, visual-drift audit, and page overrides are persisted.

## Existing projects

Back up the project, then run:

~~~bash
python3 scripts/design_workspace.py migrate --root /path/to/project
~~~

The command preserves the original .visual-ui directory and creates a new .design-director workspace. Legacy references and standards are carried forward where possible, but 2.0 still requires:

1. Review and complete REFERENCE_CONTRACT.md.
2. Write 5–8 observable principles in visual-dna.md.
3. Reapprove Gate B with style-tile, representative-screen, and wireframe evidence.
4. Run Screenshot Critic and record a complete score.
5. Pass Gate C before claiming production-ready visual implementation.

The 1.x source release remains recoverable independently; migration never deletes it.
