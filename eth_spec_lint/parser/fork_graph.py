"""Fork inheritance resolution for Ethereum consensus specs."""

from __future__ import annotations

from .models import SpecConstant, SpecContainer, SpecFunction

# Canonical fork ordering
FORK_ORDER = ["phase0", "altair", "bellatrix", "capella", "deneb", "electra"]


def _fork_index(fork: str) -> int:
    try:
        return FORK_ORDER.index(fork)
    except ValueError:
        return len(FORK_ORDER)


def resolve_functions(functions: list[SpecFunction]) -> dict[str, SpecFunction]:
    """Resolve fork overrides: later forks replace earlier definitions.

    Returns a dict of function name -> latest SpecFunction.
    """
    resolved: dict[str, SpecFunction] = {}
    for fn in sorted(functions, key=lambda f: _fork_index(f.fork)):
        resolved[fn.name] = fn
    return resolved


def resolve_constants(constants: list[SpecConstant]) -> dict[str, SpecConstant]:
    resolved: dict[str, SpecConstant] = {}
    for c in sorted(constants, key=lambda c: _fork_index(c.fork)):
        resolved[c.name] = c
    return resolved


def resolve_containers(containers: list[SpecContainer]) -> dict[str, SpecContainer]:
    resolved: dict[str, SpecContainer] = {}
    for c in sorted(containers, key=lambda c: _fork_index(c.fork)):
        resolved[c.name] = c
    return resolved
