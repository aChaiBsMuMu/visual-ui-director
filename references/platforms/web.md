# Web platform adaptation

Design for a continuum of viewports, input methods, zoom levels, and content lengths.

- Define composition breakpoints from content failure, not device brand alone. Verify a small phone, an intermediate/tablet width, and the intended desktop maximum.
- Preserve browser zoom and text reflow. Avoid fixed-height text containers and horizontal page scrolling.
- Support keyboard order, visible focus, skip navigation where needed, semantic landmarks, and pointer plus touch behavior.
- Set readable text measure, fluid type/spacing bounds, image aspect ratios, and explicit behavior for navigation, tables, charts, overlays, and dense controls.
- Reserve layout space for media and async content. Validate loading, empty, error, long text, localization, and reduced motion.
- For app-like web UI, distinguish persistent workspace regions from document content and define resizing behavior.

Rendered QA should include the project's real browser targets and at least one narrow and one wide viewport. Record exact sizes tested.
