---
name: theory-paper-reader
description: Explicitly invoked workflow for reading a formal economics, finance, accounting, management, or organizational-economics paper from PDF or Markdown (including MinerU output); teaches the model to an empirical researcher, reconstructs the formal structure, performs open-set model-family classification with mandatory web verification, and writes an evidence-grounded model card into a configurable theory-library workspace. Do not use for ordinary paper summaries or empirical referee reports.
---

# Theory Paper Reader

## 1. Purpose

Use this Skill only when the user explicitly invokes `$theory-paper-reader` and supplies a theory paper as either:

1. a text-based PDF;
2. a Markdown file, especially a MinerU-converted paper;
3. both Markdown and PDF, in which case Markdown is the primary textual source and PDF is used for page mapping, figures, and spot checks.

The user is an empirical researcher and may not know the relevant model families in advance. Do **not** ask the user to classify the model. Teach the paper, discover plausible model families using economics knowledge, verify the theory lineage online, and create an auditable paper-level model card.

## 2. Non-negotiable epistemic rules

Throughout all outputs, distinguish:

- **PAPER-EXPLICIT** — directly stated in the source and tied to a precise locator.
- **MODEL-INFERRED** — inferred from the formal structure but not named by the authors.
- **CANONICAL-BACKGROUND** — general knowledge about a model family, supported by local references or externally verified sources.

Never present inferred or background material as if the paper stated it. Never invent missing assumptions, equilibrium concepts, propositions, welfare claims, or citations.

**GPT/model knowledge is used to generate candidate families, not as final citation evidence.** A final theory-lineage classification requires web verification. If web access is unavailable or verification is inconclusive, mark the classification:

`PROVISIONAL — WEB VERIFICATION PENDING`

## 3. Resolve the project before reading the paper

First identify `<skill-root>` as the installed directory containing this `SKILL.md`. Read and apply `references/project_config.md`.

From the user's current working directory, run:

```bash
python <skill-root>/scripts/resolve_project.py --start . --source path/to/primary-source.md --create
```

Use the JSON returned by the script as the authoritative routing decision. In particular, retain:

- `project_root`
- `paper_slug`
- `analysis_dir`
- `source_dir`
- the configured `paper_library`, `model_library`, `update_queue`, and `indexes` paths
- the input and library policies

When `.theory-paper-reader.yaml` is found, save the run under its configured `analysis_root`. When no configuration is found, use the resolver's fallback `theory-paper-analysis/<paper-slug>/` under the current working directory.

Do not write analysis outputs into the installed Skill directory. Do not silently choose a different destination. At the start of the final response, report the resolved analysis directory.

## 4. Input preparation

### 4.1 Preferred Markdown workflow

When the user supplies a Markdown file, treat it as the primary source. MinerU Markdown often preserves equations, headings, tables, and image links better than generic PDF extraction.

Before analyzing any Markdown input, read and apply both:

- `references/mineru_markdown_rules.md`
- `references/evidence_rules.md`

These files are mandatory for Markdown-mode analysis. They govern relative assets, equations and tables, evidence locators, conversion artifacts, and Markdown–PDF discrepancies.

Run:

```bash
python <skill-root>/scripts/prepare_source.py path/to/paper.md --output-dir <source_dir>
```

Use heading names and normalized line locators such as `MD-L0120–MD-L0146`. If the Markdown contains page markers, retain them as supplementary locators. Inspect linked local images or tables when necessary and supported. Do not infer missing image content from filenames.

### 4.2 PDF workflow

For a text-based PDF, run:

```bash
python <skill-root>/scripts/prepare_source.py path/to/paper.pdf --output-dir <source_dir>
```

Use page-and-line locators such as `P008-L014–P008-L033`. Do not silently OCR. If extraction is inadequate, stop and report `PDF TEXT EXTRACTION FAILED`, asking for a text-based PDF or a MinerU/other Markdown conversion.

### 4.3 When both Markdown and PDF are supplied

Use Markdown for textual reconstruction and PDF for page mapping, figures, diagrams, and equation-layout verification. Prepare Markdown under `<source_dir>/markdown` and PDF under `<source_dir>/pdf`. When the versions disagree materially, report the discrepancy rather than silently choosing one.

Respect `input_policy.copy_original_source`. When it is false, analyze source files in place and do not copy the original PDF, Markdown, or MinerU asset folder into the analysis directory.

## 5. Output directory and files

Write the six user-facing outputs directly into the resolved `<analysis_dir>`:

1. `01_theory_tutorial.md`
2. `02_structural_reconstruction.md`
3. `03_family_classification.md`
4. `04_paper_model_card.md`
5. `05_library_update_proposal.md`
6. `06_audit_report.md`

The prepared source files belong under `<analysis_dir>/source/`. Use the corresponding templates in `assets/` and the rules in `references/`.

An ordinary paper-reading run may write only inside `<analysis_dir>`. The configured `paper_library`, `model_library`, `update_queue`, and `indexes` locations are destinations for later curation, not authorization to modify them.

## 6. Stage 0 — Paper-type audit

Classify the source as one of:

1. pure theory paper;
2. theory plus empirical paper;
3. empirical paper with a formal model;
4. empirical paper with only verbal theory;
5. review, textbook, or non-model paper.

If there is no self-contained formal model, continue only as an **empirical-theory mapping**. Do not fabricate formal primitives, equilibrium concepts, proofs, or welfare results.

## 7. Stage 1 — Teach the paper to an empirical researcher

Create `01_theory_tutorial.md`. Write a structured essay with numbered sections and subsections, coherent multi-sentence paragraphs, and selective bolding. Do not produce one-sentence-per-paragraph or fragmented knowledge-base prose.

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

## 8. Stage 2 — Formal structural reconstruction

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

Every paper-specific statement must include a source locator. For PDF use page or normalized page-line locations. For Markdown use heading plus line range and page markers when available. Mark every substantive entry `PAPER-EXPLICIT`, `MODEL-INFERRED`, or `NOT SPECIFIED`.

## 9. Stage 3 — Knowledge-driven open-set candidate generation

Before consulting `references/model_family_seed_map.md`, use economics knowledge to generate three to five plausible model families. The candidate set is **not limited** to local references.

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

## 10. Stage 4 — Mandatory web verification of theory lineage

Read and apply `references/web_verification_rules.md`. Use available web-search or browser tools. Search the publisher or official paper page, working-paper versions, author pages, DOI records, recognized repositories, seminar slides, and the canonical papers named in the model section.

Prefer primary and authoritative sources. Do not rely on search snippets. Open relevant sources and compare structural inheritance: agents, timing, information, constraints, equilibrium concept, and core mechanism.

A bibliography citation alone does not establish ancestry. Record verified and failed searches. If a lineage claim cannot be verified, preserve uncertainty.

## 11. Stage 5 — Comparative family adjudication

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

When relevant, teach the boundary between signaling and screening; adverse selection and moral hazard; moral hazard and career concerns; ownership and authority; incomplete contracts and ordinary contracting; disclosure and Bayesian persuasion; costly information acquisition and rational inattention.

## 12. Stage 6 — Generate the paper model card

Create `04_paper_model_card.md`, grounded in the specific paper. Follow `references/output_schema.md` and `assets/paper_model_card_template.md`.

Keep paper-specific content separate from canonical background. The **Empirical Translation** section is mandatory and must connect:

`theoretical primitive → real-world counterpart → empirical proxy → shock → response horizon → observable equilibrium outcome → distinguishing comparative statics → competing models`.

Apply a timing audit: state the shortest plausible response time and the maximum reasonable lag. Do not assume an empirical proxy is identical to a latent theoretical object.

## 13. Stage 7 — Library update proposal

Create `05_library_update_proposal.md`. Recommend one of:

- add as canonical ancestor;
- add as major extension;
- add as minor extension;
- add only as an applied example;
- create a new-family candidate;
- send to human review;
- do not add.

Name the configured paper-library and model-library destinations in the proposal. Never modify them during this run. Promotion or family-card revision requires a separate explicit user instruction after review, regardless of the recommendation.

## 14. Stage 8 — Deterministic validation

After writing the first five files, run:

```bash
python <skill-root>/scripts/validate_outputs.py <analysis_dir> --report <analysis_dir>/06_audit_report.md
```

Correct objective schema and formatting failures. Do not resolve substantive uncertainty by inventing confidence. The analysis is complete only when the audit distinguishes PASS, WARNING, and FAIL.

## 15. Writing standard

All user-facing outputs must use:

- numbered section and subsection headings;
- coherent essay paragraphs, normally containing multiple related sentences;
- selective bolding for concepts and conclusions;
- short lists only when parallel items genuinely require them;
- plain economic intuition before technical notation.

Avoid one-sentence-per-paragraph presentation, excessive bullets and cards, unsupported jargon, equations without interpretation, false precision about classification, and claims that a model proves a real-world causal effect.

## 16. Final response to the user

Summarize the resolved analysis directory, primary family, closest ancestor, main mechanism, confidence, and web-verification status. State uncertainties plainly. Do not claim completion if the validator reports an unresolved FAIL.
