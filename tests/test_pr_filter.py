"""Tests for PR file filtering."""

from eth_spec_lint.ci.pr_filter import filter_pairs_by_changed_files
from eth_spec_lint.client.base import ClientFunction
from eth_spec_lint.parser.models import SpecFunction


def test_filter_keeps_changed():
    pairs = [
        (
            SpecFunction(name="a", source="", args=[], file_path="spec/a.md"),
            ClientFunction(name="a", source="", params=[], file_path="src/a.ts"),
        ),
        (
            SpecFunction(name="b", source="", args=[], file_path="spec/b.md"),
            ClientFunction(name="b", source="", params=[], file_path="src/b.ts"),
        ),
    ]
    filtered = filter_pairs_by_changed_files(pairs, ["src/a.ts"])
    assert len(filtered) == 1
    assert filtered[0][1].name == "a"


def test_filter_empty_changed():
    pairs = [
        (
            SpecFunction(name="a", source="", args=[], file_path="spec/a.md"),
            ClientFunction(name="a", source="", params=[], file_path="src/a.ts"),
        ),
    ]
    filtered = filter_pairs_by_changed_files(pairs, [])
    assert len(filtered) == 0
