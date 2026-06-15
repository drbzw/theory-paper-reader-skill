#!/usr/bin/env python3
"""Deterministically validate Theory Paper Reader output files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FILES = [
    "01_theory_tutorial.md",
    "02_structural_reconstruction.md",
    "03_family_classification.md",
    "04_paper_model_card.md",
    "05_library_update_proposal.md",
]

REQUIRED = {
    "01_theory_tutorial.md": ["allocation", "first-best", "comparative statics", "empirical"],
    "02_structural_reconstruction.md": ["agents", "timing", "information structure", "constraints", "equilibrium"],
    "03_family_classification.md": ["primary model family", "closest canonical ancestor", "alternative", "classification confidence", "web verification"],
    "04_paper_model_card.md": ["paper identity", "main mechanism", "welfare implications", "empirical translation", "evidence log"],
    "05_library_update_proposal.md": ["recommendation", "rationale", "human review"],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    root = args.output_dir.resolve()
    results: list[tuple[str, str, str]] = []
    texts: dict[str, str] = {}

    for name in FILES:
        path = root / name
        if not path.exists():
            results.append((name, "FAIL", "Required file is missing."))
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        missing = [term for term in REQUIRED[name] if term not in text.lower()]
        if missing:
            results.append((name, "FAIL", "Missing expected terms: " + ", ".join(missing)))
        else:
            results.append((name, "PASS", "Required structure detected."))

    evidence_text = texts.get("02_structural_reconstruction.md", "") + texts.get("04_paper_model_card.md", "")
    for marker in ("PAPER-EXPLICIT", "MODEL-INFERRED", "CANONICAL-BACKGROUND"):
        results.append((marker, "PASS" if marker in evidence_text else "FAIL", "Evidence-status marker check."))

    locators = re.findall(r"(?:P\d{3}-L\d{3}|MD-L\d{5}|\bp\.?\s*\d+\b)", evidence_text, re.IGNORECASE)
    if len(locators) >= 10:
        results.append(("Source locators", "PASS", f"Detected {len(locators)} locators."))
    elif len(locators) >= 3:
        results.append(("Source locators", "WARNING", f"Only {len(locators)} locators detected."))
    else:
        results.append(("Source locators", "FAIL", f"Only {len(locators)} locators detected."))

    classification = texts.get("03_family_classification.md", "")
    web_ok = "VERIFIED" in classification or "WEB VERIFICATION PENDING" in classification
    results.append(("Web verification status", "PASS" if web_ok else "FAIL", "Verification status must be explicit."))

    confidence_ok = bool(re.search(r"classification confidence[^\n]*(high|moderate|low)", classification, re.IGNORECASE))
    results.append(("Classification confidence", "PASS" if confidence_ok else "FAIL", "Confidence must be High, Moderate, or Low."))

    overall = "FAIL" if any(status == "FAIL" for _, status, _ in results) else "WARNING" if any(status == "WARNING" for _, status, _ in results) else "PASS"

    lines = [
        "# Theory Paper Reader Audit Report",
        "",
        f"**Overall verdict: {overall}**",
        "",
        "This script checks schema and evidence hygiene; it does not certify the substantive economics.",
        "",
        "## 1. Results",
        "",
    ]
    for i, (name, status, detail) in enumerate(results, 1):
        lines.extend([f"### 1.{i} {name}", "", f"**{status}.** {detail}", ""])
    lines.extend([
        "## 2. Human review",
        "",
        "Substantive uncertainty about the model family must remain visible. Do not increase confidence merely to obtain a cleaner audit result.",
        "",
    ])

    report = args.report.resolve()
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")
    print(overall)
    if overall == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
