/**
 * HeroSection — palette: #6367FF · #7B8FE8 · #C5C5F0 · #FFD6F8
 */
import { ArrowDown } from "lucide-react";

export default function HeroSection({ heroBgUrl, onScrollToSearch }) {
  return (
    <section
      className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden"
      style={{ background: "radial-gradient(ellipse 90% 70% at 50% -5%, #1a1a4e 0%, #0b0b18 68%)" }}
    >
      {/* BG image overlay */}
      {heroBgUrl && (
        <div className="absolute inset-0 opacity-15 bg-cover bg-center"
          style={{ backgroundImage: `url(${heroBgUrl})` }} />
      )}

      {/* Orbs */}
      <div className="absolute top-1/4 left-1/5 w-80 h-80 rounded-full blur-3xl animate-orb pointer-events-none"
        style={{ background: "#6367FF", opacity: 0.18 }} />
      <div className="absolute bottom-1/4 right-1/5 w-60 h-60 rounded-full blur-3xl animate-orb pointer-events-none"
        style={{ background: "#C5C5F0", opacity: 0.12, animationDelay: "1.5s" }} />
      <div className="absolute top-2/3 left-1/3 w-44 h-44 rounded-full blur-2xl animate-orb pointer-events-none"
        style={{ background: "#FFD6F8", opacity: 0.1, animationDelay: "3s" }} />

      {/* Dot-grid overlay */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.035]"
        style={{
          backgroundImage: "radial-gradient(circle, #6367FF 1px, transparent 1px)",
          backgroundSize: "36px 36px",
        }} />

      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-4xl mx-auto pt-24">

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-8 text-xs font-semibold tracking-widest uppercase"
          style={{
            background: "rgba(99,103,255,0.12)",
            border: "1px solid rgba(99,103,255,0.28)",
            color: "#C5C5F0",
          }}>
          <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "#6367FF" }} />
          AI-Powered Open Data Analytics
        </div>

        {/* Headline */}
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold leading-tight tracking-tight mb-6">
          <span style={{ color: "#e4e4f7" }}>Ask anything about</span>
          <br />
          <span style={{
            background: "linear-gradient(135deg, #6367FF 0%, #7B8FE8 40%, #C5C5F0 70%, #FFD6F8 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}>
            Indian Road Safety
          </span>
        </h1>

        <p className="text-base sm:text-lg leading-relaxed max-w-2xl mx-auto mb-12"
          style={{ color: "#7B8FE8" }}>
          Government open data — structured, searchable, visualized. Get{" "}
          <span style={{ color: "#C5C5F0", fontWeight: 600 }}>precise, data-backed answers</span>{" "}
          with charts in plain English.
        </p>

        {/* Stats */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {[
            { label: "Accident Records", value: "20,000+" },
            { label: "Cities Covered",   value: "5+" },
            { label: "Data Columns",     value: "20+" },
          ].map(({ label, value }) => (
            <div key={label} className="text-center px-6 py-3 rounded-2xl"
              style={{
                background: "rgba(99,103,255,0.08)",
                border: "1px solid rgba(99,103,255,0.2)",
                backdropFilter: "blur(12px)",
              }}>
              <div className="text-2xl font-bold" style={{ color: "#C5C5F0" }}>{value}</div>
              <div className="text-xs font-medium" style={{ color: "#7B8FE8" }}>{label}</div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <button
          onClick={onScrollToSearch}
          className="group inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl font-semibold text-sm transition-all duration-300 hover:scale-105"
          style={{
            background: "linear-gradient(135deg, #6367FF, #7B8FE8)",
            color: "#fff",
            boxShadow: "0 4px 24px rgba(99,103,255,0.4), 0 1px 0 rgba(255,255,255,0.15) inset",
          }}>
          Start Exploring
          <ArrowDown size={16} className="group-hover:translate-y-1 transition-transform duration-300" />
        </button>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-36 pointer-events-none"
        style={{ background: "linear-gradient(to top, #0b0b18, transparent)" }} />
    </section>
  );
}
