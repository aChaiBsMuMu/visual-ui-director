# 静读 / Margin — Design Strategy

Fictional demonstration; proposed design, not a sampled production system.

## Product Visual Problem

People arriving after work face too many equal choices. Margin must make choosing a single twelve-minute essay easier than scanning an infinite feed. J-01 and J-11 tie hierarchy to that task.

## Desired User Perception

Unhurried means one dominant essay title, one committed action and no auto-advancing feed. Reliable means stable reading position, explicit save feedback and real focus indication. These are visible behaviors, not atmosphere adjectives.

## Creative Thesis

Give one thoughtful essay enough space to earn the reader’s attention. Editorial title character carries identity; browser-native behavior preserves confidence.

## Design Priorities

First preserve title comprehension, then reading continuity, then discovery. Secondary navigation and saved items must recede whenever they compete with the current essay.

## Design Tensions

Editorial over systematic for article hierarchy; systematic over editorial for editing and navigation. Spacious in the decision region, medium density in the archive. Brand color governs commitment; native link behavior wins over branded interaction.

## Product Goal → Visual Strategy Matrix

| Product Goal | Desired Perception | Visual Behavior | Design Decision | Rule | Failure Signal |
|---|---|---|---|---|---|
| Start one essay | Low pressure | One dominant title | J-01, J-04 | One title leads the first glance | Four equally loud previews |
| Resume reliably | Trust | Stable column and visible save result | J-09 | State feedback leaves text in place | Toast obscures current paragraph |

## Visual Budget

Color Budget: warm neutrals carry the reading area. Accent Budget: one committed reading action per decision region. Card Budget: no cards around ordinary paragraphs or article rows. Radius Budget: controls and selected filters have separate roles; editorial surfaces remain square. Shadow Budget: only transient overlays. Border Budget: editable fields and necessary boundaries. Motion Budget: feedback and navigation continuity only. Decorative Effect Budget: zero unsolicited gradients, blur or floating ornaments.

## Design Non-negotiables

Primary essay text must fit in Chinese and English. Secondary actions cannot match the primary CTA’s color area. Content hierarchy must survive absent imagery. J-03, J-06 and J-08 are non-negotiable.

## Design Risks

A very long Chinese title can dominate all useful space; allow wrapping and place metadata after it. System serif fallback may change line breaks, so inspect the target browser. Avoid shrinking type to rescue a fixed-height hero.

## Anti-patterns

Equal card grids, oversized save buttons, all-red navigation icons and image placeholders are failure signals here. They add choice pressure or visual competition instead of supporting the reading task.
