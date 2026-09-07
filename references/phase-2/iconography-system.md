# Iconography system

Define outline/fill with state logic, grid, stroke width, cap, join, corner treatment, optical size, size roles (e.g. 24/20/16 where justified), inactive/active/selected states, container rules, color and accessible labels. Explain the relationship between icon and text; icons usually support the task rather than compete with primary content.

Choose a production source by platform and needed coverage: SF Symbols, Lucide, Material Symbols or custom are options, not defaults. Record source/license or system availability. Do not mix libraries, stroke weights or filled/outline styles without an explicit semantic or platform rule. Do not put every symbol inside a circle.

SPECIMENS.json supplies representative SVG paths and token references for grid, size, stroke and states; paths are geometry assets, never evidence that a production library was installed. Label custom specimen paths honestly. For SF Symbols use actual permitted platform output for final native checks; approximations must remain labeled proposals. Render grid, sizes, default/active/selected states, container rules and icon + label in icon-style-sheet.svg. Do not use image generation for this sheet.
