# eth-spec-lint

LLM-powered Ethereum protocol security linter that compares consensus/execution specifications against client implementations, flagging inconsistencies and spec drift.

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Copy and edit config
cp config.example.yml eth-spec-lint.yml

# Full scan
eth-spec-lint scan

# PR-scoped scan (only changed files)
eth-spec-lint check-pr --base origin/main

# List matched spec<->client pairs
eth-spec-lint list-mappings
```

## Configuration

See `config.example.yml` for all options. Key settings:

- `spec.repo_path`: Path to `ethereum/consensus-specs` checkout
- `client.repo_path`: Path to client repo (e.g., `ChainSafe/lodestar`)
- `llm.provider`: `anthropic` or `openai`
- `report.formats`: `json`, `markdown`, `sarif`

Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in environment.

## GitHub Action

```yaml
- uses: nichechristie/eth-spec-lint@main
  with:
    config: eth-spec-lint.yml
    mode: pr
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Finding Categories

| Category | Severity | Description |
|----------|----------|-------------|
| LOGIC_DIVERGENCE | error | Implementation doesn't match spec logic |
| MISSING_CHECK | error | Validation present in spec but absent in client |
| CONSTANT_MISMATCH | error | Constant value differs |
| TYPE_MISMATCH | warning | Type/structure differs meaningfully |
| OFF_BY_ONE | error | Off-by-one in bounds/indexing |
| OPTIMIZATION_SAFE | note | Different but provably equivalent |

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
