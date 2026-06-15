# Project Configuration Rules

## 1. Purpose

A project can define `.theory-paper-reader.yaml` at its root. Before deciding where to save outputs, the Skill must search from the current working directory upward for this file.

When the file exists, it controls the analysis workspace and the locations of the long-term paper and model libraries. When it does not exist, the fallback is `theory-paper-analysis/<paper-slug>/` under the current working directory.

## 2. Required resolution workflow

Before source preparation:

1. identify the Skill directory as the directory containing `SKILL.md`;
2. run `scripts/resolve_project.py` from that Skill directory;
3. search upward from the current working directory for `.theory-paper-reader.yaml`;
4. use the returned `analysis_dir` and `source_dir`;
5. do not silently choose another output directory.

## 3. Supported schema

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

Configured paths must be relative and remain inside the project root.

## 4. Library safety

The configuration identifies library destinations but does not authorize writes to them. During an ordinary paper-reading run, write only to the resolved analysis directory. Do not promote a paper card, update a family card, or modify indexes without a separate explicit user instruction.

## 5. Source retention

When `copy_original_source` is false, analyze the supplied source in place. Do not copy the original PDF, Markdown, or MinerU asset directory into the analysis output. Prepared line-addressable source files may remain local and may be excluded from Git.

## 6. Naming

The default paper slug is derived from the primary source filename. The user may request a slug such as `author-year-short-title`. Reuse the same slug for revisions unless the user deliberately requests a separate versioned run.
