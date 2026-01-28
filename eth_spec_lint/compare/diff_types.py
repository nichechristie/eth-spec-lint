"""Finding categories for spec-vs-implementation comparison."""

from __future__ import annotations

from ..parser.models import FindingCategory, Severity

# Default severity mapping per category
CATEGORY_SEVERITY: dict[FindingCategory, Severity] = {
    FindingCategory.LOGIC_DIVERGENCE: Severity.ERROR,
    FindingCategory.MISSING_CHECK: Severity.ERROR,
    FindingCategory.CONSTANT_MISMATCH: Severity.ERROR,
    FindingCategory.TYPE_MISMATCH: Severity.WARNING,
    FindingCategory.OFF_BY_ONE: Severity.ERROR,
    FindingCategory.OPTIMIZATION_SAFE: Severity.NOTE,
}
