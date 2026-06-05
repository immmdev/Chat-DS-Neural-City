import { useState, useRef, useEffect } from "react";
import { Search, Send, X, Loader2 } from "lucide-react";

export default function SearchBar({ onSubmit, loading, initialValue = "" }) {
  const [value, setValue] = useState(initialValue);
  const inputRef = useRef(null);

  useEffect(() => {
    setValue(initialValue);
    if (initialValue) inputRef.current?.focus();
  }, [initialValue]);

  function handleSubmit(e) {
    e?.preventDefault();
    if (!value.trim() || loading) return;
    onSubmit(value.trim());
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit(); }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div
        className="relative flex items-center gap-3 px-5 py-4 rounded-3xl transition-all duration-300"
        style={{
          background: "rgba(99,103,255,0.08)",
          border: "1px solid rgba(99,103,255,0.22)",
          backdropFilter: "blur(20px)",
          boxShadow: "0 2px 0 rgba(255,255,255,0.06) inset, 0 8px 32px rgba(99,103,255,0.12)",
        }}
      >
        <Search size={19} style={{ color: "#7B8FE8", flexShrink: 0 }} />

        <input
          ref={inputRef}
          type="text"
          id="main-search-input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about Indian road accidents…"
          disabled={loading}
          autoComplete="off"
          spellCheck="false"
          className="flex-1 bg-transparent outline-none text-sm sm:text-base font-medium disabled:opacity-60 disabled:cursor-not-allowed"
          style={{ color: "#e4e4f7" }}
        />

        {/* Clear */}
        {value && !loading && (
          <button type="button" onClick={() => { setValue(""); inputRef.current?.focus(); }}
            style={{ color: "#7B8FE8", flexShrink: 0 }}
            className="hover:opacity-70 transition-opacity" aria-label="Clear">
            <X size={15} />
          </button>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={!value.trim() || loading}
          aria-label="Submit question"
          className="shrink-0 cursor-pointer flex items-center justify-center w-9 h-9 rounded-xl transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed hover:scale-105 active:scale-95"
          style={{
            background: "linear-gradient(135deg, #6367FF, #7B8FE8)",
            boxShadow: "0 4px 16px rgba(99,103,255,0.4)",
            color: "#fff",
          }}
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={15} />}
        </button>
      </div>
    </form>
  );
}
