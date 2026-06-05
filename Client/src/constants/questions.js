/**
 * DEFAULT_QUESTIONS — pre-seeded questions for the suggestion chips.
 */
export const DEFAULT_QUESTIONS = [
  {
    id: 1,
    label: "Which city has the highest number of accidents?",
    icon: "MapPin",
    color: "from-violet-400/20 to-purple-500/20 border-violet-400/30",
    accent: "text-violet-300",
  },
  {
    id: 2,
    label: "Compare average risk score between Delhi and Mumbai.",
    icon: "BarChart2",
    color: "from-sky-400/20 to-cyan-500/20 border-sky-400/30",
    accent: "text-sky-300",
  },
  {
    id: 3,
    label: "Top 5 cities with the highest casualties.",
    icon: "AlertTriangle",
    color: "from-rose-400/20 to-pink-500/20 border-rose-400/30",
    accent: "text-rose-300",
  },
  {
    id: 4,
    label: "How do accident counts vary by hour of the day?",
    icon: "Clock",
    color: "from-amber-400/20 to-orange-500/20 border-amber-400/30",
    accent: "text-amber-300",
  },
  {
    id: 5,
    label: "How are accidents distributed across weather conditions?",
    icon: "CloudRain",
    color: "from-teal-400/20 to-emerald-500/20 border-teal-400/30",
    accent: "text-teal-300",
  },
  {
    id: 6,
    label: "Show fatal accidents during festivals.",
    icon: "Sparkles",
    color: "from-fuchsia-400/20 to-purple-500/20 border-fuchsia-400/30",
    accent: "text-fuchsia-300",
  },
  {
    id: 7,
    label: "Which road type has the highest average risk score?",
    icon: "Navigation",
    color: "from-lime-400/20 to-green-500/20 border-lime-400/30",
    accent: "text-lime-300",
  },
];

export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
