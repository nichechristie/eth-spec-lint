const features = [
  {
    icon: (
      <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Zm3.75 11.625a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
      </svg>
    ),
    title: "Spec Parsing",
    description:
      "Extracts structured requirements from EIP markdown — MUSTs, SHOULDs, and SHALLs identified automatically.",
    color: "purple",
  },
  {
    icon: (
      <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
      </svg>
    ),
    title: "Client Analysis",
    description:
      "Scans Ethereum client source code and maps implementation details back to spec requirements.",
    color: "blue",
  },
  {
    icon: (
      <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
      </svg>
    ),
    title: "LLM Comparison",
    description:
      "Semantically compares spec requirements against client code using large language models for deep compliance checks.",
    color: "emerald",
  },
  {
    icon: (
      <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
      </svg>
    ),
    title: "CI Integration",
    description:
      "Ships as a GitHub Action for automated spec-compliance checks on every pull request.",
    color: "cyan",
  },
];

const colorMap: Record<string, string> = {
  purple: "text-purple-400 bg-purple-500/10 border-purple-500/20",
  blue: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  cyan: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20",
};

export default function Features() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <h2 className="mb-3 text-center text-3xl font-bold text-white">
        Built for Ethereum
      </h2>
      <p className="mb-12 text-center text-slate-500">
        Everything you need to keep client implementations in sync with EIP specifications.
      </p>
      <div className="grid gap-5 sm:grid-cols-2">
        {features.map((f) => (
          <div
            key={f.title}
            className="eth-card-glow group rounded-2xl border border-white/5 bg-white/[0.02] p-7 transition-all duration-300"
          >
            <div className={`mb-4 inline-flex rounded-xl border p-3 ${colorMap[f.color]}`}>
              {f.icon}
            </div>
            <h3 className="mb-2 text-lg font-semibold text-white">
              {f.title}
            </h3>
            <p className="text-sm leading-relaxed text-slate-400">{f.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
