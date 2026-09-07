# 静读 / Margin — Typography

Fictional demonstration; proposed design, not a sampled production system.

## Font Character and Families

J-03 chooses Song-style Chinese headings and Georgia-compatible Latin serifs to mark essays as reading content. Neutral PingFang/Arial labels remain direct. Medium heading weight leaves stroke detail legible; bold UI copy would flatten the distinction.

## Roles and Token Mapping

Display, h1, h2, title, body, label, caption and numeric map to typography.roles. Exact proposed values are only in TOKENS.json; specimens demonstrate the relationships using actual bilingual reading content.

## Line Length and Alignment

Left alignment anchors titles and body. Body measure follows a comfortable continuous reading column; compact screens wrap naturally. Larger leading supports Chinese paragraphs and mixed Latin words without forcing manual line breaks.

## Numeric Behavior

Numeric reading time uses the numeric role and stable unit association. Proportional article titles remain independent of metrics. Tabular numerals are requested for progress displays; browser font support requires verification.

## Multilingual Behavior

Chinese is primary; English title translations and labels are supported. Keep punctuation with the preceding phrase when possible. Long translated titles may grow vertically, never shrink beneath body hierarchy.

## Fallback Verification

Songti SC/Georgia and PingFang SC/Arial are requested with system fallbacks. The SVG displays requested families, not a license or installation guarantee. Inspect wrapping in the target browser and choose an explicit alternative if missing.
