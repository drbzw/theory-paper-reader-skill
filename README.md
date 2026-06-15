# Theory Paper Reader

A controlled Codex Skill for empirical researchers who need to **understand, classify, and archive formal economics and finance models**.

The Skill accepts either:

- a text-based PDF;
- a Markdown paper, especially accurate MinerU output; or
- both Markdown and PDF, using Markdown for text and PDF for page mapping, figures, and spot checks.

It produces:

1. a beginner-oriented tutorial written for an empirical researcher;
2. an evidence-grounded reconstruction of the model;
3. an open-set model-family classification verified with web research;
4. a Reference-style paper model card;
5. a proposal for how the paper should enter a long-term model library; and
6. a deterministic audit report.

The workflow is inspired by the model-matching and theory-lineage ideas in [pAI-Econ-claude](https://github.com/maxwell2732/pAI-Econ-claude), while adding an explicit **empirical translation layer**, support for MinerU Markdown, and stronger controls for evidence, uncertainty, and model-family classification.

## 1. Install in Codex

### 1.1 Recommended installation

In Codex, run the skill installer and ask it to install:

```text
https://github.com/drbzw/theory-paper-reader-skill
```

### 1.2 Manual installation

**Windows PowerShell**

```powershell
git clone https://github.com/drbzw/theory-paper-reader-skill "$HOME\.agents\skills\theory-paper-reader"
python -m pip install -r "$HOME\.agents\skills\theory-paper-reader\requirements.txt"
```

**macOS / Linux**

```bash
git clone https://github.com/drbzw/theory-paper-reader-skill ~/.agents/skills/theory-paper-reader
python -m pip install -r ~/.agents/skills/theory-paper-reader/requirements.txt
```

## 2. Use

The Skill is intentionally **explicit-invocation only**.

### 2.1 Analyze a MinerU Markdown paper

```text
$theory-paper-reader Analyze papers/my-paper.md
```

The Markdown file may retain relative links to MinerU-generated images and tables. Keep those asset folders beside the Markdown file.

### 2.2 Analyze a text-based PDF

```text
$theory-paper-reader Analyze papers/my-paper.pdf
```

The Skill never silently uses OCR. When PDF text extraction is poor, convert the paper with MinerU and supply the Markdown instead.

### 2.3 Supply both versions

```text
$theory-paper-reader Analyze papers/my-paper.md and use papers/my-paper.pdf for page mapping and figure verification.
```

### 2.4 Ask a focused question

```text
$theory-paper-reader Analyze papers/my-paper.md. I especially need to understand why this is screening rather than signaling.
```

By default, outputs are written to:

```text
theory-paper-analysis/<paper-slug>/
```

## 3. Evidence locators

For PDF input, the deterministic preparation script creates locations such as `P008-L014–P008-L033`.

For Markdown input, it creates locations such as `MD-L00482–MD-L00531`. The analysis should also name the nearest section heading. If MinerU preserved page markers, they are retained as supplementary evidence; the Skill does not invent page numbers when the Markdown has none.

The source-preparation command is:

```bash
python scripts/prepare_source.py path/to/paper.md --output-dir theory-paper-analysis/paper/source
```

The same command accepts `.pdf`.

## 4. Core controls

- The model taxonomy is **not closed**. Codex may identify a family absent from the seed map.
- GPT/model knowledge generates candidate families; it does not serve as final citation evidence.
- Final theory-lineage claims require external verification. Without web access, classification is marked provisional.
- Every paper-specific claim must be tied to a page, section, equation, proposition, theorem, appendix, or normalized Markdown line location.
- Outputs distinguish `PAPER-EXPLICIT`, `MODEL-INFERRED`, and `CANONICAL-BACKGROUND`.
- Missing assumptions, equilibria, propositions, and welfare results must not be invented.
- The Skill never modifies a canonical model library without a separate, explicit instruction.

## 5. Output style

The tutorial and interpretation use **numbered sections and subsections, coherent multi-sentence paragraphs, and selective bolding**. The Skill explicitly avoids one-sentence-per-paragraph writing and fragmented knowledge-base or checklist prose.

## 6. Repository structure

```text
SKILL.md
agents/openai.yaml
scripts/
references/
assets/
tests/
```

## 7. Status

Version 0.1.0 — initial controlled release. Evaluate the Skill on theory papers familiar to you before treating its classification judgments as production-grade.

## 8. License

MIT. See `LICENSE`.
