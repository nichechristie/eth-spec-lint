const steps = [
  { label: "EIP Specs", sub: "Markdown", color: "purple" },
  { label: "Spec Parser", sub: "Extract reqs", color: "violet" },
  { label: "Client Scanner", sub: "Map code", color: "blue" },
  { label: "LLM Engine", sub: "Compare", color: "cyan" },
  { label: "Report", sub: "Findings", color: "emerald" },
];

const borderColors: Record<string, string> = {
  purple: "border-purple-500/30",
  violet: "border-violet-500/30",
  blue: "border-blue-500/30",
  cyan: "border-cyan-500/30",
  emerald: "border-emerald-500/30",
};

const dotColors: Record<string, string> = {
  purple: "bg-purple-500",
  violet: "bg-violet-500",
  blue: "bg-blue-500",
  cyan: "bg-cyan-500",
  emerald: "bg-emerald-500",
};

export default function Architecture() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <h2 className="mb-3 text-center text-3xl font-bold text-white">
        Pipeline
      </h2>
      <p className="mb-12 text-center text-slate-500">
        From specification to compliance report in one command.
      </p>
      <div className="flex flex-wrap items-center justify-center gap-3">
        {steps.map((s, i) => (
          <div key={s.label} className="flex items-center gap-3">
            <div className={`rounded-xl border ${borderColors[s.color]} bg-white/[0.02] px-6 py-4 text-center transition-all hover:bg-white/[0.05]`}>
              <div className="flex items-center justify-center gap-2">
                <div className={`h-2 w-2 rounded-full ${dotColors[s.color]}`} />
                <span className="font-semibold text-white">{s.label}</span>
              </div>
              <div className="mt-1 text-xs text-slate-500">{s.sub}</div>
            </div>
            {i < steps.length - 1 && (
              <svg className="h-5 w-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
              </svg>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
