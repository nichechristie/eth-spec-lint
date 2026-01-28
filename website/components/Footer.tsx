export default function Footer() {
  return (
    <footer className="border-t border-white/5 py-10">
      <div className="mx-auto max-w-6xl px-6 flex flex-col items-center gap-4 sm:flex-row sm:justify-between">
        <div className="flex items-center gap-2 text-sm text-slate-500">
          <svg width="12" height="20" viewBox="0 0 256 417" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M127.961 0L125.166 9.5V285.168L127.961 287.958L255.923 212.32L127.961 0Z" fill="#4B5563" />
            <path d="M127.962 0L0 212.32L127.962 287.958V154.158V0Z" fill="#6B7280" />
            <path d="M127.961 312.187L126.386 314.107V412.306L127.961 416.905L255.999 236.587L127.961 312.187Z" fill="#4B5563" />
            <path d="M127.962 416.905V312.187L0 236.587L127.962 416.905Z" fill="#6B7280" />
          </svg>
          Awesome Eth Linter
        </div>
        <p className="text-sm text-slate-600">
          Ethereum specification compliance linter
        </p>
      </div>
    </footer>
  );
}
