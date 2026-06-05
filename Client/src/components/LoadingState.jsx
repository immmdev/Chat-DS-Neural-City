/**
 * LoadingState — skeleton + bouncing dots, palette-matched.
 */
export default function LoadingState({ question }) {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-fade-in">

      {/* Question echo */}
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full shrink-0 flex items-center justify-center text-white text-xs font-bold"
          style={{ background: "linear-gradient(135deg,#6367FF,#7B8FE8)" }}>
          ?
        </div>
        <div className="flex-1 px-4 py-2.5 rounded-2xl text-sm italic"
          style={{ background: "rgba(99,103,255,0.08)", border: "1px solid rgba(99,103,255,0.18)", color: "#C5C5F0" }}>
          {question}
        </div>
      </div>

      {/* Thinking dots */}
      <div className="flex items-center gap-3 pl-11">
        <div className="flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <span key={i} className="w-2 h-2 rounded-full"
              style={{
                background: i === 0 ? "#6367FF" : i === 1 ? "#7B8FE8" : "#C5C5F0",
                animation: `bounce-dot 1s ${i * 0.18}s infinite`,
              }} />
          ))}
        </div>
        <span className="text-xs" style={{ color: "#7B8FE8" }}>Analysing dataset…</span>
      </div>

      {/* Skeleton grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {[0, 1].map((card) => (
          <div key={card} className="rounded-3xl p-6 space-y-3"
            style={{ background: "rgba(99,103,255,0.05)", border: "1px solid rgba(99,103,255,0.12)" }}>
            <div className="h-3 w-20 rounded-full animate-pulse"
              style={{ background: "rgba(99,103,255,0.18)" }} />
            {[100, 85, 70, 55].map((w, i) => (
              <div key={i} className="h-3 rounded-full animate-pulse"
                style={{ width: `${w}%`, background: `rgba(99,103,255,${0.1 - i * 0.02})`, animationDelay: `${i * 80}ms` }} />
            ))}
          </div>
        ))}
      </div>

      {/* Table skeleton */}
      <div className="rounded-3xl overflow-hidden"
        style={{ background: "rgba(99,103,255,0.04)", border: "1px solid rgba(99,103,255,0.1)" }}>
        {[...Array(4)].map((_, i) => (
          <div key={i} className="flex gap-4 px-6 py-3"
            style={{ borderBottom: "1px solid rgba(99,103,255,0.07)" }}>
            {[70, 55, 80, 40].map((w, j) => (
              <div key={j} className="h-2.5 rounded-full animate-pulse"
                style={{ width: `${w}%`, background: "rgba(99,103,255,0.1)", animationDelay: `${i * 60}ms` }} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
