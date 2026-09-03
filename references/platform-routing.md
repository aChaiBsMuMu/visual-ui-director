# Platform routing

Use a shared creative thesis across targets, then load only the relevant platform references.

## Detect targets

Infer targets from the brief and repository when reliable:

- Web: HTML/CSS, React, Next.js, Vue, Svelte, Angular, browser build files
- Apple: Xcode projects, Swift/SwiftUI, UIKit, iOS/iPadOS/watchOS targets
- Android: Gradle, Android manifests, Kotlin/Java, Compose, Wear OS modules
- Windows: WinUI, WPF, Windows App SDK, .NET desktop, Avalonia/Uno when targeting Windows
- Cross-platform: Flutter, React Native, Kotlin Multiplatform, .NET MAUI

Cross-platform technology does not erase platform differences. Identify which targets share code and which need native behavior or token aliases.

## Shared versus adaptive

Keep these shared when feasible:

- creative thesis and brand personality
- semantic palette intent
- type character, icon grammar, imagery, and material
- spacing rhythm and motion character
- component naming and content hierarchy

Adapt these by platform:

- navigation model and system bars
- typography role mapping and dynamic type
- density, safe areas, window size, orientation, and multitasking
- pointer, keyboard, touch, crown, bezel, rotary, pen, and gamepad input
- hit targets, gestures, focus, hover, context menus, and back behavior
- native controls, permissions, notifications, complications/widgets, and lifecycle

## Multiple targets

Define one priority surface and at least one compact and expanded condition. Put platform differences in named overrides rather than weakening the master rules into vague averages.
