"""Markdown report output for PR comments."""

from __future__ import annotations

from pathlib import Path

from ..parser.models import Finding, Severity


def generate_markdown_report(findings: list[Finding], output_path: str | Path) -> None:
    lines = ["# eth-spec-lint Report", ""]

    errors = [f for f in findings if f.severity == Severity.ERROR]
    warnings = [f for f in findings if f.severity == Severity.WARNING]
    notes = [f for f in findings if f.severity == Severity.NOTE]

    lines.append(f"**{len(errors)} errors**, **{len(warnings)} warnings**, **{len(notes)} notes**")
    lines.append("")

    if not findings:
        lines.append("No findings detected.")
    else:
        for f in findings:
            icon = {"error": "X", "warning": "!", "note": "i"}[f.severity.value]
            lines.append(f"### [{icon}] {f.category.value}: {f.summary}")
            lines.append("")
            lines.append(f"- **Spec**: `{f.spec_function}` ({f.spec_file})")
            lines.append(f"- **Client**: `{f.client_function}` ({f.client_file}:{f.client_line})")
            if f.detail:
                lines.append(f"- **Detail**: {f.detail}")
            lines.append(f"- **Confidence**: {f.confidence:.0%}")
            lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines))
