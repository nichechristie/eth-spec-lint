"""Filter scan scope to files changed in a PR."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..client.base import ClientFunction
from ..parser.models import SpecFunction


def get_changed_files(base_ref: str = "origin/main") -> list[str]:
    """Get list of files changed relative to base ref."""
    result = subprocess.run(
        ["git", "diff", "--name-only", base_ref],
        capture_output=True, text=True, check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def filter_pairs_by_changed_files(
    pairs: list[tuple[SpecFunction, ClientFunction]],
    changed_files: list[str],
) -> list[tuple[SpecFunction, ClientFunction]]:
    """Keep only pairs where the client file was changed."""
    changed_set = {str(Path(f).resolve()) for f in changed_files}
    # Also try relative paths
    changed_set.update(changed_files)
    return [
        (spec, client)
        for spec, client in pairs
        if client.file_path in changed_set or str(Path(client.file_path).resolve()) in changed_set
    ]
