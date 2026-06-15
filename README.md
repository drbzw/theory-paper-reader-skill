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
4. a paper-level model card;
5. a proposal for how the paper should enter a long-term model library; and
6. a deterministic audit report.

The workflow is inspired by the model-matching and theory-lineage ideas in [pAI-Econ-claude](https://github.com/maxwell2732/pAI-Econ-claude), while adding an explicit **empirical translation layer**, support for MinerU Markdown, project-aware output routing, and stronger controls for evidence and uncertainty.

## 1. Install in Codex

### 1.1 Recommended installation

In Codex, run the Skill installer and ask it to install:

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

## 2. Recommended persistent-library setup

Use this public repository only as the reusable tool. Keep paper analyses and the evolving theory library in a separate project repository.

A project can define `.theory-paper-reader.yaml` at its root:

```yaml
version: 1
library_name: My Theory Model Library

paths:
  analysis_root: analysis_runs
  paper_library: paper_library
  model_library: model_library
  update_queue: update_queue
  indexes: indexes
  input_root: inputs

input_policy:
  copy_original_source: false
  retain_source_manifest: true

library_policy:
  auto_promote_paper_card: false
  auto_modify_model_library: false
  require_human_approval: true
```

Before every run, `scripts/resolve_project.py` searches upward from the current working directory for this file. When found, a paper is saved under:

```text
analysis_runs/<paper-slug>/
```

When no project configuration exists, the fallback remains:

```text
theory-paper-analysis/<paper-slug>/
```

The Skill never writes its paper outputs into the installed Skill directory.

## 3. Use

The Skill is intentionally **explicit-invocation only**. Open the repository in which you want the analysis saved, then invoke it.

### 3.1 Analyze a MinerU Markdown paper

```text
$theory-paper-reader Analyze inputs/inbox/my-paper/paper.md
```

Keep MinerU-generated image and table directories beside the Markdown file so relative links continue to work.

### 3.2 Analyze a text-based PDF

```text
$theory-paper-reader Analyze inputs/inbox/my-paper/paper.pdf
```

The Skill never silently uses OCR. When extraction is poor, convert the paper with MinerU and supply Markdown instead.

### 3.3 Supply both versions

```text
$theory-paper-reader Analyze inputs/inbox/my-paper/paper.md and use inputs/inbox/my-paper/paper.pdf for page mapping and figure verification.
```

### 3.4 Ask a focused question

```text
$theory-paper-reader Analyze inputs/inbox/my-paper/paper.md. Explain especially why this is screening rather than signaling.
```

## 4. How routing works

The resolver returns the project root, deterministic paper slug, analysis directory, source-preparation directory, and configured long-term library paths.

```bash
python scripts/resolve_project.py --start . --source path/to/paper.md --create
```

The six analysis files are written to the resolved paper folder. Prepared source text is stored under its `source/` subdirectory. The configured `paper_library/`, `model_library/`, `update_queue/`, and `indexes/` locations are not modified during an ordinary reading run.

## 5. Evidence locators

For PDF input, `prepare_source.py` creates locations such as `P008-L014–P008-L033`.

For Markdown input, it creates locations such as `MD-L00482–MD-L00531` and records the nearest heading. If MinerU preserved page markers, they are retained as supplementary evidence; the Skill does not invent page numbers.

## 6. Core controls

- The model taxonomy is **not closed**. Codex may identify a family absent from the seed map.
- GPT/model knowledge generates candidate families; it does not serve as final citation evidence.
- Final theory-lineage claims require external verification. Without web access, classification is marked provisional.
- Every paper-specific claim must be tied to a source locator.
- Outputs distinguish `PAPER-EXPLICIT`, `MODEL-INFERRED`, and `CANONICAL-BACKGROUND`.
- Missing assumptions, equilibria, propositions, and welfare results must not be invented.
- Paper cards and family cards are never promoted or modified without separate human approval.

## 7. Output style

The tutorial and interpretation use **numbered sections and subsections, coherent multi-sentence paragraphs, and selective bolding**. The Skill avoids one-sentence-per-paragraph and fragmented checklist prose.

## 8. Repository structure

```text
SKILL.md
agents/openai.yaml
scripts/
references/
assets/
examples/
tests/
```

## 9. Status

Version 0.2.0 — project-aware release. Evaluate the Skill on papers whose model lineage is already familiar before treating its classification judgments as production-grade.

## 10. License

MIT. See `LICENSE`.
