"""LLM comparison engine with SQLite caching."""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
from pathlib import Path

from ..client.base import ClientFunction
from ..config import Config
from ..parser.models import Finding, FindingCategory, Severity, SpecFunction
from .diff_types import CATEGORY_SEVERITY
from .prompts import render_compare_function

logger = logging.getLogger(__name__)

PROMPT_VERSION = "1"


class Cache:
    """SQLite-backed cache for LLM comparison results."""

    def __init__(self, db_path: str) -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)"
        )
        self._conn.commit()

    def get(self, key: str) -> str | None:
        row = self._conn.execute("SELECT value FROM cache WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

    def set(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)", (key, value)
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


def _cache_key(spec_source: str, client_source: str) -> str:
    payload = f"{PROMPT_VERSION}:{spec_source}:{client_source}"
    return hashlib.sha256(payload.encode()).hexdigest()


def _call_anthropic(prompt: str, config: Config) -> str:
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config.llm.model,
        max_tokens=2048,
        temperature=config.llm.temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def _call_openai(prompt: str, config: Config) -> str:
    import openai

    client = openai.OpenAI()
    resp = client.chat.completions.create(
        model=config.llm.model,
        temperature=config.llm.temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or ""


def _call_llm(prompt: str, config: Config) -> str:
    if config.llm.provider == "anthropic":
        return _call_anthropic(prompt, config)
    elif config.llm.provider == "openai":
        return _call_openai(prompt, config)
    else:
        raise ValueError(f"Unknown LLM provider: {config.llm.provider}")


def _parse_findings_json(raw: str, spec_fn: SpecFunction, client_fn: ClientFunction) -> list[Finding]:
    """Extract JSON array of findings from LLM response."""
    # Try to find JSON array in response
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        items = json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        logger.warning("Failed to parse LLM JSON response")
        return []

    findings: list[Finding] = []
    for item in items:
        try:
            cat = FindingCategory(item.get("category", "LOGIC_DIVERGENCE"))
        except ValueError:
            cat = FindingCategory.LOGIC_DIVERGENCE

        sev_str = item.get("severity")
        if sev_str:
            try:
                sev = Severity(sev_str.lower())
            except ValueError:
                sev = CATEGORY_SEVERITY.get(cat, Severity.WARNING)
        else:
            sev = CATEGORY_SEVERITY.get(cat, Severity.WARNING)

        findings.append(Finding(
            category=cat,
            severity=sev,
            summary=item.get("summary", ""),
            spec_function=spec_fn.name,
            client_function=client_fn.name,
            spec_file=spec_fn.file_path,
            client_file=client_fn.file_path,
            client_line=client_fn.line_number,
            detail=item.get("detail", ""),
            confidence=float(item.get("confidence", 0.5)),
        ))
    return findings


def compare_function_pair(
    spec_fn: SpecFunction,
    client_fn: ClientFunction,
    config: Config,
    cache: Cache | None = None,
) -> list[Finding]:
    """Compare a single spec function against its client implementation."""
    key = _cache_key(spec_fn.source, client_fn.source)

    if cache:
        cached = cache.get(key)
        if cached is not None:
            return _parse_findings_json(cached, spec_fn, client_fn)

    prompt = render_compare_function(
        spec_source=spec_fn.source,
        client_source=client_fn.source,
        spec_name=spec_fn.name,
        client_name=client_fn.name,
    )

    raw = _call_llm(prompt, config)

    if cache:
        cache.set(key, raw)

    return _parse_findings_json(raw, spec_fn, client_fn)


def compare_all(
    pairs: list[tuple[SpecFunction, ClientFunction]],
    config: Config,
) -> list[Finding]:
    """Compare all matched function pairs."""
    cache = Cache(config.cache.db_path)
    all_findings: list[Finding] = []
    try:
        for spec_fn, client_fn in pairs:
            logger.info("Comparing %s <-> %s", spec_fn.name, client_fn.name)
            findings = compare_function_pair(spec_fn, client_fn, config, cache)
            all_findings.extend(findings)
    finally:
        cache.close()
    return all_findings
