# Tests

## 1. Source preparation smoke test

From the repository root:

```bash
python scripts/prepare_source.py tests/fixtures/sample_model.md --output-dir tests/tmp/source
```

Expected outputs:

```text
tests/tmp/source/source.json
tests/tmp/source/source_numbered.txt
```

The numbered source should contain Markdown locators such as `MD-L00001`.

## 2. Python syntax check

```bash
python -m py_compile scripts/prepare_source.py scripts/validate_outputs.py
```

## 3. PDF path

Install `requirements.txt`, then test `prepare_source.py` on a text-based PDF. Scanned PDFs should fail clearly rather than silently invoking OCR.

## 4. Full Skill evaluation

A substantive evaluation requires papers for which the user already understands the model lineage. Compare the Skill's output against a human reference on:

1. agents, timing, and information;
2. primary and secondary model families;
3. closest canonical ancestor;
4. load-bearing assumptions;
5. main mechanism and comparative statics;
6. invented or overextended claims;
7. clarity for an empirical researcher.

Do not treat the deterministic validator as evidence that the economic classification is correct.
