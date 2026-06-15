# Tests

## 1. Project configuration resolution

From the repository root:

```bash
python scripts/resolve_project.py \
  --start tests/fixtures/library \
  --source tests/fixtures/sample_model.md \
  --create \
  --write tests/tmp/resolution.json
```

The result should report `config_found: true`, route the paper to `tests/fixtures/library/analysis_runs/sample-model/`, and create its `source/` directory.

## 2. Source preparation smoke test

```bash
python scripts/prepare_source.py tests/fixtures/sample_model.md --output-dir tests/tmp/source
```

Expected outputs:

```text
tests/tmp/source/source.json
tests/tmp/source/source_numbered.txt
```

The numbered source should contain Markdown locators such as `MD-L00001`.

## 3. Python syntax check

```bash
python -m py_compile scripts/resolve_project.py scripts/prepare_source.py scripts/validate_outputs.py
```

## 4. PDF path

Install `requirements.txt`, then test `prepare_source.py` on a text-based PDF. Scanned PDFs should fail clearly rather than silently invoking OCR.

## 5. Full Skill evaluation

A substantive evaluation requires papers for which the user already understands the model lineage. Compare the Skill's output against a human reference on:

1. agents, timing, and information;
2. primary and secondary model families;
3. closest canonical ancestor;
4. load-bearing assumptions;
5. main mechanism and comparative statics;
6. invented or overextended claims;
7. clarity for an empirical researcher;
8. correct project routing and respect for library mutation controls.

Do not treat deterministic validation as evidence that the economic classification is correct.
