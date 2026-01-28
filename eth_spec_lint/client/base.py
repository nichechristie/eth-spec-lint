"""Abstract base for client analyzers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ClientFunction:
    name: str
    source: str
    params: list[str]
    return_type: str | None = None
    file_path: str = ""
    line_number: int = 0
    exported: bool = False


class ClientAnalyzer(ABC):
    """Base class for language-specific client analyzers."""

    @abstractmethod
    def analyze(self, source_paths: list[str]) -> list[ClientFunction]:
        """Parse source files and return extracted functions."""
        ...
