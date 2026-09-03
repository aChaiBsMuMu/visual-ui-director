# watchOS adaptation

watchOS is not a miniature phone. Preserve the creative thesis while radically compressing hierarchy and interaction.

- Design for glanceable understanding, brief sessions, one dominant action, and minimal decision depth.
- Prefer concise labels, large meaningful values, strong contrast, and progressive disclosure. Avoid dense navigation, long forms, dashboards, and phone-sized card grids.
- Account for small rectangular displays, rounded screen corners, bezels, safe content areas, wrist movement, Always On behavior where relevant, and Dynamic Type.
- Map interaction to touch, Digital Crown, system gestures, complications, notifications, Smart Stack/widget contexts, and haptics only when the product actually uses them.
- Keep controls comfortably operable and separated; verify with current Apple guidance and the project's deployment target instead of hardcoding one watch size as universal.
- Simplify imagery and icon detail at small optical sizes. Use short, interruptible motion that communicates state quickly.

For every watch design, render at least the smallest and largest supported watch canvases, test long/localized text, inactive/Always On variants when applicable, and confirm what moves to the paired phone.
