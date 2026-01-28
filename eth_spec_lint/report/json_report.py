"""JSON report output."""

from __future__ import annotations

import json
from pathlib import Path

from ..parser.models import Finding


def generate_json_report(findings: list[Finding], output_path: str | Path) -> None:
    data = [
        {
            "category": f.category.value,
            "severity": f.severity.value,
            "summary": f.summary,
            "detail": f.detail,
            "spec_function": f.spec_function,
            "client_function": f.client_function,
            "spec_file": f.spec_file,
            "client_file": f.client_file,
            "client_line": f.client_line,
            "confidence": f.confidence,
        }
        for f in findings
    ]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(data, indent=2))
