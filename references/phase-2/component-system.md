# Scope-aware component system

First derive inventory from product tasks, actual screens, required states and platform. Do not dump Material/Ant Design. A watch may have only a value, action and feedback; a dashboard need not have bottom tabs. Components are interface anatomy and behavior; icons are a separate symbol language.

For each in-scope component record Name, Purpose, Anatomy, Dimensions, Padding, Typography, Icon, Color, Geometry, States, Variants, Content Rule, Interaction, Platform Difference, Token Mapping, Why, Do and Don't. Link the decision J-ID. Explain shape and hierarchy: why this control isn't a pill, why the secondary action must recede, why a surface needs containment.

Cover applicable Default, Pressed, Hover, Focus, Selected, Disabled, Loading, Error and Destructive states. State explicit non-applicability per component, e.g. no hover on touch-only watch. Focus is required for keyboard-operable targets. Declare state transitions, truncation/wrapping, loading label stability and error recovery; default-state-only drawings cannot validate the system.

The component specimen renders the core inventory and states with actual tokens. Configure multiple examples/variants rather than hardcoding a universal library. Include needed actions, surfaces, input, navigation, tabs/segment, chips and feedback only when in scope. If the SVG renderer lacks an anatomy primitive, add a scoped renderer capability or use the product stack and document the evidence; never substitute an unrelated component.
