Here's the markdown:

```markdown
# Neural City - Indian Road Accident Analytics

[![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75C2?style=flat-square&logo=googlegemini&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

A web-based data science platform providing an AI-powered conversational analytics interface for the Indian Road Accident Dataset (2022–2025). Ask questions in natural language — they get translated into structured queries, executed against a Pandas engine, and visualized dynamically on the frontend.

---

## Dataset

The system relies on a unified dataset at `Server/indian_roads_dataset.csv`. The client fetches metadata dynamically from `/api/metadata` to align suggestions, constraints, and valid ranges with the server.

**20,002 rows · 24 columns · Jan 2022 – May 2025 · 8 Indian cities**

### Schema

| Column | Type | Description | Sample / Allowed Values |
|---|---|---|---|
| `accident_id` | int64 | Unique record identifier | 0, 1, 2 … |
| `city` | object | Major Indian city | Bangalore, Chandigarh, Chennai, Delhi, Hyderabad, Kolkata, Mumbai, Pune |
| `state` | object | State of the city | Delhi, Karnataka, Maharashtra, Punjab, Tamil Nadu, Telangana, West Bengal |
| `latitude` | float64 | Geospatial latitude | 18.68, 28.80 |
| `longitude` | float64 | Geospatial longitude | 73.93, 77.05 |
| `date` | object | Accident date (YYYY-MM-DD) | 2023-10-22 |
| `time` | object | Time of accident (HH:MM) | 5:00, 16:00 |
| `hour` | int64 | Extracted hour (0–23) | 0, 8, 13, 23 |
| `day_of_week` | object | Day name | Monday … Sunday |
| `is_weekend` | int64 | Weekend flag | 0 = Weekday, 1 = Weekend |
| `road_type` | object | Road infrastructure class | highway, rural, urban |
| `lanes` | int64 | Lane count | 1 – 6 |
| `traffic_signal` | int64 | Signal presence | 0 = No, 1 = Yes |
| `weather` | object | Weather conditions | clear, fog, rain |
| `visibility` | object | Visibility level | low, medium, high |
| `temperature` | int64 | Temperature (°C) | 15 – 40 |
| `traffic_density` | object | Traffic density level | low, medium, high |
| `cause` | object | Primary accident cause | distraction, drunk driving, overspeeding, poor road, weather |
| `accident_severity` | object | Severity outcome | fatal, major, minor |
| `vehicles_involved` | int64 | Vehicle count in collision | 1 – 5 |
| `casualties` | int64 | Injuries / deaths | 0 – 5 |
| `is_peak_hour` | int64 | Peak traffic flag | 0 = No, 1 = Yes |
| `festival` | object | Holiday context | Diwali, Eid, Holi, None |
| `risk_score` | float64 | Engineered hazard score (0–1) | 0.0 – 1.0 |

### Engineered Features

Temporal columns (`hour`, `day_of_week`, `is_weekend`, `is_peak_hour`) are extracted from the raw timestamp. `risk_score` is a composite metric — values near 1.0 cluster around fog, low visibility, peak hours, and highway conditions.

---

## Client Architecture

Responsive single-page application. All state flows through a single custom hook; charts are auto-selected from the result shape without user configuration.

**Stack:** React 19 (Vite) · TailwindCSS v4 · Recharts 3.8.1 · Lucide React · React Markdown + remark-gfm

### File Structure

| File | Role |
|---|---|
| `App.jsx` | Root layout coordinator. Manages views, health checks on load, auto-scrolls to results. |
| `components/Navbar.jsx` | Branding bar with live green/red server connection indicator. |
| `components/HeroSection.jsx` | Welcome header with smooth-scroll to the query workspace. |
| `components/SearchBar.jsx` | Text input with Enter-key and button submission; disabled during in-flight queries. |
| `components/SuggestionChips.jsx` | Clickable seed questions for one-tap query execution. |
| `components/LoadingState.jsx` | Animated skeleton loader with contextual phase feedback. |
| `components/ErrorCard.jsx` | Displays structured API error details with a retry action. |
| `components/ResultSection.jsx` | Hosts the four result panels: Answer, Chart, Table, Debugger. |
| `components/AnswerCard.jsx` | Renders the LLM-synthesised answer from markdown (with GFM tables). |
| `components/ChartPanel.jsx` | Infers and renders the best Recharts visualisation from result shape. |
| `components/ResultTable.jsx` | Scrollable, paginated raw data table. |
| `components/QueryDebugPanel.jsx` | Collapsible panel showing the raw structured query JSON from Gemini. |
| `hooks/useQuery.js` | Encapsulates query state, submission handlers, and AbortController cancellation. |
| `api/queryApi.js` | REST layer with in-memory request cache to prevent redundant calls. |

### Visualisation Inference Logic (`ChartPanel.jsx`)

| Chart | Condition |
|---|---|
| Area Chart | Result contains a temporal field (e.g. `hour`) alongside numeric values |
| Pie Chart | Fewer than 9 rows · exactly one string category column · exactly one numeric column |
| Bar Chart | Default — comparisons, aggregations, top-n results |

---

## Server Architecture

FastAPI backend. Loads the dataset into memory at startup, translates natural-language queries via Gemini, validates the structured output, then executes safe Pandas operations — no `eval()` or `exec()`.

**Stack:** FastAPI (Uvicorn) · Google Gemini 2.5 Flash · LangChain + LangChain Google GenAI · Pandas · Python-Dotenv

### File Structure

| File | Role |
|---|---|
| `app.py` | Entry point. Controls lifespan, loads dataset, configures CORS, binds routes. |
| `routes/query_routes.py` | Query entry point. Wraps execution in a 60-second async timeout; appends to audit log. |
| `schemas/query_schema.py` | Pydantic definitions for `UserQueryRequest` (3–500 chars) and `StructuredQuery`. |
| `schemas/response_schema.py` | Validation rules for endpoint response structures. |
| `services/llm_service.py` | Generates the structured query JSON from natural language; synthesises the final answer from the result DataFrame. |
| `services/validation_service.py` | Maps JSON to whitelisted columns; fuzzy-corrects city spelling; rejects out-of-scope fields. |
| `services/pandas_engine.py` | Safe executor. Routes by intent (aggregate, compare, trend, top_n, distribution, filter) to dedicated Pandas methods. |
| `services/answer_service.py` | Local fallback answer formatter when LLM generation fails or times out. |
| `utils/metadata.py` | Computes ranges, categoricals, and numeric stats at startup; passes them as LLM prompt context. |
| `utils/constants.py` | Whitelists of allowed columns, intents, and aggregation methods securing the pipeline. |

---

## Data Flow

```
User Input
    │
    ▼
useQuery Hook  ──AbortController──▶  queryApi Client
                                          │
                                          │  POST /api/query
                                          ▼
                                    FastAPI Router (process_query)
                                          │
                                          │  system_prompt + user_prompt
                                          ▼
                                    Gemini 2.5 Flash
                                          │
                                          │  StructuredQuery JSON
                                          ▼
                                    validation_service  (fuzzy-correct, whitelist)
                                          │
                                          ▼
                                    pandas_engine  ──▶  indian_roads_dataset.csv
                                          │
                                          │  result DataFrame + operation_desc
                                          ▼
                                    llm_service  (synthesise answer)
                                          │
                                          ▼
                                    QueryResponse JSON
                                          │
                                          ▼
                              React ◀── useQuery state update
                      AnswerCard · ChartPanel · ResultTable · QueryDebugPanel
```

### Steps

1. User submits a question. `useQuery` aborts any in-flight request and fires `POST /api/query`.
2. FastAPI router sets the 60-second timeout and passes the request to `llm_service` with dataset metadata.
3. Gemini returns a structured JSON query (intent, metric, aggregation, filters, group-by).
4. `validation_service` maps to whitelisted columns and fuzzy-corrects values. Returns `400` for invalid fields.
5. `pandas_engine` routes by intent and runs safe Pandas operations on the CSV.
6. The resulting DataFrame goes back to `llm_service` for natural-language synthesis.
7. The serialised `QueryResponse` reaches the client; React renders all four result panels.

---

## API Reference

### `GET /`
Returns basic service info.

```json
{
  "service": "Road Safety Analytics API",
  "version": "1.0.0",
  "docs": "/docs",
  "status": "running"
}
```

### `GET /health`
Backend health check and dataset summary.

```json
{
  "status": "healthy",
  "total_records": 20002,
  "columns": ["accident_id", "city", "..."],
  "date_range": { "min": "2022-01-01", "max": "2025-05-30" }
}
```

### `GET /api/metadata`
Schema statistics computed at startup.

```json
{
  "total_records": 20002,
  "cities": ["Bangalore", "Chandigarh", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai", "Pune"],
  "categorical_values": {
    "weather": ["clear", "fog", "rain"],
    "accident_severity": ["fatal", "major", "minor"],
    "cause": ["distraction", "drunk driving", "overspeeding", "poor road", "weather"],
    "festival": ["Diwali", "Eid", "Holi", "None"]
  },
  "numeric_stats": {
    "casualties":  { "min": 0.0, "max": 5.0, "mean": 2.15 },
    "risk_score":  { "min": 0.0, "max": 1.0, "mean": 0.48 }
  }
}
```

### `GET /api/audit-log`
Last 50 query operations.

```json
{
  "total_queries": 12,
  "logs": [{
    "timestamp": "2026-06-05T10:41:03+05:30",
    "user_query": "Compare average risk score between Delhi and Mumbai",
    "generated_json": {
      "intent": "compare",
      "metric": "risk_score",
      "aggregation": "mean",
      "compare_values": ["Delhi", "Mumbai"],
      "compare_column": "city"
    },
    "result_summary": "2 rows returned"
  }]
}
```

### `POST /api/query`
Main analytics pipeline.

**Request**
```json
{ "question": "Top 5 cities with the highest casualties" }
```
Min 3 chars · Max 500 chars

**Response `200`**
```json
{
  "answer": "The top 5 cities with the highest casualties are Delhi, Bangalore, Mumbai, Chennai, and Kolkata...",
  "operation_description": "Computed sum(casualties) grouped by city",
  "query_json": {
    "intent": "top_n",
    "metric": "casualties",
    "group_by": "city",
    "aggregation": "sum",
    "top_n": 5,
    "sort_order": "desc"
  },
  "result_table": [
    { "city": "Delhi",     "casualties_sum": 6120 },
    { "city": "Bangalore", "casualties_sum": 5890 }
  ]
}
```

**Error responses**

| Status | Reason | `detail.reason` |
|---|---|---|
| `400` | Invalid column, uncorrectable category | `"Cannot group by 'unknown_column'"` |
| `408` | Pipeline exceeded 60-second limit | `"Pipeline timeout"` |
| `500` | Unexpected model or engine error | Traceback / error description |
```
