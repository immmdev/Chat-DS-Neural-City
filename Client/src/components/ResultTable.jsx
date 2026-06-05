/**
 * ResultTable — sortable, paginated. Palette: #6367FF · #7B8FE8 · #C5C5F0 · #FFD6F8
 */
import { useState } from "react";
import { Table2, ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";

const PAGE_SIZE = 10;

function formatCell(val) {
  if (val === null || val === undefined)
    return <span style={{ color: "rgba(123,143,232,0.35)" }}>—</span>;
  if (typeof val === "number")
    return <span className="font-mono" style={{ color: "#C5C5F0" }}>
      {Number.isInteger(val) ? val.toLocaleString() : val.toFixed(3)}
    </span>;
  return <span style={{ color: "#e4e4f7" }}>{String(val)}</span>;
}

export default function ResultTable({ resultTable }) {
  const [page, setPage]       = useState(0);
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState("desc");

  if (!resultTable?.length) return null;
  const columns = Object.keys(resultTable[0]);

  const sorted = sortKey
    ? [...resultTable].sort((a, b) => {
        const [av, bv] = [a[sortKey], b[sortKey]];
        if (typeof av === "number" && typeof bv === "number")
          return sortDir === "asc" ? av - bv : bv - av;
        return sortDir === "asc"
          ? String(av).localeCompare(String(bv))
          : String(bv).localeCompare(String(av));
      })
    : resultTable;

  const totalPages = Math.ceil(sorted.length / PAGE_SIZE);
  const pageData   = sorted.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  function toggleSort(key) {
    if (sortKey === key) setSortDir((d) => d === "asc" ? "desc" : "asc");
    else { setSortKey(key); setSortDir("desc"); }
    setPage(0);
  }

  const surface  = "rgba(99,103,255,0.04)";
  const border   = "rgba(99,103,255,0.12)";
  const rowHover = "rgba(99,103,255,0.07)";

  return (
    <div className="rounded-3xl overflow-hidden"
      style={{ background: surface, border: `1px solid ${border}`, backdropFilter: "blur(16px)" }}>

      {/* Header row */}
      <div className="flex items-center justify-between px-6 py-4"
        style={{ borderBottom: `1px solid ${border}` }}>
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-xl flex items-center justify-center"
            style={{ background: "linear-gradient(135deg,#C5C5F0,#FFD6F8)" }}>
            <Table2 size={13} style={{ color: "#0b0b18" }} />
          </div>
          <span className="text-xs font-bold tracking-widest uppercase"
            style={{ color: "#C5C5F0" }}>Data Table</span>
        </div>
        <span className="text-xs" style={{ color: "rgba(123,143,232,0.5)" }}>
          {sorted.length} rows · {columns.length} cols
        </span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr style={{ borderBottom: `1px solid ${border}` }}>
              {columns.map((col) => (
                <th key={col} onClick={() => toggleSort(col)}
                  className="px-5 py-3 text-left font-semibold cursor-pointer select-none whitespace-nowrap transition-colors duration-150"
                  style={{ color: sortKey === col ? "#C5C5F0" : "rgba(123,143,232,0.65)" }}>
                  <span className="inline-flex items-center gap-1">
                    {col}
                    {sortKey === col
                      ? sortDir === "asc"
                        ? <ChevronUp size={11} style={{ color: "#6367FF" }} />
                        : <ChevronDown size={11} style={{ color: "#6367FF" }} />
                      : <ChevronDown size={11} style={{ opacity: 0.2 }} />}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageData.map((row, ri) => (
              <tr key={ri} className="transition-colors duration-100"
                style={{ borderBottom: `1px solid rgba(99,103,255,0.06)` }}
                onMouseEnter={(e) => (e.currentTarget.style.background = rowHover)}
                onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}>
                {columns.map((col) => (
                  <td key={col} className="px-5 py-3 whitespace-nowrap">
                    {formatCell(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-6 py-3"
          style={{ borderTop: `1px solid ${border}` }}>
          <button onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="flex items-center gap-1 text-xs transition-opacity disabled:opacity-30"
            style={{ color: "#7B8FE8" }}>
            <ChevronLeft size={14} /> Prev
          </button>
          <span className="text-xs" style={{ color: "rgba(123,143,232,0.45)" }}>
            {page + 1} / {totalPages}
          </span>
          <button onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page === totalPages - 1}
            className="flex items-center gap-1 text-xs transition-opacity disabled:opacity-30"
            style={{ color: "#7B8FE8" }}>
            Next <ChevronRight size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
