/**
 * Navbar — floating island style, centered, glossy.
 */
import { Activity, Database, Zap } from "lucide-react";

export default function Navbar({ healthy }) {
  return (
    /* Outer positioning wrapper — does NOT block content */
    <div className="fixed top-5 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
      {/* Island pill */}
      <nav
        className="
          island-nav
          pointer-events-auto
          flex items-center justify-between
          gap-6 px-5 py-2.5
          rounded-full
          w-full max-w-2xl
        "
      >
        {/* Brand */}
        <div className="flex items-center gap-2.5">
          <div className="relative w-8 h-8 rounded-full flex items-center justify-center shrink-0"
            style={{ background: "linear-gradient(135deg,#6367FF,#C5C5F0)" }}>
            <Zap size={15} className="text-white" />
            <span className="absolute inset-0 rounded-full animate-ping opacity-30"
              style={{ background: "#6367FF" }} />
          </div>
          <span className="text-sm font-bold tracking-tight"
            style={{ color: "#C5C5F0" }}>
            Neural<span style={{ color: "#6367FF" }}>City</span>
          </span>
        </div>

        {/* Dataset tag — hidden on very small screens */}
        <div className="hidden sm:flex items-center gap-1.5 text-xs"
          style={{ color: "#7B8FE8" }}>
          <Database size={12} style={{ color: "#7B8FE8" }} />
          Indian Roads Dataset
        </div>

        {/* Health badge */}
        <div
          className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border"
          style={
            healthy === true
              ? { background: "rgba(99,103,255,0.15)", borderColor: "rgba(99,103,255,0.35)", color: "#C5C5F0" }
              : healthy === false
              ? { background: "rgba(255,100,100,0.12)", borderColor: "rgba(255,100,100,0.3)", color: "#FFD6F8" }
              : { background: "rgba(197,197,240,0.08)", borderColor: "rgba(197,197,240,0.2)", color: "#7B8FE8" }
          }
        >
          <Activity size={11} />
          {healthy === true ? "Live" : healthy === false ? "Offline" : "…"}
        </div>
      </nav>
    </div>
  );
}
