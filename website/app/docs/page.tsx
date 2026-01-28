export default function DocsPage() {
  return (
    <article className="mx-auto max-w-3xl px-6 py-16 text-slate-300">
      <h1 className="mb-12 text-4xl font-bold text-white">Documentation</h1>

      <Section title="Whitepaper">
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-white">Abstract</h3>
          <p>
            Awesome ETH Linter is an LLM-powered security tool that automatically detects
            specification drift between Ethereum protocol specifications and client implementations.
            By leveraging large language models to perform semantic comparison of spec definitions
            against production code, it identifies logic divergences, missing validations, and
            constant mismatches that could lead to consensus failures or security vulnerabilities.
          </p>

          <h3 className="text-lg font-semibold text-white">Problem Statement</h3>
          <p>
            Ethereum clients must faithfully implement the consensus and execution specifications.
            Manual code review is time-consuming and error-prone, especially as specs evolve across
            hard forks (Phase0 → Altair → Bellatrix → Capella → Deneb → Electra). A single
            implementation bug can cause chain splits, fund losses, or network instability.
          </p>

          <h3 className="text-lg font-semibold text-white">Solution Architecture</h3>
          <p>
            The linter operates in three phases: (1) Parse spec files using Python AST to extract
            function signatures, constants, and container definitions across fork versions;
            (2) Analyze client code using Tree-sitter to identify corresponding implementations;
            (3) Use LLM comparison to semantically verify that client logic matches spec intent,
            detecting subtle divergences that pattern-matching tools would miss.
          </p>

          <h3 className="text-lg font-semibold text-white">Key Capabilities</h3>
          <ul className="list-inside list-disc space-y-1">
            <li>Fork-aware spec parsing with inheritance resolution</li>
            <li>Automatic spec↔client function mapping with manual overrides</li>
            <li>LLM-powered semantic comparison (Anthropic Claude / OpenAI)</li>
            <li>PR-scoped scanning for CI integration</li>
            <li>SARIF output for GitHub Security tab integration</li>
          </ul>
        </div>
      </Section>

      <Section title="Installation">
        <Code>{`# Clone the repository
git clone https://github.com/nichechristie/Awesome-ETH-Linter.git
cd Awesome-ETH-Linter

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"`}</Code>
      </Section>

      <Section title="Configuration">
        <p>
          Copy <code className="text-eth-blue">config.example.yml</code> to{" "}
          <code className="text-eth-blue">eth-spec-lint.yml</code> and customize:
        </p>
        <Code>{`spec:
  # Path to ethereum/consensus-specs checkout
  repo_path: ./consensus-specs
  # Forks to analyze (in order)
  forks:
    - phase0
    - altair
    - bellatrix
    - capella
    - deneb
    - electra

client:
  name: lodestar
  repo_path: ./lodestar
  source_globs:
    - "packages/beacon-node/src/**/*.ts"
    - "packages/state-transition/src/**/*.ts"

llm:
  provider: anthropic  # or "openai"
  model: claude-sonnet-4-20250514
  concurrency: 4
  temperature: 0.0

report:
  formats:
    - json
    - markdown
    - sarif
  output_dir: ./reports`}</Code>
        <p className="mt-4">
          Set your API key in the environment:
        </p>
        <Code>{`export ANTHROPIC_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"`}</Code>
      </Section>

      <Section title="CLI Commands">
        <Code>{`# Full spec-vs-client comparison scan
eth-spec-lint scan

# With custom config file
eth-spec-lint -c my-config.yml scan

# PR-scoped scan (only files changed since base)
eth-spec-lint check-pr --base origin/main

# List matched spec<->client function pairs
eth-spec-lint list-mappings

# Enable verbose logging
eth-spec-lint -v scan`}</Code>
      </Section>

      <Section title="GitHub Action">
        <p>
          Add to your workflow at{" "}
          <code className="text-eth-blue">.github/workflows/spec-lint.yml</code>:
        </p>
        <Code>{`name: Spec Lint
on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: nichechristie/Awesome-ETH-Linter@main
        with:
          config: eth-spec-lint.yml
          mode: pr
          anthropic_api_key: \${{ secrets.ANTHROPIC_API_KEY }}`}</Code>
      </Section>

      <Section title="Finding Categories">
        <ul className="list-inside list-disc space-y-2">
          <li>
            <strong className="text-white">LOGIC_DIVERGENCE</strong> (error) &mdash;
            Implementation doesn&apos;t match spec logic.
          </li>
          <li>
            <strong className="text-white">MISSING_CHECK</strong> (error) &mdash;
            Validation present in spec but absent in client.
          </li>
          <li>
            <strong className="text-white">CONSTANT_MISMATCH</strong> (error) &mdash;
            Constant value differs between spec and implementation.
          </li>
          <li>
            <strong className="text-white">TYPE_MISMATCH</strong> (warning) &mdash;
            Type or structure differs meaningfully.
          </li>
          <li>
            <strong className="text-white">OFF_BY_ONE</strong> (error) &mdash;
            Off-by-one error in bounds or indexing.
          </li>
          <li>
            <strong className="text-white">OPTIMIZATION_SAFE</strong> (note) &mdash;
            Different implementation but provably equivalent behavior.
          </li>
        </ul>
      </Section>

      <Section title="Development">
        <Code>{`# Clone and install dev dependencies
git clone https://github.com/nichechristie/Awesome-ETH-Linter.git
cd Awesome-ETH-Linter
pip install -e ".[dev]"

# Run tests
pytest

# Run a scan with example config
cp config.example.yml eth-spec-lint.yml
eth-spec-lint scan`}</Code>
      </Section>
    </article>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="mb-12">
      <h2 className="mb-4 text-2xl font-bold text-white">{title}</h2>
      <div className="space-y-4">{children}</div>
    </section>
  );
}

function Code({ children }: { children: string }) {
  return (
    <pre className="overflow-x-auto rounded-xl border border-eth-border bg-eth-card p-4 text-sm leading-relaxed">
      <code>{children}</code>
    </pre>
  );
}
