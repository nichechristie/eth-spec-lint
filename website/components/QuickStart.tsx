export default function QuickStart() {
  return (
    <section className="mx-auto max-w-3xl px-6 py-20">
      <h2 className="mb-3 text-center text-3xl font-bold text-white">
        Quick Start
      </h2>
      <p className="mb-8 text-center text-slate-500">
        Get up and running in seconds.
      </p>
      <div className="eth-glow rounded-2xl border border-white/5 bg-white/[0.02] p-1">
        <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/5">
          <div className="h-3 w-3 rounded-full bg-red-500/60" />
          <div className="h-3 w-3 rounded-full bg-yellow-500/60" />
          <div className="h-3 w-3 rounded-full bg-green-500/60" />
          <span className="ml-2 text-xs text-slate-600">terminal</span>
        </div>
        <pre className="overflow-x-auto p-6 text-sm leading-relaxed">
          <code>
            <span className="text-slate-500"># Install</span>{"\n"}
            <span className="text-purple-400">pip install</span> <span className="text-slate-300">eth-spec-lint</span>{"\n\n"}
            <span className="text-slate-500"># Run against a client repo</span>{"\n"}
            <span className="text-purple-400">eth-spec-lint</span> <span className="text-blue-400">\</span>{"\n"}
            {"  "}<span className="text-cyan-400">--spec</span> <span className="text-slate-300">EIP-1559</span> <span className="text-blue-400">\</span>{"\n"}
            {"  "}<span className="text-cyan-400">--client-path</span> <span className="text-slate-300">./go-ethereum</span> <span className="text-blue-400">\</span>{"\n"}
            {"  "}<span className="text-cyan-400">--output</span> <span className="text-slate-300">report.json</span>
          </code>
        </pre>
      </div>
    </section>
  );
}
