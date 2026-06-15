---
name: theory-paper-reader
description: Explicitly invoked workflow for reading a formal economics, finance, accounting, management, or organizational-economics paper from PDF or Markdown (including MinerU output); teaches the model to an empirical researcher, reconstructs the formal structure, performs open-set model-family classification with mandatory web verification, and writes an evidence-grounded model card. Do not use for ordinary paper summaries or empirical referee reports.
---

# Theory Paper Reader

## 1. Purpose

Use this Skill only when the user explicitly invokes `$theory-paper-reader` and supplies a theory paper as either:

1. a text-based PDF;
2. a Markdown file, especially a MinerU-converted paper;
3. both Markdown and PDF, in which case Markdown is the primary textual source and PDF is used for page mapping, figures, and spot checks.

The user is an empirical researcher and may not know the relevant model families in advance. Do **not** ask the user to classify the model. Your job is to teach the paper, discover plausible model families using your economics knowledge, verify the theory lineage online, and create an auditable paper-level model card.

## 2. Non-negotiable epistemic rules

Throughout all outputs, distinguish:

- **PAPER-EXPLICIT** — directly stated in the source and tied to a precise locator.
- **MODEL-INFERRED** — inferred from the formal structure but not named by the authors.
- **CANONICAL-BACKGROUND** — general knowledge about a model family, supported by the local references or externally verified sources.

Never present inferred or background material as if the paper stated it. Never invent missing assumptions, equilibrium concepts, propositions, welfare claims, or citations.

**GPT/model knowledge is used to generate candidate families, not as final citation evidence.** A final theory-lineage classification requires web verification. If web access is unavailable or verification is inconclusive, mark the classification:

`PROVISIONAL — WEB VERIFICATION PENDING`

## 3. Input preparation

### 3.1 Preferred Markdown workflow

When the user supplies a Markdown file, treat it as the primary source. MinerU Markdown often preserves equations, headings, tables, and image links better than generic PDF extraction.

Run:

```bash
python scripts/prepare_source.py path/to/paper.md --output-dir theory-paper-analysis/<paper-slug>/source
```

Use heading names and normalized line locators such as `MD-L0120–MD-L0146`. If the Markdown contains page markers, retain them as supplementary locators. Inspect linked local images or tables when they are necessary to understand the model and the runtime supports visual inspection. Do not infer missing image content from filenames.

### 3.2 PDF workflow

For a text-based PDF, run:

```bash
python scripts/prepare_source.py path/to/paper.pdf --output-dir theory-paper-analysis/<paper-slug>/source
```

Use page-and-line locators such as `P008-L014–P008-L033`. Do not silently OCR. If extraction is inadequate, stop and report `PDF TEXT EXTRACTION FAILED`, asking for a text-based PDF or a MinerU/other Markdown conversion.

### 3.3 When both Markdown and PDF are supplied

Use Markdown for textual reconstruction and PDF for page mapping, figures, diagrams, and equation-layout verification. Prepare both sources in separate subdirectories. When the two versions disagree materially, report the discrepancy rather than silently choosing one.

## 4. Output directory and files

Write all outputs to:

```text
theory-paper-analysis/<paper-slug>/
```

Create exactly these six files:

1. `01_theory_tutorial.md`
2. `02_structural_reconstruction.md`
3. `03_family_classification.md`
4. `04_paper_model_card.md`
5. `05_library_update_proposal.md`
6. `06_audit_report.md`

Use the corresponding templates in `assets/` and the rules in `references/`.

## 5. Stage 0 — Paper-type audit

Classify the source as one of:

1. pure theory paper;
2. theory plus empirical paper;
3. empirical paper with a formal model;
4. empirical paper with only verbal theory;
5. review, textbook, or non-model paper.

If there is no self-contained formal model, continue only as an **empirical-theory mapping**. Do not fabricate formal primitives, equilibrium concepts, proofs, or welfare results.

## 6. Stage 1 — Teach the paper to an empirical researcher

Create `01_theory_tutorial.md`. Write a structured essay with numbered sections and subsections. Use coherent multi-sentence paragraphs and selective bolding. Do not write one sentence per paragraph and do not produce a fragmented knowledge-base checklist.

Explain:

1. the paper's actual economic question;
2. the allocation problem;
3. the agents and their roles;
4. the sequence of events;
5. who knows what and when;
6. what each agent wants;
7. the central friction and trade-off;
8. the first-best benchmark;
9. why first-best fails;
10. the second-best or equilibrium response;
11. the genuinely non-trivial results;
12. comparative statics;
13. welfare and distributional implications;
14. what an empirical researcher should learn from the model.

For each load-bearing equation, explain what it means economically, why it is needed, and what would change if it were removed or altered. Do not merely restate notation.

## 7. Stage 2 — Formal structural reconstruction

Create `02_structural_reconstruction.md`. Reconstruct:

- agents;
- timing and commitment;
- information structure;
- preferences and payoff functions;
- actions and strategy spaces;
- state variables and outcomes;
- constraints;
- equilibrium or solution concept;
- first-best and second-best benchmarks;
- propositions and proof status;
- comparative statics;
- welfare results;
- load-bearing assumptions and boundary conditions.

Every paper-specific statement must include a source locator. For PDF use page or normalized page-line locations. For Markdown use heading plus line range; use page markers too when available. Mark every substantive entry `PAPER-EXPLICIT`, `MODEL-INFERRED`, or `NOT SPECIFIED`.

## 8. Stage 3 — Knowledge-driven open-set candidate generation

Before consulting the seed map, use your economics knowledge to generate three to five plausible model families. The candidate set is **not limited** to the local references.

Classify from structural fingerprints, not titles, abstracts, JEL codes, or isolated terms. Focus on:

- who moves first;
- hidden type versus hidden action;
- information arrival and observability;
- contractibility and commitment;
- allocation of ownership, authority, cash-flow rights, and control rights;
- choice variables and constraints;
- equilibrium concept;
- the friction that prevents first-best;
- the core rent, incentive, risk-sharing, information, or coordination trade-off.

For every candidate, state what fits, what does not fit, and whether it is a baseline family, a specific subfamily, or an extension family.

## 9. Stage 4 — Mandatory web verification of theory lineage

Use available web-search or browser tools. Search the publisher or official paper page, working-paper versions, author pages, DOI records, NBER/CEPR/SSRN or institutional repositories, seminar slides, and the specific canonical papers named in the model section.

Prefer primary and authoritative sources. Do not rely on search snippets. Open the relevant sources and compare structural inheritance: agents, timing, information, constraints, equilibrium concept, and core mechanism.

A bibliography citation alone does not establish ancestry. Distinguish papers that provide the model skeleton from papers that are merely related or cited for context.

Record verified and failed searches. If a citation or lineage claim cannot be verified, retain the uncertainty and exclude unsupported certainty.

## 10. Stage 5 — Comparative family adjudication

Create `03_family_classification.md`. It must include:

1. primary model family;
2. more specific subfamily;
3. secondary or extension family;
4. closest canonical ancestor;
5. all serious candidate families;
6. affirmative fit analysis;
7. rejection of the two strongest alternatives;
8. paper status: canonical model, major extension, minor extension, application/relabeling, hybrid, new-family candidate, or unresolved;
9. inherited elements;
10. changed elements;
11. new mechanism as a causal chain;
12. irreducibility condition;
13. classification confidence;
14. paper evidence;
15. external verification evidence;
16. remaining uncertainty.

When relevant, explicitly teach the boundary between commonly confused families: signaling versus screening; adverse selection versus moral hazard; moral hazard versus career concerns; ownership versus authority; incomplete contracts versus ordinary contracting; disclosure versus Bayesian persuasion; costly information acquisition versus rational inattention.

## 11. Stage 6 — Generate the paper model card

Create `04_paper_model_card.md`, inspired by canonical model-family cards but grounded in this specific paper. Required sections are defined in `references/output_schema.md` and `assets/paper_model_card_template.md`.

Keep paper-specific content separate from canonical background. The **Empirical Translation** section is mandatory and must connect:

`theoretical primitive → real-world counterpart → empirical proxy → shock → response horizon → observable equilibrium outcome → distinguishing comparative statics → competing models`.

Apply a timing audit: state the shortest plausible response time and the maximum reasonable lag for the proposed empirical implications. Do not assume an empirical proxy is identical to a latent theoretical object.

## 12. Stage 7 — Library update proposal

Create `05_library_update_proposal.md`. Recommend one of:

- add as canonical ancestor;
- add as major extension;
- add as minor extension;
- add only as an applied example;
- create a new-family candidate;
- send to human review;
- do not add.

Never modify an external or local canonical model library during this workflow. A library update requires a separate, explicit user instruction after review.

## 13. Stage 8 — Deterministic validation

After writing the first five files, run:

```bash
python scripts/validate_outputs.py theory-paper-analysis/<paper-slug>/ --report theory-paper-analysis/<paper-slug>/06_audit_report.md
```

Correct objective schema and formatting failures. Do not resolve substantive uncertainty by inventing confidence. The analysis is complete only when the audit distinguishes PASS, WARNING, and FAIL and reports any unresolved theoretical judgment.

## 14. Writing standard

All user-facing outputs must use:

- numbered section and subsection headings;
- coherent essay paragraphs, normally containing multiple related sentences;
- selective bolding for concepts and conclusions;
- short lists only when parallel items genuinely require them;
- plain economic intuition before technical notation.

Avoid:

- one-sentence-per-paragraph presentation;
- excessive bullets, cards, labels, and checklist prose;
- unsupported jargon;
- equations without economic interpretation;
- false precision about model classification;
- claims that a model proves a real-world causal effect.

## 15. Final response to the user

Summarize the primary family, closest ancestor, main mechanism, confidence, web-verification status, and output directory. State uncertainties plainly. Do not claim completion if the validator reports an unresolved FAIL.
