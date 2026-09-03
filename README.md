# Visual UI Director

A reference-led Codex skill for designing visually distinctive interfaces across Web, iOS, iPadOS, watchOS, Android, Wear OS, and Windows.

It uses a three-stage workflow:

1. Discover visual references and let the user choose the aesthetic direction.
2. Derive an actionable visual standard with tokens, wireframes, and a rendered style tile.
3. Implement the approved direction and validate it through rendered screenshots.

The skill is intentionally platform-adaptive: one creative thesis, shared brand primitives, and explicit platform overrides.

## Use

Install the `visual-ui-director` folder in your Codex skills directory, then invoke:

```text
$visual-ui-director Help me explore and build a cross-platform interface for ...
```

The default Guided mode pauses for reference selection and visual-standard approval. Reference-led and Direct modes are also supported.

## Decision workspace

For persistent projects, the bundled helper creates versioned decision artifacts:

```bash
python3 scripts/design_workspace.py init \
  --root /path/to/project \
  --project "Project Name" \
  --platform web \
  --platform ios \
  --mode guided
```

Run `python3 scripts/design_workspace.py --help` for the remaining commands.
