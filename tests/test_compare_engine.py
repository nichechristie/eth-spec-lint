"""Tests for comparison engine with mocked LLM."""

import json
from unittest.mock import patch

from eth_spec_lint.client.base import ClientFunction
from eth_spec_lint.compare.engine import Cache, _parse_findings_json, compare_function_pair
from eth_spec_lint.config import Config
from eth_spec_lint.parser.models import FindingCategory, Severity, SpecFunction

MOCK_LLM_RESPONSE = json.dumps([
    {
        "category": "MISSING_CHECK",
        "severity": "error",
        "summary": "Missing bounds check on validator index",
        "detail": "The spec checks index < len(validators) but the client does not.",
        "confidence": 0.9,
    }
])


def _make_spec_fn():
    return SpecFunction(
        name="process_slot",
        source="def process_slot(state): ...",
        args=["state"],
        fork="phase0",
        file_path="specs/phase0/beacon-chain.md",
        line_number=10,
    )


def _make_client_fn():
    return ClientFunction(
        name="processSlot",
        source="export function processSlot(state: BeaconState): void { ... }",
        params=["state"],
        file_path="packages/state-transition/src/slot.ts",
        line_number=5,
        exported=True,
    )


def test_parse_findings_json():
    spec_fn = _make_spec_fn()
    client_fn = _make_client_fn()
    findings = _parse_findings_json(MOCK_LLM_RESPONSE, spec_fn, client_fn)
    assert len(findings) == 1
    assert findings[0].category == FindingCategory.MISSING_CHECK
    assert findings[0].severity == Severity.ERROR
    assert findings[0].confidence == 0.9


def test_parse_findings_empty():
    findings = _parse_findings_json("[]", _make_spec_fn(), _make_client_fn())
    assert findings == []


def test_parse_findings_garbage():
    findings = _parse_findings_json("no json here", _make_spec_fn(), _make_client_fn())
    assert findings == []


def test_cache(tmp_path):
    db = str(tmp_path / "test.db")
    cache = Cache(db)
    assert cache.get("key1") is None
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    cache.close()


@patch("eth_spec_lint.compare.engine._call_llm")
def test_compare_function_pair(mock_llm, tmp_path):
    mock_llm.return_value = MOCK_LLM_RESPONSE
    config = Config()
    config.cache.db_path = str(tmp_path / "cache.db")

    findings = compare_function_pair(_make_spec_fn(), _make_client_fn(), config)
    assert len(findings) == 1
    assert findings[0].summary == "Missing bounds check on validator index"
    mock_llm.assert_called_once()


@patch("eth_spec_lint.compare.engine._call_llm")
def test_compare_uses_cache(mock_llm, tmp_path):
    mock_llm.return_value = MOCK_LLM_RESPONSE
    config = Config()
    config.cache.db_path = str(tmp_path / "cache.db")
    cache = Cache(config.cache.db_path)

    # First call hits LLM
    compare_function_pair(_make_spec_fn(), _make_client_fn(), config, cache)
    assert mock_llm.call_count == 1

    # Second call uses cache
    compare_function_pair(_make_spec_fn(), _make_client_fn(), config, cache)
    assert mock_llm.call_count == 1

    cache.close()
