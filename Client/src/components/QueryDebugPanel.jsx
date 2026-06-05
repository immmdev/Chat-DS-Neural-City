/**
 * QueryDebugPanel — collapsible JSON inspector, palette-matched.
 */
import { useState } from "react";
import { Code2, ChevronDown, ChevronUp } from "lucide-react";

export default function QueryDebugPanel({ queryJson }) {
  const [open, setOpen] = useState(false);
  if (!queryJson) return null;

  return (
    <div className="rounded-2xl overflow-hidden"
      style={{ background: "rgba(99,103,255,0.04)", border: "1px solid rgba(99,103,255,0.12)" }}>
      <button onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-5 py-3 transition-colors duration-150"
        style={{ color: "rgba(123,143,232,0.55)" }}>
        <span className="flex items-center gap-2 text-xs font-semibold tracking-wide">
          <Code2 size={13} />
          Structured Query JSON
        </span>
        {open
          ? <ChevronUp size={13} />
          : <ChevronDown size={13} />}
      </button>

      {open && (
        <pre className="px-5 pb-5 text-[11px] leading-relaxed font-mono overflow-x-auto"
          style={{
            color: "#C5C5F0",
            borderTop: "1px solid rgba(99,103,255,0.1)",
          }}>
          {JSON.stringify(queryJson, null, 2)}
        </pre>
      )}
    </div>
  );
}
