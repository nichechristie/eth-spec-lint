import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-white/5 bg-[#0a0a1a]/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2.5 text-lg font-bold text-white">
          <EthDiamond />
          Awesome Eth Linter
        </Link>
        <div className="flex items-center gap-6 text-sm">
          <Link href="/docs" className="text-slate-400 hover:text-white transition-colors">
            Docs
          </Link>
          <a
            href="https://github.com/nichechristie/eth-spec-lint"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-1.5 text-slate-300 transition-all hover:border-purple-500/40 hover:bg-white/10"
          >
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
}

function EthDiamond() {
  return (
    <svg width="20" height="32" viewBox="0 0 256 417" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M127.961 0L125.166 9.5V285.168L127.961 287.958L255.923 212.32L127.961 0Z" fill="#7B3FE4" />
      <path d="M127.962 0L0 212.32L127.962 287.958V154.158V0Z" fill="#9F73FF" />
      <path d="M127.961 312.187L126.386 314.107V412.306L127.961 416.905L255.999 236.587L127.961 312.187Z" fill="#7B3FE4" />
      <path d="M127.962 416.905V312.187L0 236.587L127.962 416.905Z" fill="#9F73FF" />
      <path d="M127.961 287.958L255.922 212.32L127.961 154.158V287.958Z" fill="#5C2DB8" />
      <path d="M0 212.32L127.962 287.958V154.158L0 212.32Z" fill="#7B3FE4" />
    </svg>
  );
}
