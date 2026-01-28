"""SARIF 2.1.0 report for GitHub code scanning."""

from __future__ import annotations

import json
from pathlib import Path

from ..parser.models import Finding, Severity


def _severity_to_sarif(sev: Severity) -> str:
    return {"error": "error", "warning": "warning", "note": "note"}[sev.value]


def generate_sarif_report(findings: list[Finding], output_path: str | Path) -> None:
    results = []
    rules = {}

    for i, f in enumerate(findings):
        rule_id = f.category.value
        rules[rule_id] = {
            "id": rule_id,
            "shortDescription": {"text": f"Spec drift: {rule_id}"},
        }

        result = {
            "ruleId": rule_id,
            "level": _severity_to_sarif(f.severity),
            "message": {"text": f"{f.summary}\n\n{f.detail}" if f.detail else f.summary},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": f.client_file},
                        "region": {"startLine": max(f.client_line, 1)},
                    }
                }
            ],
        }
        results.append(result)

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "eth-spec-lint",
                        "version": "0.1.0",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(sarif, indent=2))
