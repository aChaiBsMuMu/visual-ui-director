# 静读 / Margin — Components

Fictional demonstration; proposed design, not a sampled production system.

## Scope and Inventory

The actual inventory is read-primary, save-secondary, essay-surface, search, navigation, reading-filter and feedback. No data table, bottom tab bar or desktop card dashboard is required by this reading product.

## Anatomy and Token Mapping

Each example maps width/height/padding, typography role, foreground/background, border and radius to tokens in SPECIMENS.json. Action anatomy is label within a target; search adds an editable boundary; navigation is aligned text destinations; summary is title plus synopsis without a container; feedback is status plus recovery text. Icon roles are separately specified.

## States and Variants

Buttons show default/pressed/hover/focus/disabled/loading. Search shows default/focus/disabled/error; navigation and filters show default/selected/focus. Feedback includes loading and error recovery. Secondary save is a receding action variant. Hover omissions describe unchanged surfaces and native underline affordances.

## Content and Interaction Rules

Action labels describe the next task. Loading preserves control size; error retains the article and offers retry. Titles wrap rather than disappear into ellipses. Navigation uses actual links; search uses a real input; feedback announces state without moving the reading position.

## Platform Differences

Web keyboard focus is explicit and touch targets stay independently operable. Wide navigation distributes destinations; compact keeps a short text row. No watch or mobile-native control claims are made by this example.

## Design Judgment and Do / Don’t

J-06: a modest rectangular reading action feels operable without toy-like pills; a bordered save control is secondary. Do keep the title leading; Don’t color both CTAs identically. J-05: uncontained summary supports continuous reading; Don’t add a shadow because a component is named surface.
