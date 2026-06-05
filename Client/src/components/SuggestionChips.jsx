/**
 * SuggestionChips — palette: #6367FF · #7B8FE8 · #C5C5F0 · #FFD6F8
 */
import {
  MapPin, BarChart2, AlertTriangle, Clock,
  CloudRain, Sparkles, Navigation,
} from "lucide-react";

const ICON_MAP = { MapPin, BarChart2, AlertTriangle, Clock, CloudRain, Sparkles, Navigation };

// Each chip gets a tint from the palette
const CHIP_STYLES = [
  { bg: "rgba(99,103,255,0.12)", border: "rgba(99,103,255,0.28)", icon: "#6367FF", text: "#C5C5F0" },
  { bg: "rgba(123,143,232,0.12)", border: "rgba(123,143,232,0.28)", icon: "#7B8FE8", text: "#C5C5F0" },
  { bg: "rgba(197,197,240,0.10)", border: "rgba(197,197,240,0.24)", icon: "#C5C5F0", text: "#C5C5F0" },
  { bg: "rgba(255,214,248,0.10)", border: "rgba(255,214,248,0.22)", icon: "#FFD6F8", text: "#C5C5F0" },
  { bg: "rgba(99,103,255,0.12)", border: "rgba(99,103,255,0.28)", icon: "#6367FF", text: "#C5C5F0" },
  { bg: "rgba(197,197,240,0.10)", border: "rgba(197,197,240,0.24)", icon: "#C5C5F0", text: "#C5C5F0" },
  { bg: "rgba(123,143,232,0.12)", border: "rgba(123,143,232,0.28)", icon: "#7B8FE8", text: "#C5C5F0" },
];

export default function SuggestionChips({ questions, onSelect }) {
  return (
    <div className="w-full max-w-5xl mx-auto">
      <p className="text-center text-xs font-semibold tracking-widest uppercase mb-5"
        style={{ color: "rgba(123,143,232,0.55)" }}>
        Frequently asked questions
      </p>

      <div className="flex-col space-y-2 w-full"
        style={{ scrollbarWidth: "thin" }}>
        {questions.map((q, idx) => {
          const Icon = ICON_MAP[q.icon] ?? MapPin;
          const s = CHIP_STYLES[idx % CHIP_STYLES.length];
          return (
            <button
              key={q.id}
              onClick={() => onSelect(q.label)}
              className="
                shrink-0 flex cursor-pointer items-start gap-2.5
                px-4 py-3.5 rounded-2xl text-left text-xs w-full font-medium
                transition-all duration-200
                hover:scale-[1.04] active:scale-[0.97]
              "
              style={{
                background: s.bg,
                border: `1px solid ${s.border}`,
                backdropFilter: "blur(12px)",
                color: s.text,
             
                boxShadow: "0 1px 0 rgba(255,255,255,0.06) inset",
              }}
            >
              <span className="shrink-0 mt-0.5 transition-transform duration-200 group-hover:scale-110"
                style={{ color: s.icon }}>
                <Icon size={14} />
              </span>
              <span className="leading-snug overflow-hidden"
                style={{ display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical" }}>
                {q.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
