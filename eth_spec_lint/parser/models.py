"""Data models for parsed spec and comparison findings."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass
class SpecFunction:
    name: str
    source: str
    args: list[str]
    return_type: str | None = None
    fork: str = ""
    file_path: str = ""
    line_number: int = 0


@dataclass
class SpecConstant:
    name: str
    value: str
    fork: str = ""
    file_path: str = ""
    line_number: int = 0


@dataclass
class SpecContainer:
    """SSZ container / dataclass from the spec."""
    name: str
    fields: list[tuple[str, str]]  # (field_name, type_annotation)
    source: str = ""
    fork: str = ""
    file_path: str = ""
    line_number: int = 0


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    NOTE = "note"


class FindingCategory(str, Enum):
    LOGIC_DIVERGENCE = "LOGIC_DIVERGENCE"
    MISSING_CHECK = "MISSING_CHECK"
    CONSTANT_MISMATCH = "CONSTANT_MISMATCH"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    OFF_BY_ONE = "OFF_BY_ONE"
    OPTIMIZATION_SAFE = "OPTIMIZATION_SAFE"


@dataclass
class Finding:
    category: FindingCategory
    severity: Severity
    summary: str
    spec_function: str
    client_function: str
    spec_file: str = ""
    client_file: str = ""
    client_line: int = 0
    detail: str = ""
    confidence: float = 0.0
