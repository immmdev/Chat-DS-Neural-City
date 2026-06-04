"""
Constants and whitelists for the Road Safety Analytics Backend.
These define the allowed operations, columns, and values to ensure
safe query execution without arbitrary code execution.
"""

# ── Allowed Dataset Columns ──────────────────────────────────────────────────
ALLOWED_COLUMNS = [
    "accident_id",
    "city",
    "state",
    "latitude",
    "longitude",
    "date",
    "time",
    "hour",
    "day_of_week",
    "is_weekend",
    "road_type",
    "lanes",
    "traffic_signal",
    "weather",
    "visibility",
    "temperature",
    "traffic_density",
    "cause",
    "accident_severity",
    "vehicles_involved",
    "casualties",
    "is_peak_hour",
    "festival",
    "risk_score",
]

# ── Numeric Columns (can be aggregated) ──────────────────────────────────────
NUMERIC_COLUMNS = [
    "latitude",
    "longitude",
    "hour",
    "lanes",
    "temperature",
    "vehicles_involved",
    "casualties",
    "risk_score",
]

# ── Categorical Columns (can be grouped / filtered with exact values) ────────
CATEGORICAL_COLUMNS = [
    "city",
    "state",
    "day_of_week",
    "is_weekend",
    "road_type",
    "traffic_signal",
    "weather",
    "visibility",
    "traffic_density",
    "cause",
    "accident_severity",
    "is_peak_hour",
    "festival",
]

# ── Columns valid for group_by operations ────────────────────────────────────
GROUPABLE_COLUMNS = [
    "city",
    "state",
    "day_of_week",
    "is_weekend",
    "road_type",
    "weather",
    "visibility",
    "traffic_density",
    "cause",
    "accident_severity",
    "is_peak_hour",
    "festival",
    "traffic_signal",
    "hour",
    "month",        # derived column
    "year",         # derived column
    "date",
]

# ── Allowed Aggregation Functions ────────────────────────────────────────────
ALLOWED_AGGREGATIONS = ["count", "sum", "mean", "min", "max"]

# ── Allowed Metric Columns (what can be counted / summed / averaged) ─────────
ALLOWED_METRICS = [
    "accident_id",       # for counting accidents
    "accident_count",    # alias for count of accidents
    "casualties",
    "vehicles_involved",
    "risk_score",
    "temperature",
    "lanes",
]

# ── Allowed Intent Types ─────────────────────────────────────────────────────
ALLOWED_INTENTS = [
    "aggregate",
    "compare",
    "trend",
    "top_n",
    "distribution",
    "filter",
    "out_of_scope",
]

# ── Default Values ───────────────────────────────────────────────────────────
DEFAULT_AGGREGATION = "count"
DEFAULT_METRIC = "accident_id"
DEFAULT_TOP_N = 5
MAX_TOP_N = 20

# ── Chart Configuration ─────────────────────────────────────────────────────
CHART_DIR = "charts"
CHART_INTENT_MAP = {
    "trend": "line",
    "compare": "bar",
    "distribution": "pie",
    "top_n": "hbar",
    "aggregate": "bar",
    "filter": "bar",
}

# ── Color Palette for Charts ─────────────────────────────────────────────────
CHART_COLORS = [
    "#6366f1",  # indigo
    "#f43f5e",  # rose
    "#10b981",  # emerald
    "#f59e0b",  # amber
    "#3b82f6",  # blue
    "#8b5cf6",  # violet
    "#ec4899",  # pink
    "#14b8a6",  # teal
    "#ef4444",  # red
    "#84cc16",  # lime
]
