# Android and Wear OS adaptation

Use current Android platform guidance and the repository's minimum/target SDK as constraints; verify unstable numeric platform guidance from official sources when it matters.

- Support edge-to-edge layouts, system insets, font scaling, TalkBack, gesture and predictive back behavior, dark theme, and reduced motion where available.
- Design adaptive navigation and panes for phones, tablets, foldables, desktop/windowed Android, and posture changes. Do not stretch a phone column across an expanded window.
- Preserve native semantics, ripple/state feedback, system permissions, text input, and lifecycle behavior even with a custom visual language.
- For Wear OS, optimize for glanceability, rotary input, round/variable screen shapes, complications/tiles, short sessions, and one primary task per screen.
- Map shared brand tokens to platform roles rather than forcing Apple or web component geometry onto Android.

Test a compact phone width, an expanded tablet/foldable condition, font scaling, dark theme, gesture navigation, keyboard/focus where relevant, and the smallest supported wearable canvas.
