"""Load Jinja2 prompt templates."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


def _get_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_PROMPTS_DIR)),
        keep_trailing_newline=True,
    )


def render_compare_function(spec_source: str, client_source: str, spec_name: str, client_name: str) -> str:
    env = _get_env()
    tmpl = env.get_template("compare_function.j2")
    return tmpl.render(
        spec_source=spec_source,
        client_source=client_source,
        spec_name=spec_name,
        client_name=client_name,
    )


def render_compare_constants(spec_constants: list[dict], client_constants: list[dict]) -> str:
    env = _get_env()
    tmpl = env.get_template("compare_constants.j2")
    return tmpl.render(spec_constants=spec_constants, client_constants=client_constants)


def render_compare_type(spec_type: str, client_type: str, spec_name: str, client_name: str) -> str:
    env = _get_env()
    tmpl = env.get_template("compare_type.j2")
    return tmpl.render(
        spec_type=spec_type,
        client_type=client_type,
        spec_name=spec_name,
        client_name=client_name,
    )
