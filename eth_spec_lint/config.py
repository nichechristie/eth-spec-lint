"""YAML configuration loader."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SpecConfig:
    repo_path: str = "./consensus-specs"
    forks: list[str] = field(
        default_factory=lambda: ["phase0", "altair", "bellatrix", "capella", "deneb", "electra"]
    )


@dataclass
class ClientConfig:
    name: str = "lodestar"
    repo_path: str = "./lodestar"
    source_globs: list[str] = field(
        default_factory=lambda: [
            "packages/beacon-node/src/**/*.ts",
            "packages/state-transition/src/**/*.ts",
        ]
    )


@dataclass
class LLMConfig:
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    concurrency: int = 4
    temperature: float = 0.0


@dataclass
class CacheConfig:
    db_path: str = ".eth-spec-lint-cache.db"


@dataclass
class MappingConfig:
    overrides_file: str | None = None


@dataclass
class ReportConfig:
    formats: list[str] = field(default_factory=lambda: ["json", "markdown"])
    output_dir: str = "./reports"


@dataclass
class Config:
    spec: SpecConfig = field(default_factory=SpecConfig)
    client: ClientConfig = field(default_factory=ClientConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    mapping: MappingConfig = field(default_factory=MappingConfig)
    report: ReportConfig = field(default_factory=ReportConfig)


def _build_dataclass(cls: type, data: dict[str, Any] | None) -> Any:
    if data is None:
        return cls()
    valid = {k: v for k, v in data.items() if k in {f.name for f in cls.__dataclass_fields__.values()}}
    return cls(**valid)


def load_config(path: str | Path | None = None) -> Config:
    """Load config from YAML file, falling back to defaults."""
    raw: dict[str, Any] = {}
    if path and Path(path).exists():
        raw = yaml.safe_load(Path(path).read_text()) or {}
    elif path is None:
        for candidate in ("eth-spec-lint.yml", "eth-spec-lint.yaml", ".eth-spec-lint.yml"):
            if Path(candidate).exists():
                raw = yaml.safe_load(Path(candidate).read_text()) or {}
                break

    # Environment variable overrides
    if api_key := os.environ.get("ANTHROPIC_API_KEY"):
        raw.setdefault("llm", {})["provider"] = "anthropic"
    if api_key := os.environ.get("OPENAI_API_KEY"):
        raw.setdefault("llm", {}).setdefault("provider", "openai")

    return Config(
        spec=_build_dataclass(SpecConfig, raw.get("spec")),
        client=_build_dataclass(ClientConfig, raw.get("client")),
        llm=_build_dataclass(LLMConfig, raw.get("llm")),
        cache=_build_dataclass(CacheConfig, raw.get("cache")),
        mapping=_build_dataclass(MappingConfig, raw.get("mapping")),
        report=_build_dataclass(ReportConfig, raw.get("report")),
    )
