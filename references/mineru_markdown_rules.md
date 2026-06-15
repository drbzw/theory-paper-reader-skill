# MinerU Markdown Handling Rules

## 1. Treat Markdown as a source representation, not as a summary

A MinerU conversion should preserve the paper's substantive text, equations, tables, and image references. Read the full Markdown rather than summarizing only headings or the introduction.

## 2. Keep the asset directory intact

MinerU commonly writes figures, equation images, and tables to sibling directories and links them with relative Markdown paths. The user should supply the Markdown together with those assets. Resolve relative paths from the Markdown file's own directory, not from the current working directory.

## 3. Evidence locations

Use normalized line locators from `scripts/prepare_source.py`, plus the nearest Markdown heading. When page markers survive conversion, use them as supplementary evidence only. Do not invent printed page numbers.

## 4. Equations and layout

Prefer native LaTeX or text equations in the Markdown. When an equation is represented only as an image, inspect the image if the runtime supports it. If not, mark the equation as unreadable and avoid reconstructing it from surrounding prose.

## 5. Tables and multi-column artifacts

MinerU output can occasionally reorder multi-column text or flatten tables. Check whether timing lists, assumptions, and proposition conditions appear internally coherent. When a passage seems scrambled, use a companion PDF if available or report the uncertainty.

## 6. Duplicate content

Conversions may repeat headers, footers, captions, or equations. Do not treat repeated text as independent evidence. Deduplicate conceptually while preserving the original locators.

## 7. Markdown versus PDF discrepancies

If both sources are available and materially disagree, report the discrepancy in the evidence log. Use the PDF to verify visual structure and printed pagination, but use the cleaner Markdown text for close reading when justified.
