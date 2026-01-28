import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative overflow-hidden grid-bg">
      {/* Gradient orbs */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 h-[500px] w-[800px] rounded-full bg-purple-600/10 blur-[120px]" />
      <div className="pointer-events-none absolute top-20 left-1/4 h-[300px] w-[400px] rounded-full bg-blue-600/10 blur-[100px]" />

      <div className="relative flex flex-col items-center gap-8 px-6 py-28 text-center">
        {/* Floating ETH diamond */}
        <div className="eth-diamond mb-2">
          <svg width="64" height="104" viewBox="0 0 256 417" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M127.961 0L125.166 9.5V285.168L127.961 287.958L255.923 212.32L127.961 0Z" fill="#7B3FE4" />
            <path d="M127.962 0L0 212.32L127.962 287.958V154.158V0Z" fill="#9F73FF" />
            <path d="M127.961 312.187L126.386 314.107V412.306L127.961 416.905L255.999 236.587L127.961 312.187Z" fill="#7B3FE4" />
            <path d="M127.962 416.905V312.187L0 236.587L127.962 416.905Z" fill="#9F73FF" />
            <path d="M127.961 287.958L255.922 212.32L127.961 154.158V287.958Z" fill="#5C2DB8" />
            <path d="M0 212.32L127.962 287.958V154.158L0 212.32Z" fill="#7B3FE4" />
          </svg>
        </div>

        <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl">
          <span className="eth-gradient-text">Awesome Eth Linter</span>
        </h1>

        <p className="max-w-2xl text-lg leading-relaxed text-slate-400">
          Automatically verify Ethereum client implementations against official
          EIP specifications using <span className="text-purple-400">LLM-powered</span> analysis.
        </p>

        <div className="flex gap-4 mt-2">
          <Link
            href="/docs"
            className="eth-gradient rounded-xl px-7 py-3.5 font-semibold text-white shadow-lg shadow-purple-500/20 transition-all hover:shadow-purple-500/40 hover:scale-105"
          >
            Get Started
          </Link>
          <a
            href="https://github.com/nichechristie/eth-spec-lint"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-xl border border-white/10 bg-white/5 px-7 py-3.5 font-semibold text-slate-300 backdrop-blur transition-all hover:border-purple-500/30 hover:bg-white/10"
          >
            View on GitHub
          </a>
        </div>

        {/* Stats bar */}
        <div className="mt-8 flex gap-8 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-green-500" />
            Open Source
          </div>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-purple-500" />
            LLM-Powered
          </div>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-blue-500" />
            CI Ready
          </div>
        </div>
      </div>
    </section>
  );
}
