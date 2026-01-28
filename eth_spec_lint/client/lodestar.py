"""Lodestar (TypeScript) client analyzer using tree-sitter."""

from __future__ import annotations

import glob as globmod
from pathlib import Path

from .base import ClientAnalyzer, ClientFunction

try:
    import tree_sitter_typescript as ts_typescript
    from tree_sitter import Language, Parser

    _TS_AVAILABLE = True
except ImportError:
    _TS_AVAILABLE = False


def _build_parser() -> "Parser":
    if not _TS_AVAILABLE:
        raise RuntimeError("tree-sitter and tree-sitter-typescript are required for Lodestar analysis")
    parser = Parser(Language(ts_typescript.language_typescript()))
    return parser


def _extract_functions_from_tree(tree, source_bytes: bytes, file_path: str) -> list[ClientFunction]:
    """Walk tree-sitter AST and extract exported function declarations."""
    functions: list[ClientFunction] = []
    root = tree.root_node

    for node in _walk(root):
        # export function foo(...)
        if node.type == "export_statement":
            for child in node.children:
                if child.type == "function_declaration":
                    fn = _parse_function_node(child, source_bytes, file_path, exported=True)
                    if fn:
                        functions.append(fn)
        # Plain function declarations
        elif node.type == "function_declaration":
            # Check if parent is export_statement (already handled)
            if node.parent and node.parent.type == "export_statement":
                continue
            fn = _parse_function_node(node, source_bytes, file_path, exported=False)
            if fn:
                functions.append(fn)

    return functions


def _parse_function_node(node, source_bytes: bytes, file_path: str, exported: bool) -> ClientFunction | None:
    name = None
    params: list[str] = []
    return_type = None

    for child in node.children:
        if child.type == "identifier":
            name = child.text.decode()
        elif child.type == "formal_parameters":
            for param in child.children:
                if param.type in ("required_parameter", "optional_parameter"):
                    param_name = None
                    for pc in param.children:
                        if pc.type == "identifier":
                            param_name = pc.text.decode()
                            break
                    if param_name:
                        params.append(param_name)
        elif child.type == "type_annotation":
            return_type = child.text.decode().lstrip(": ").strip()

    if not name:
        return None

    return ClientFunction(
        name=name,
        source=source_bytes[node.start_byte:node.end_byte].decode(errors="replace"),
        params=params,
        return_type=return_type,
        file_path=file_path,
        line_number=node.start_point[0] + 1,
        exported=exported,
    )


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


class LodestarAnalyzer(ClientAnalyzer):
    def __init__(self) -> None:
        self._parser = _build_parser()

    def analyze(self, source_paths: list[str]) -> list[ClientFunction]:
        functions: list[ClientFunction] = []
        for pattern in source_paths:
            for fpath in sorted(globmod.glob(pattern, recursive=True)):
                source = Path(fpath).read_bytes()
                tree = self._parser.parse(source)
                functions.extend(_extract_functions_from_tree(tree, source, fpath))
        return functions
