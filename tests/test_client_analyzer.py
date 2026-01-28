"""Tests for client mapping (tree-sitter tests skipped if not installed)."""

import pytest

from eth_spec_lint.client.mapping import build_mapping, camel_to_snake, snake_to_camel
from eth_spec_lint.parser.models import SpecFunction


def test_snake_to_camel():
    assert snake_to_camel("process_slot") == "processSlot"
    assert snake_to_camel("get_active_validator_indices") == "getActiveValidatorIndices"
    assert snake_to_camel("foo") == "foo"


def test_camel_to_snake():
    assert camel_to_snake("processSlot") == "process_slot"
    assert camel_to_snake("getActiveValidatorIndices") == "get_active_validator_indices"


def test_build_mapping_auto():
    from eth_spec_lint.client.base import ClientFunction

    spec_fns = [
        SpecFunction(name="process_slot", source="...", args=["state"]),
        SpecFunction(name="unmapped_fn", source="...", args=[]),
    ]
    client_fns = [
        ClientFunction(name="processSlot", source="...", params=["state"]),
        ClientFunction(name="otherFn", source="...", params=[]),
    ]
    pairs = build_mapping(spec_fns, client_fns)
    assert len(pairs) == 1
    assert pairs[0][0].name == "process_slot"
    assert pairs[0][1].name == "processSlot"


def test_build_mapping_override():
    from eth_spec_lint.client.base import ClientFunction

    spec_fns = [SpecFunction(name="process_slot", source="...", args=["state"])]
    client_fns = [ClientFunction(name="customProcessSlot", source="...", params=["state"])]
    pairs = build_mapping(spec_fns, client_fns, overrides={"process_slot": "customProcessSlot"})
    assert len(pairs) == 1
    assert pairs[0][1].name == "customProcessSlot"


try:
    import tree_sitter
    import tree_sitter_typescript
    _HAS_TREESITTER = True
except ImportError:
    _HAS_TREESITTER = False


@pytest.mark.skipif(not _HAS_TREESITTER, reason="tree-sitter not installed")
def test_lodestar_analyzer():
    from pathlib import Path

    from eth_spec_lint.client.lodestar import LodestarAnalyzer

    fixture = str(Path(__file__).parent / "fixtures" / "sample_client.ts")
    analyzer = LodestarAnalyzer()
    fns = analyzer.analyze([fixture])
    names = [f.name for f in fns]
    assert "processSlot" in names
    assert "getActiveValidatorIndices" in names
    # Check exported flag
    exported = {f.name: f.exported for f in fns}
    assert exported.get("processSlot") is True
    assert exported.get("internalHelper") is False
