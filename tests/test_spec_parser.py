"""Tests for spec parser."""

from pathlib import Path

from eth_spec_lint.parser.fork_graph import resolve_constants, resolve_functions
from eth_spec_lint.parser.spec_parser import extract_code_blocks, parse_spec_file

FIXTURE = Path(__file__).parent / "fixtures" / "sample_spec.md"


def test_extract_code_blocks():
    text = FIXTURE.read_text()
    blocks = extract_code_blocks(text)
    assert len(blocks) == 4  # constants, container, process_slot, get_active_validator_indices


def test_parse_spec_file_functions():
    fns, consts, containers = parse_spec_file(FIXTURE, "phase0")
    names = [f.name for f in fns]
    assert "process_slot" in names
    assert "get_active_validator_indices" in names


def test_parse_spec_file_constants():
    fns, consts, containers = parse_spec_file(FIXTURE, "phase0")
    const_names = [c.name for c in consts]
    assert "SLOTS_PER_EPOCH" in const_names
    assert "MAX_VALIDATORS_PER_COMMITTEE" in const_names
    assert "BASE_REWARD_FACTOR" in const_names


def test_parse_spec_file_containers():
    fns, consts, containers = parse_spec_file(FIXTURE, "phase0")
    assert any(c.name == "BeaconBlockHeader" for c in containers)
    bbh = next(c for c in containers if c.name == "BeaconBlockHeader")
    field_names = [f[0] for f in bbh.fields]
    assert "slot" in field_names
    assert "proposer_index" in field_names


def test_fork_resolution():
    from eth_spec_lint.parser.models import SpecFunction

    fns = [
        SpecFunction(name="foo", source="v1", args=[], fork="phase0"),
        SpecFunction(name="foo", source="v2", args=[], fork="altair"),
    ]
    resolved = resolve_functions(fns)
    assert resolved["foo"].source == "v2"
    assert resolved["foo"].fork == "altair"
