# Typography character

Explain how classification, width, contrast, x-height, weight and rhythm support the thesis. Why medium rather than bold? Why more body leading? Why stronger numeric emphasis? A scale alone cannot answer these.

Define Font Family, CJK Font, Latin Font and Fallback; Display, Heading (H1/H2 as needed), Title, Body, Label, Caption and Numeric roles. Each role specifies size, weight, line height, tracking, case, alignment, line length, numeric behavior and multilingual behavior. Alias unused roles explicitly; do not inflate a watch UI into a desktop hierarchy.

Do not claim an exact reference font without evidence. Mark alternatives and exact new values Proposed; confirm availability, licensing and rendered fallback. Put parameters in tokens and typography specimen text/role selections in SPECIMENS.json. Show real Chinese for Chinese products and Chinese + Latin for bilingual products, including long text, numerals and punctuation. Numeric roles state tabular/proportional digits, decimal/unit alignment and emphasis.

The deterministic typography specimen must show actual scale and samples, not just labels such as H1 32px. Inspect wrapping, clipping and font substitution in the rendered output; SVG font-family is a request, not proof that the font is installed.
