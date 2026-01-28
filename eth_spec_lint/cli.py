"""CLI entry point for eth-spec-lint."""

from __future__ import annotations

import logging
import sys

import click

from .config import load_config


@click.group()
@click.option("--config", "-c", "config_path", default=None, help="Path to config YAML file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def main(ctx: click.Context, config_path: str | None, verbose: bool) -> None:
    """eth-spec-lint: LLM-powered Ethereum spec drift detector."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_path)


@main.command()
@click.pass_context
def scan(ctx: click.Context) -> None:
    """Run full spec-vs-client comparison scan."""
    from .client.lodestar import LodestarAnalyzer
    from .client.mapping import build_mapping, load_overrides
    from .compare.engine import compare_all
    from .parser.fork_graph import resolve_functions
    from .parser.spec_parser import parse_spec_repo
    from .report.json_report import generate_json_report
    from .report.markdown_report import generate_markdown_report
    from .report.sarif_report import generate_sarif_report

    config = ctx.obj["config"]

    click.echo("Parsing spec files...")
    fns, consts, containers = parse_spec_repo(config.spec.repo_path, config.spec.forks)
    resolved = resolve_functions(fns)
    click.echo(f"  Found {len(resolved)} spec functions across {len(fns)} definitions")

    click.echo("Analyzing client code...")
    analyzer = LodestarAnalyzer()
    client_fns = analyzer.analyze(config.client.source_globs)
    click.echo(f"  Found {len(client_fns)} client functions")

    click.echo("Building mappings...")
    overrides = load_overrides(config.mapping.overrides_file)
    pairs = build_mapping(list(resolved.values()), client_fns, overrides)
    click.echo(f"  Matched {len(pairs)} function pairs")

    if not pairs:
        click.echo("No matched pairs found. Check your config paths and mappings.")
        sys.exit(0)

    click.echo("Running LLM comparison...")
    findings = compare_all(pairs, config)
    click.echo(f"  Found {len(findings)} findings")

    # Generate reports
    out = config.report.output_dir
    for fmt in config.report.formats:
        if fmt == "json":
            generate_json_report(findings, f"{out}/report.json")
        elif fmt == "markdown":
            generate_markdown_report(findings, f"{out}/report.md")
        elif fmt == "sarif":
            generate_sarif_report(findings, f"{out}/report.sarif")
    click.echo(f"Reports written to {out}/")


@main.command("check-pr")
@click.option("--base", default="origin/main", help="Base ref for diff")
@click.pass_context
def check_pr(ctx: click.Context, base: str) -> None:
    """Run comparison scoped to files changed in current PR."""
    from .ci.pr_filter import filter_pairs_by_changed_files, get_changed_files
    from .client.lodestar import LodestarAnalyzer
    from .client.mapping import build_mapping, load_overrides
    from .compare.engine import compare_all
    from .parser.fork_graph import resolve_functions
    from .parser.spec_parser import parse_spec_repo
    from .report.json_report import generate_json_report
    from .report.markdown_report import generate_markdown_report
    from .report.sarif_report import generate_sarif_report

    config = ctx.obj["config"]

    changed = get_changed_files(base)
    click.echo(f"Changed files: {len(changed)}")

    fns, consts, containers = parse_spec_repo(config.spec.repo_path, config.spec.forks)
    resolved = resolve_functions(fns)

    analyzer = LodestarAnalyzer()
    client_fns = analyzer.analyze(config.client.source_globs)

    overrides = load_overrides(config.mapping.overrides_file)
    pairs = build_mapping(list(resolved.values()), client_fns, overrides)
    pairs = filter_pairs_by_changed_files(pairs, changed)
    click.echo(f"Pairs affected by PR: {len(pairs)}")

    if not pairs:
        click.echo("No affected function pairs.")
        sys.exit(0)

    findings = compare_all(pairs, config)

    out = config.report.output_dir
    for fmt in config.report.formats:
        if fmt == "json":
            generate_json_report(findings, f"{out}/report.json")
        elif fmt == "markdown":
            generate_markdown_report(findings, f"{out}/report.md")
        elif fmt == "sarif":
            generate_sarif_report(findings, f"{out}/report.sarif")
    click.echo(f"Reports written to {out}/")


@main.command("list-mappings")
@click.pass_context
def list_mappings(ctx: click.Context) -> None:
    """Show matched spec<->client function pairs."""
    from .client.lodestar import LodestarAnalyzer
    from .client.mapping import build_mapping, load_overrides
    from .parser.fork_graph import resolve_functions
    from .parser.spec_parser import parse_spec_repo

    config = ctx.obj["config"]

    fns, _, _ = parse_spec_repo(config.spec.repo_path, config.spec.forks)
    resolved = resolve_functions(fns)

    analyzer = LodestarAnalyzer()
    client_fns = analyzer.analyze(config.client.source_globs)

    overrides = load_overrides(config.mapping.overrides_file)
    pairs = build_mapping(list(resolved.values()), client_fns, overrides)

    click.echo(f"{'Spec Function':<40} {'Client Function':<40} {'Client File'}")
    click.echo("-" * 120)
    for spec_fn, client_fn in pairs:
        click.echo(f"{spec_fn.name:<40} {client_fn.name:<40} {client_fn.file_path}")
