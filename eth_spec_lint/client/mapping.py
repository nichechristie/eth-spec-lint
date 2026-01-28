"""Map spec function names (snake_case) to client function names (camelCase)."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from ..parser.models import SpecFunction
from .base import ClientFunction


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    s = re.sub(r"([A-Z])", r"_\1", name).lower()
    return s.lstrip("_")


def load_overrides(path: str | Path | None) -> dict[str, str]:
    """Load manual spec_name -> client_name overrides from YAML."""
    if not path or not Path(path).exists():
        return {}
    data = yaml.safe_load(Path(path).read_text()) or {}
    return {str(k): str(v) for k, v in data.items()}


def build_mapping(
    spec_functions: list[SpecFunction],
    client_functions: list[ClientFunction],
    overrides: dict[str, str] | None = None,
) -> list[tuple[SpecFunction, ClientFunction]]:
    """Match spec functions to client functions.

    Strategy:
    1. Use manual overrides first.
    2. Try snake_to_camel conversion.
    3. Try exact name match.
    """
    overrides = overrides or {}
    client_by_name: dict[str, ClientFunction] = {f.name: f for f in client_functions}

    pairs: list[tuple[SpecFunction, ClientFunction]] = []
    for spec_fn in spec_functions:
        # Check override
        if spec_fn.name in overrides:
            target = overrides[spec_fn.name]
            if target in client_by_name:
                pairs.append((spec_fn, client_by_name[target]))
                continue

        # Try camelCase conversion
        camel = snake_to_camel(spec_fn.name)
        if camel in client_by_name:
            pairs.append((spec_fn, client_by_name[camel]))
            continue

        # Try exact match
        if spec_fn.name in client_by_name:
            pairs.append((spec_fn, client_by_name[spec_fn.name]))

    return pairs
