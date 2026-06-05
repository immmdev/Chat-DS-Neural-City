/**
 * ChartPanel — Recharts charts with palette: #6367FF · #7B8FE8 · #C5C5F0 · #FFD6F8
 */
import {
  BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { BarChart2 } from "lucide-react";

// Palette-only colors for chart series
const PALETTE = ["#6367FF", "#7B8FE8", "#C5C5F0", "#FFD6F8", "#a8aeff", "#d0d3ff", "#ffe0fb"];

const TOOLTIP_STYLE = {
  backgroundColor: "rgba(11,11,24,0.94)",
  border: "1px solid rgba(99,103,255,0.28)",
  borderRadius: "14px",
  color: "#C5C5F0",
  fontSize: "12px",
  boxShadow: "0 8px 32px rgba(99,103,255,0.25)",
};

function detectChartType(data) {
  if (!data?.length) return null;
  const keys = Object.keys(data[0]);
  const hasHour = keys.some((k) => k.toLowerCase().includes("hour"));
  const numericKeys = keys.filter((k) => typeof data[0][k] === "number");
  const stringKeys  = keys.filter((k) => typeof data[0][k] === "string");
  if (hasHour && numericKeys.length >= 1) return "area";
  if (data.length <= 8 && stringKeys.length === 1 && numericKeys.length === 1) return "pie";
  return "bar";
}

function getChartKeys(data) {
  if (!data?.length) return { xKey: null, yKeys: [] };
  const keys = Object.keys(data[0]);
  const stringKeys  = keys.filter((k) => typeof data[0][k] === "string");
  const numericKeys = keys.filter((k) => typeof data[0][k] === "number");
  const xKey  = stringKeys[0] || keys[0];
  const yKeys = numericKeys.length > 0 ? numericKeys : keys.filter((k) => k !== xKey);
  return { xKey, yKeys };
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={TOOLTIP_STYLE} className="px-3.5 py-2.5">
      <p className="font-semibold text-xs mb-1.5 truncate max-w-[200px]"
        style={{ color: "#C5C5F0" }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="text-xs" style={{ color: p.color }}>
          {p.name}:{" "}
          <strong>{typeof p.value === "number" ? p.value.toLocaleString() : p.value}</strong>
        </p>
      ))}
    </div>
  );
}

const AXIS_TICK = { fill: "rgba(123,143,232,0.55)", fontSize: 10 };
const GRID_STROKE = "rgba(99,103,255,0.1)";

function BarChartView({ data, xKey, yKeys }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 48 }}>
        <defs>
          {yKeys.map((k, i) => (
            <linearGradient key={k} id={`bg${i}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%"  stopColor={PALETTE[i % PALETTE.length]} stopOpacity={0.9} />
              <stop offset="100%" stopColor={PALETTE[i % PALETTE.length]} stopOpacity={0.3} />
            </linearGradient>
          ))}
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={GRID_STROKE} />
        <XAxis dataKey={xKey} tick={AXIS_TICK} tickLine={false}
          axisLine={{ stroke: GRID_STROKE }} angle={-35} textAnchor="end"
          interval={0} height={55} />
        <YAxis tick={AXIS_TICK} tickLine={false} axisLine={false}
          tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v} />
        <Tooltip content={<CustomTooltip />} />
        {yKeys.length > 1 && <Legend wrapperStyle={{ color: "#7B8FE8", fontSize: 11 }} />}
        {yKeys.map((k, i) => (
          <Bar key={k} dataKey={k} fill={`url(#bg${i})`} radius={[6, 6, 0, 0]} maxBarSize={52} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

function AreaChartView({ data, xKey, yKeys }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 20 }}>
        <defs>
          {yKeys.map((k, i) => (
            <linearGradient key={k} id={`ag${i}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%"   stopColor={PALETTE[i % PALETTE.length]} stopOpacity={0.45} />
              <stop offset="100%" stopColor={PALETTE[i % PALETTE.length]} stopOpacity={0.0} />
            </linearGradient>
          ))}
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={GRID_STROKE} />
        <XAxis dataKey={xKey} tick={AXIS_TICK} tickLine={false} axisLine={{ stroke: GRID_STROKE }} />
        <YAxis tick={AXIS_TICK} tickLine={false} axisLine={false}
          tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v} />
        <Tooltip content={<CustomTooltip />} />
        {yKeys.length > 1 && <Legend wrapperStyle={{ color: "#7B8FE8", fontSize: 11 }} />}
        {yKeys.map((k, i) => (
          <Area key={k} type="monotone" dataKey={k}
            stroke={PALETTE[i % PALETTE.length]} strokeWidth={2.5}
            fill={`url(#ag${i})`} dot={false}
            activeDot={{ r: 5, strokeWidth: 0, fill: PALETTE[i % PALETTE.length] }} />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  );
}

const RADIAN = Math.PI / 180;
function PieChartView({ data, xKey, yKey }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%"
          innerRadius={62} outerRadius={105}
          dataKey={yKey} nameKey={xKey}
          paddingAngle={3} labelLine={false}
          label={({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
            const r = innerRadius + (outerRadius - innerRadius) * 0.5;
            const x = cx + r * Math.cos(-midAngle * RADIAN);
            const y = cy + r * Math.sin(-midAngle * RADIAN);
            return percent > 0.05 ? (
              <text x={x} y={y} fill="white" textAnchor="middle"
                dominantBaseline="central" fontSize={11} fontWeight="600">
                {`${(percent * 100).toFixed(0)}%`}
              </text>
            ) : null;
          }}>
          {data.map((_, i) => <Cell key={i} fill={PALETTE[i % PALETTE.length]} />)}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ color: "#7B8FE8", fontSize: 11 }}
          formatter={(v) => String(v).slice(0, 20)} />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default function ChartPanel({ resultTable }) {
  if (!resultTable?.length) return null;
  const chartType = detectChartType(resultTable);
  const { xKey, yKeys } = getChartKeys(resultTable);
  if (!xKey || !yKeys.length) return null;

  return (
    <div className="rounded-3xl p-6 space-y-4"
      style={{
        background: "linear-gradient(135deg, rgba(123,143,232,0.09) 0%, rgba(255,214,248,0.06) 100%)",
        border: "1px solid rgba(123,143,232,0.2)",
        backdropFilter: "blur(16px)",
        boxShadow: "0 2px 0 rgba(255,255,255,0.05) inset",
      }}>

      {/* Header */}
      <div className="flex items-center gap-2.5">
        <div className="w-7 h-7 rounded-xl flex items-center justify-center shrink-0"
          style={{ background: "linear-gradient(135deg,#7B8FE8,#FFD6F8)" }}>
          <BarChart2 size={13} className="text-white" />
        </div>
        <span className="text-xs font-bold tracking-widest uppercase"
          style={{ color: "#7B8FE8" }}>Visualization</span>
      </div>

      {chartType === "area" && <AreaChartView data={resultTable} xKey={xKey} yKeys={yKeys} />}
      {chartType === "pie"  && <PieChartView  data={resultTable} xKey={xKey} yKey={yKeys[0]} />}
      {chartType === "bar"  && <BarChartView  data={resultTable} xKey={xKey} yKeys={yKeys} />}
    </div>
  );
}
