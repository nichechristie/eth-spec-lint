"""Extract Python functions, constants, and containers from consensus-spec markdown files."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from .models import SpecConstant, SpecContainer, SpecFunction

# Match fenced Python code blocks in spec markdown
_CODE_BLOCK_RE = re.compile(
    r"```python\s*\n(.*?)```", re.DOTALL
)


def extract_code_blocks(markdown: str) -> list[str]:
    """Return all fenced Python code blocks from a markdown string."""
    return _CODE_BLOCK_RE.findall(markdown)


def _parse_function(node: ast.FunctionDef, source_lines: list[str], fork: str, file_path: str) -> SpecFunction:
    src = ast.get_source_segment("\n".join(source_lines), node) or ""
    args = [a.arg for a in node.args.args]
    ret = None
    if node.returns:
        ret = ast.unparse(node.returns)
    return SpecFunction(
        name=node.name,
        source=src,
        args=args,
        return_type=ret,
        fork=fork,
        file_path=file_path,
        line_number=node.lineno,
    )


def _parse_container(node: ast.ClassDef, source_lines: list[str], fork: str, file_path: str) -> SpecContainer | None:
    """Parse a class that looks like an SSZ container (class with annotated fields)."""
    fields: list[tuple[str, str]] = []
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            fields.append((item.target.id, ast.unparse(item.annotation)))
    if not fields:
        return None
    return SpecContainer(
        name=node.name,
        fields=fields,
        source=ast.get_source_segment("\n".join(source_lines), node) or "",
        fork=fork,
        file_path=file_path,
        line_number=node.lineno,
    )


def _parse_constant(node: ast.Assign, source_lines: list[str], fork: str, file_path: str) -> list[SpecConstant]:
    constants = []
    for target in node.targets:
        if isinstance(target, ast.Name) and target.id.isupper():
            constants.append(SpecConstant(
                name=target.id,
                value=ast.unparse(node.value),
                fork=fork,
                file_path=file_path,
                line_number=node.lineno,
            ))
    return constants


def parse_spec_file(
    file_path: str | Path,
    fork: str,
) -> tuple[list[SpecFunction], list[SpecConstant], list[SpecContainer]]:
    """Parse a single spec markdown file, returning extracted functions, constants, and containers."""
    text = Path(file_path).read_text()
    blocks = extract_code_blocks(text)

    functions: list[SpecFunction] = []
    constants: list[SpecConstant] = []
    containers: list[SpecContainer] = []

    for block in blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue

        lines = block.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(_parse_function(node, lines, fork, str(file_path)))
            elif isinstance(node, ast.ClassDef):
                c = _parse_container(node, lines, fork, str(file_path))
                if c:
                    containers.append(c)
            elif isinstance(node, ast.Assign):
                constants.extend(_parse_constant(node, lines, fork, str(file_path)))

    return functions, constants, containers


def parse_spec_repo(
    repo_path: str | Path,
    forks: list[str],
) -> tuple[list[SpecFunction], list[SpecConstant], list[SpecContainer]]:
    """Parse all spec files across forks. Later forks override earlier ones."""
    all_fns: list[SpecFunction] = []
    all_consts: list[SpecConstant] = []
    all_containers: list[SpecContainer] = []

    repo = Path(repo_path)
    for fork in forks:
        specs_dir = repo / "specs" / fork
        if not specs_dir.exists():
            # Try alternate layout: specs/_features/fork or presets/
            specs_dir = repo / "specs" / "_features" / fork
        if not specs_dir.exists():
            continue
        for md_file in sorted(specs_dir.rglob("*.md")):
            fns, consts, ctrs = parse_spec_file(md_file, fork)
            all_fns.extend(fns)
            all_consts.extend(consts)
            all_containers.extend(ctrs)

    return all_fns, all_consts, all_containers
