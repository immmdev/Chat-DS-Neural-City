/**
 * ErrorCard — blush-pink error styling from the palette.
 */
import { AlertCircle, RefreshCw } from "lucide-react";

export default function ErrorCard({ message, onRetry }) {
  return (
    <div className="w-full max-w-2xl mx-auto rounded-3xl p-8 flex flex-col items-center gap-5 text-center"
      style={{
        background: "rgba(255,214,248,0.07)",
        border: "1px solid rgba(255,214,248,0.2)",
        backdropFilter: "blur(16px)",
        boxShadow: "0 1px 0 rgba(255,255,255,0.05) inset",
      }}>

      <div className="w-14 h-14 rounded-2xl flex items-center justify-center"
        style={{ background: "rgba(255,214,248,0.12)", border: "1px solid rgba(255,214,248,0.25)" }}>
        <AlertCircle size={26} style={{ color: "#FFD6F8" }} />
      </div>

      <div>
        <h3 className="font-semibold text-base mb-2" style={{ color: "#C5C5F0" }}>
          Something went wrong
        </h3>
        <p className="text-sm leading-relaxed max-w-sm" style={{ color: "#7B8FE8" }}>
          {message || "An unexpected error occurred. Please try again."}
        </p>
      </div>

      {onRetry && (
        <button onClick={onRetry}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95"
          style={{
            background: "rgba(255,214,248,0.1)",
            border: "1px solid rgba(255,214,248,0.22)",
            color: "#FFD6F8",
          }}>
          <RefreshCw size={13} />
          Try again
        </button>
      )}
    </div>
  );
}
