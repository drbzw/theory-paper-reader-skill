# Theory Paper Reader

A controlled Codex Skill for empirical researchers who need to **understand, classify, and archive formal economics and finance models**.

This Skill takes one theory paper PDF and produces:

1. a beginner-oriented tutorial written for an empirical researcher;
2. a page-grounded reconstruction of the model;
3. an open-set model-family classification verified with web research;
4. a Reference-style paper model card;
5. a proposal for how the paper should enter a long-term model library; and
6. a deterministic audit report.

The workflow is inspired by the model-matching and theory-lineage ideas in [pAI-Econ-claude](https://github.com/maxwell2732/pAI-Econ-claude), while adding an explicit **empirical translation layer** and stronger controls for evidence, uncertainty, and model-family classification.

## Install in Codex

### Recommended: ask the built-in installer

In Codex, run `$skill-installer`, then say:

```text
Install the skill from https://github.com/drbzw/theory-paper-reader-skill
```

Restart Codex only if the newly installed skill does not appear.

### Manual installation

**Windows PowerShell**

```powershell
git clone https://github.com/drbzw/theory-paper-reader-skill "$HOME\.agents\skills\theory-paper-reader"
```

**macOS / Linux**

```bash
git clone https://github.com/drbzw/theory-paper-reader-skill ~/.agents/skills/theory-paper-reader
```

Install the one Python dependency used by the deterministic PDF extractor:

```bash
python -m pip install -r ~/.agents/skills/theory-paper-reader/requirements.txt
```

On Windows, use the corresponding cloned path.

## Use

The Skill is intentionally **explicit-invocation only**. In Codex, type:

```text
$theory-paper-reader Analyze papers/my-paper.pdf
```

You can also add a specific question:

```text
$theory-paper-reader Analyze papers/my-paper.pdf. I especially need to understand why this is screening rather than signaling.
```

By default, the Skill writes six files to:

```text
theory-paper-analysis/<paper-slug>/
```

## Core controls

- The local model taxonomy is **not closed**. Codex may identify a family absent from the seed map.
- GPT/model knowledge generates candidate families; it does not serve as final citation evidence.
- Final theory-lineage claims require external verification. Without web access, classification is marked provisional.
- Every paper-specific claim must be tied to a page, section, equation, proposition, theorem, or appendix location.
- The outputs distinguish `PAPER-EXPLICIT`, `MODEL-INFERRED`, and `CANONICAL-BACKGROUND`.
- Missing assumptions, equilibria, propositions, and welfare results must not be invented.
- The Skill never modifies a canonical model library without a separate, explicit user instruction.

## Output style

The tutorial and interpretation use **numbered sections and subsections, coherent multi-sentence paragraphs, and selective bolding**. The Skill explicitly avoids one-sentence-per-paragraph writing and fragmented knowledge-base/checklist prose.

## Repository structure

```text
SKILL.md
agents/openai.yaml
scripts/
references/
assets/
tests/
```

## Status

Version 0.1.0 — initial controlled release. The Skill should be evaluated on theory papers familiar to the user before its classification judgments are treated as production-grade.

## License

MIT. See `LICENSE`.
