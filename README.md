<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Neural City — Indian Road Accident Analytics</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0a0b0d;
    --bg2: #0f1115;
    --bg3: #14161c;
    --surface: #181b22;
    --surface2: #1e2229;
    --border: rgba(255,255,255,0.06);
    --border2: rgba(255,255,255,0.12);
    --text: #e8eaf0;
    --text2: #8b90a0;
    --text3: #5a5f70;
    --accent: #4f8ef7;
    --accent2: #6ea8ff;
    --accent-dim: rgba(79,142,247,0.12);
    --accent-glow: rgba(79,142,247,0.25);
    --green: #3ecf8e;
    --green-dim: rgba(62,207,142,0.1);
    --amber: #f59e0b;
    --amber-dim: rgba(245,158,11,0.1);
    --red: #f87171;
    --red-dim: rgba(248,113,113,0.1);
    --purple: #a78bfa;
    --purple-dim: rgba(167,139,250,0.1);
    --cyan: #22d3ee;
    --cyan-dim: rgba(34,211,238,0.1);
    --font-display: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.75;
    min-height: 100vh;
  }

  /* ── LAYOUT ── */
  .page {
    display: grid;
    grid-template-columns: 240px 1fr;
    min-height: 100vh;
  }

  /* ── SIDEBAR ── */
  .sidebar {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    background: var(--bg2);
    border-right: 1px solid var(--border);
    padding: 2rem 0;
    display: flex;
    flex-direction: column;
    gap: 0;
    scrollbar-width: thin;
    scrollbar-color: var(--border2) transparent;
  }

  .sidebar-logo {
    padding: 0 1.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.25rem;
  }

  .sidebar-logo .wordmark {
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .sidebar-logo .sub {
    font-size: 11px;
    color: var(--text3);
    margin-top: 2px;
    font-family: var(--font-mono);
    letter-spacing: 0.03em;
  }

  .sidebar-section-label {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text3);
    padding: 0.75rem 1.5rem 0.4rem;
  }

  .sidebar-link {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.45rem 1.5rem;
    font-size: 13px;
    color: var(--text2);
    text-decoration: none;
    transition: all 0.15s;
    border-left: 2px solid transparent;
  }

  .sidebar-link:hover {
    color: var(--text);
    background: rgba(255,255,255,0.03);
    border-left-color: var(--border2);
  }

  .sidebar-link.active {
    color: var(--accent2);
    border-left-color: var(--accent);
    background: var(--accent-dim);
  }

  .sidebar-link .dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.5;
    flex-shrink: 0;
  }

  /* ── MAIN CONTENT ── */
  .main {
    min-width: 0;
    padding: 3.5rem 4rem 6rem;
    max-width: 900px;
  }

  /* ── HERO ── */
  .hero {
    margin-bottom: 4rem;
    padding-bottom: 3rem;
    border-bottom: 1px solid var(--border);
  }

  .hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .hero-eyebrow::before {
    content: '';
    display: block;
    width: 24px;
    height: 1px;
    background: var(--accent);
  }

  .hero-title {
    font-family: var(--font-display);
    font-size: clamp(2.4rem, 4vw, 3.6rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 1.25rem;
  }

  .hero-title span {
    background: linear-gradient(135deg, var(--accent2) 0%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-desc {
    font-size: 16px;
    color: var(--text2);
    max-width: 600px;
    line-height: 1.8;
    margin-bottom: 2rem;
  }

  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .badge {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 400;
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid;
    letter-spacing: 0.03em;
  }

  .badge-blue  { color: var(--accent2); border-color: rgba(110,168,255,0.25); background: rgba(79,142,247,0.07); }
  .badge-green { color: var(--green);   border-color: rgba(62,207,142,0.25);  background: rgba(62,207,142,0.07); }
  .badge-amber { color: var(--amber);   border-color: rgba(245,158,11,0.25);  background: rgba(245,158,11,0.07); }
  .badge-purple{ color: var(--purple);  border-color: rgba(167,139,250,0.25); background: rgba(167,139,250,0.07); }
  .badge-cyan  { color: var(--cyan);    border-color: rgba(34,211,238,0.25);  background: rgba(34,211,238,0.07); }

  /* ── SECTION HEADERS ── */
  .section { margin-bottom: 3.5rem; }

  .section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.75rem;
  }

  .section-num {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text3);
    font-weight: 400;
    letter-spacing: 0.06em;
    white-space: nowrap;
  }

  .section-title {
    font-family: var(--font-display);
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
  }

  .section-divider {
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  h3 {
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.9rem;
    margin-top: 1.75rem;
    letter-spacing: -0.01em;
  }

  p {
    color: var(--text2);
    margin-bottom: 1rem;
    font-size: 14.5px;
    line-height: 1.8;
  }

  /* ── TABLE ── */
  .table-wrap {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  thead tr {
    background: var(--surface);
    border-bottom: 1px solid var(--border2);
  }

  thead th {
    padding: 10px 16px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text3);
    text-align: left;
    white-space: nowrap;
  }

  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
  }

  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: rgba(255,255,255,0.015); }

  tbody td {
    padding: 10px 16px;
    color: var(--text2);
    vertical-align: top;
    line-height: 1.55;
  }

  tbody td:first-child {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--cyan);
    white-space: nowrap;
  }

  .td-type {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--green);
    white-space: nowrap;
  }

  .td-sample {
    font-family: var(--font-mono);
    font-size: 11.5px;
    color: var(--text3);
  }

  /* ── CODE BLOCKS ── */
  .code-block {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 1.25rem;
    overflow: hidden;
  }

  .code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
  }

  .code-lang {
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text3);
  }

  .code-dots { display: flex; gap: 6px; }
  .code-dot  { width: 8px; height: 8px; border-radius: 50%; background: var(--border2); }

  pre {
    padding: 1.25rem 1.5rem;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 12.5px;
    line-height: 1.7;
    color: var(--text2);
    scrollbar-width: thin;
    scrollbar-color: var(--border2) transparent;
  }

  .kw  { color: var(--purple); }
  .str { color: var(--green); }
  .num { color: var(--amber); }
  .cmt { color: var(--text3); font-style: italic; }
  .key { color: var(--cyan); }
  .val { color: var(--accent2); }

  /* ── CALL-OUT CARDS ── */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 1.5rem;
  }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    transition: border-color 0.2s, background 0.2s;
  }

  .card:hover {
    border-color: var(--border2);
    background: var(--surface2);
  }

  .card-label {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  .card-value {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.2;
    color: var(--text);
  }

  .card-sub {
    font-size: 12px;
    color: var(--text3);
    margin-top: 4px;
    font-family: var(--font-mono);
  }

  /* ── FLOW DIAGRAM ── */
  .flow-diagram {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    overflow-x: auto;
  }

  /* ── FILE LIST ── */
  .file-list {
    display: flex;
    flex-direction: column;
    gap: 0;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.25rem;
  }

  .file-item {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 16px;
    padding: 11px 16px;
    border-bottom: 1px solid var(--border);
    transition: background 0.12s;
    align-items: start;
  }

  .file-item:last-child { border-bottom: none; }
  .file-item:hover { background: rgba(255,255,255,0.015); }

  .file-name {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--accent2);
    line-height: 1.5;
  }

  .file-desc {
    font-size: 13px;
    color: var(--text2);
    line-height: 1.55;
  }

  /* ── API ENDPOINTS ── */
  .endpoint {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1rem;
  }

  .endpoint-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
  }

  .method {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    flex-shrink: 0;
  }

  .method-get  { background: rgba(62,207,142,0.15); color: var(--green); }
  .method-post { background: rgba(79,142,247,0.15); color: var(--accent2); }

  .endpoint-path {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--text);
    font-weight: 400;
  }

  .endpoint-summary {
    font-size: 12px;
    color: var(--text3);
    margin-left: auto;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .endpoint-body {
    padding: 0;
    background: var(--bg2);
  }

  .endpoint-body pre {
    padding: 1rem 1.25rem;
    font-size: 12px;
  }

  /* ── STATUS PILLS ── */
  .status-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }

  .status-pill {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.04em;
  }

  .status-200 { background: rgba(62,207,142,0.12); color: var(--green); border: 1px solid rgba(62,207,142,0.25); }
  .status-400 { background: rgba(245,158,11,0.12); color: var(--amber); border: 1px solid rgba(245,158,11,0.25); }
  .status-408 { background: rgba(248,113,113,0.12); color: var(--red);   border: 1px solid rgba(248,113,113,0.25); }
  .status-500 { background: rgba(248,113,113,0.12); color: var(--red);   border: 1px solid rgba(248,113,113,0.25); }

  /* ── DATA FLOW SVG WRAPPER ── */
  .flow-svg-wrap { overflow-x: auto; }

  /* ── INLINE CODE ── */
  code {
    font-family: var(--font-mono);
    font-size: 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 6px;
    color: var(--cyan);
  }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

  /* ── TECH STACK CHIPS ── */
  .tech-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 1.5rem;
  }

  .tech-chip {
    display: flex;
    align-items: center;
    gap: 7px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--text2);
    transition: border-color 0.15s;
  }

  .tech-chip:hover { border-color: var(--border2); }

  .tech-chip .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  /* ── DIVIDER ── */
  hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.5rem 0;
  }

  /* ── INFO BOX ── */
  .info-box {
    border-left: 3px solid var(--accent);
    background: var(--accent-dim);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    font-size: 13.5px;
    color: var(--text2);
    line-height: 1.7;
  }

  .info-box strong {
    color: var(--accent2);
    font-weight: 500;
  }

  /* PRINT */
  @media print {
    .sidebar { display: none; }
    .page { grid-template-columns: 1fr; }
    .main { padding: 2rem; }
  }
</style>
</head>
<body>
<div class="page">

  <!-- SIDEBAR -->
  <nav class="sidebar">
    <div class="sidebar-logo">
      <div class="wordmark">Neural City</div>
      <div class="sub">Road Analytics v1.0.0</div>
    </div>

    <div class="sidebar-section-label">Overview</div>
    <a class="sidebar-link active" href="#overview"><span class="dot"></span>Introduction</a>
    <a class="sidebar-link" href="#dataset"><span class="dot"></span>Dataset</a>
    <a class="sidebar-link" href="#schema"><span class="dot"></span>Schema</a>

    <div class="sidebar-section-label">Architecture</div>
    <a class="sidebar-link" href="#client"><span class="dot"></span>Client</a>
    <a class="sidebar-link" href="#server"><span class="dot"></span>Server</a>
    <a class="sidebar-link" href="#dataflow"><span class="dot"></span>Data Flow</a>

    <div class="sidebar-section-label">Reference</div>
    <a class="sidebar-link" href="#api"><span class="dot"></span>API Endpoints</a>
    <a class="sidebar-link" href="#errors"><span class="dot"></span>Error Codes</a>
  </nav>

  <!-- MAIN -->
  <main class="main">

    <!-- HERO -->
    <section class="hero" id="overview">
      <div class="hero-eyebrow">Documentation</div>
      <h1 class="hero-title">Neural City<br><span>Road Accident Analytics</span></h1>
      <p class="hero-desc">
        An AI-powered conversational analytics platform for the Indian Road Accident Dataset (2022–2025). Submit natural-language questions, receive structured query plans, Pandas execution results, and dynamic chart visualizations — all in one unified interface.
      </p>
      <div class="badge-row">
        <span class="badge badge-blue">React 19</span>
        <span class="badge badge-green">FastAPI</span>
        <span class="badge badge-amber">Pandas</span>
        <span class="badge badge-purple">Gemini 2.5 Flash</span>
        <span class="badge badge-cyan">Recharts 3.8.1</span>
        <span class="badge badge-blue">LangChain</span>
        <span class="badge badge-green">Python</span>
        <span class="badge badge-amber">TailwindCSS v4</span>
      </div>
    </section>

    <!-- DATASET -->
    <section class="section" id="dataset">
      <div class="section-header">
        <span class="section-num">01</span>
        <h2 class="section-title">Dataset</h2>
        <div class="section-divider"></div>
      </div>

      <div class="card-grid">
        <div class="card">
          <div class="card-label" style="color:var(--accent)">Records</div>
          <div class="card-value">20,002</div>
          <div class="card-sub">accident_id 0 → 20001</div>
        </div>
        <div class="card">
          <div class="card-label" style="color:var(--green)">Columns</div>
          <div class="card-value">24</div>
          <div class="card-sub">spatial · temporal · env · risk</div>
        </div>
        <div class="card">
          <div class="card-label" style="color:var(--amber)">Date Range</div>
          <div class="card-value" style="font-size:1.1rem;padding-top:4px">2022 – 2025</div>
          <div class="card-sub">Jan 2022 → May 2025</div>
        </div>
        <div class="card">
          <div class="card-label" style="color:var(--purple)">Cities</div>
          <div class="card-value">8</div>
          <div class="card-sub">across 7 Indian states</div>
        </div>
      </div>

      <div class="info-box">
        <strong>Location:</strong> The unified dataset lives at <code>Server/indian_roads_dataset.csv</code>. The client does not maintain a local copy — it fetches schema metadata dynamically from <code>GET /api/metadata</code> to align suggestions, constraints, and valid ranges with the server at runtime.
      </div>

      <p>The dataset captures accident records enriched with environmental, temporal, and infrastructure context. A computed <strong>risk_score</strong> (0–1) synthesises traffic density, weather severity, visibility, and time-of-day factors into a single hazard proxy.</p>
    </section>

    <!-- SCHEMA -->
    <section class="section" id="schema">
      <div class="section-header">
        <span class="section-num">02</span>
        <h2 class="section-title">Column Schema</h2>
        <div class="section-divider"></div>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Column</th>
              <th>Type</th>
              <th>Description</th>
              <th>Sample / Allowed Values</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>accident_id</td><td class="td-type">int64</td><td>Unique record identifier</td><td class="td-sample">0, 1, 2 …</td></tr>
            <tr><td>city</td><td class="td-type">object</td><td>Major Indian city</td><td class="td-sample">Bangalore, Delhi, Mumbai …</td></tr>
            <tr><td>state</td><td class="td-type">object</td><td>State of the city</td><td class="td-sample">Karnataka, Maharashtra …</td></tr>
            <tr><td>latitude</td><td class="td-type">float64</td><td>Geospatial latitude</td><td class="td-sample">18.68, 28.80</td></tr>
            <tr><td>longitude</td><td class="td-type">float64</td><td>Geospatial longitude</td><td class="td-sample">73.93, 77.05</td></tr>
            <tr><td>date</td><td class="td-type">object</td><td>Accident date (YYYY-MM-DD)</td><td class="td-sample">2023-10-22</td></tr>
            <tr><td>time</td><td class="td-type">object</td><td>Time of accident (HH:MM)</td><td class="td-sample">5:00, 16:00</td></tr>
            <tr><td>hour</td><td class="td-type">int64</td><td>Extracted hour (0–23)</td><td class="td-sample">0, 8, 13, 23</td></tr>
            <tr><td>day_of_week</td><td class="td-type">object</td><td>Day name</td><td class="td-sample">Monday … Sunday</td></tr>
            <tr><td>is_weekend</td><td class="td-type">int64</td><td>Weekend flag</td><td class="td-sample">0 = Weekday, 1 = Weekend</td></tr>
            <tr><td>road_type</td><td class="td-type">object</td><td>Road infrastructure class</td><td class="td-sample">highway, rural, urban</td></tr>
            <tr><td>lanes</td><td class="td-type">int64</td><td>Lane count</td><td class="td-sample">1 – 6</td></tr>
            <tr><td>traffic_signal</td><td class="td-type">int64</td><td>Signal presence</td><td class="td-sample">0 = No, 1 = Yes</td></tr>
            <tr><td>weather</td><td class="td-type">object</td><td>Weather conditions</td><td class="td-sample">clear, fog, rain</td></tr>
            <tr><td>visibility</td><td class="td-type">object</td><td>Visibility level</td><td class="td-sample">low, medium, high</td></tr>
            <tr><td>temperature</td><td class="td-type">int64</td><td>Temperature (°C)</td><td class="td-sample">15 – 40</td></tr>
            <tr><td>traffic_density</td><td class="td-type">object</td><td>Traffic density level</td><td class="td-sample">low, medium, high</td></tr>
            <tr><td>cause</td><td class="td-type">object</td><td>Primary accident cause</td><td class="td-sample">distraction, overspeeding …</td></tr>
            <tr><td>accident_severity</td><td class="td-type">object</td><td>Severity outcome</td><td class="td-sample">fatal, major, minor</td></tr>
            <tr><td>vehicles_involved</td><td class="td-type">int64</td><td>Vehicle count in collision</td><td class="td-sample">1 – 5</td></tr>
            <tr><td>casualties</td><td class="td-type">int64</td><td>Injuries / deaths</td><td class="td-sample">0 – 5</td></tr>
            <tr><td>is_peak_hour</td><td class="td-type">int64</td><td>Peak traffic flag</td><td class="td-sample">0 = No, 1 = Yes</td></tr>
            <tr><td>festival</td><td class="td-type">object</td><td>Holiday context</td><td class="td-sample">Diwali, Eid, Holi, None</td></tr>
            <tr><td>risk_score</td><td class="td-type">float64</td><td>Engineered hazard score</td><td class="td-sample">0.0 – 1.0</td></tr>
          </tbody>
        </table>
      </div>

      <h3>Engineered Features</h3>
      <p>Four temporal columns — <code>hour</code>, <code>day_of_week</code>, <code>is_weekend</code>, <code>is_peak_hour</code> — are extracted from the raw timestamp to support time-series and peak-period queries without in-query parsing. The <code>risk_score</code> is a composite: higher values (approaching 1.0) cluster around fog, low visibility, peak hours, and highway conditions.</p>
    </section>

    <!-- CLIENT -->
    <section class="section" id="client">
      <div class="section-header">
        <span class="section-num">03</span>
        <h2 class="section-title">Client Architecture</h2>
        <div class="section-divider"></div>
      </div>

      <p>A responsive single-page application built on React 19 with Vite. All state flows through a single custom hook; charts are auto-selected from the query result shape without user configuration.</p>

      <h3>Tech Stack</h3>
      <div class="tech-grid">
        <div class="tech-chip"><span class="dot" style="background:var(--accent)"></span>React 19 + Vite</div>
        <div class="tech-chip"><span class="dot" style="background:var(--cyan)"></span>TailwindCSS v4</div>
        <div class="tech-chip"><span class="dot" style="background:var(--green)"></span>Recharts 3.8.1</div>
        <div class="tech-chip"><span class="dot" style="background:var(--amber)"></span>Lucide React</div>
        <div class="tech-chip"><span class="dot" style="background:var(--purple)"></span>React Markdown + remark-gfm</div>
      </div>

      <h3>File Structure</h3>
      <div class="file-list">
        <div class="file-item" style="background:var(--surface);border-bottom:1px solid var(--border2)">
          <div class="file-name" style="color:var(--text3);font-size:10px;letter-spacing:0.08em;text-transform:uppercase">Client /</div>
          <div></div>
        </div>
        <div class="file-item"><div class="file-name">App.jsx</div><div class="file-desc">Root layout coordinator. Manages view composition (Navbar, HeroSection, SearchBar, SuggestionChips, ResultSection), runs health checks on load, and auto-scrolls to results.</div></div>
        <div class="file-item"><div class="file-name">components/Navbar.jsx</div><div class="file-desc">Branding bar with live green/red server connection indicator.</div></div>
        <div class="file-item"><div class="file-name">components/HeroSection.jsx</div><div class="file-desc">Welcome header with smooth-scroll action to the query workspace.</div></div>
        <div class="file-item"><div class="file-name">components/SearchBar.jsx</div><div class="file-desc">Text input with Enter-key and button submission; disabled states during in-flight queries.</div></div>
        <div class="file-item"><div class="file-name">components/SuggestionChips.jsx</div><div class="file-desc">Clickable seed questions providing one-tap query execution examples.</div></div>
        <div class="file-item"><div class="file-name">components/LoadingState.jsx</div><div class="file-desc">Animated skeleton loader with contextual phase feedback.</div></div>
        <div class="file-item"><div class="file-name">components/ErrorCard.jsx</div><div class="file-desc">Displays structured API error details with a retry action.</div></div>
        <div class="file-item"><div class="file-name">components/ResultSection.jsx</div><div class="file-desc">Hosts the four result panels: Answer, Chart, Table, Debugger.</div></div>
        <div class="file-item"><div class="file-name">components/AnswerCard.jsx</div><div class="file-desc">Renders the LLM-synthesised answer from markdown (with GFM tables).</div></div>
        <div class="file-item"><div class="file-name">components/ChartPanel.jsx</div><div class="file-desc">Infers and renders the best Recharts visualisation from result shape. See Visualisation Logic below.</div></div>
        <div class="file-item"><div class="file-name">components/ResultTable.jsx</div><div class="file-desc">Scrollable, paginated raw data table.</div></div>
        <div class="file-item"><div class="file-name">components/QueryDebugPanel.jsx</div><div class="file-desc">Collapsible panel showing the raw structured query JSON from Gemini.</div></div>
        <div class="file-item"><div class="file-name">hooks/useQuery.js</div><div class="file-desc">Encapsulates query state, submission handlers, and in-flight cancellation via AbortController.</div></div>
        <div class="file-item"><div class="file-name">api/queryApi.js</div><div class="file-desc">REST layer with in-memory request cache to prevent redundant calls.</div></div>
      </div>

      <h3>Visualisation Inference Logic</h3>
      <p><code>ChartPanel.jsx</code> selects the chart type automatically based on result shape — no user configuration required:</p>
      <div class="card-grid" style="grid-template-columns: repeat(3,1fr)">
        <div class="card">
          <div class="card-label" style="color:var(--cyan)">Area Chart</div>
          <div style="font-size:13px;color:var(--text2);margin-top:6px">Result contains a temporal field (e.g. <code>hour</code>) alongside numeric values.</div>
        </div>
        <div class="card">
          <div class="card-label" style="color:var(--purple)">Pie Chart</div>
          <div style="font-size:13px;color:var(--text2);margin-top:6px">Fewer than 9 rows, exactly one string category column, exactly one numeric value column.</div>
        </div>
        <div class="card">
          <div class="card-label" style="color:var(--green)">Bar Chart</div>
          <div style="font-size:13px;color:var(--text2);margin-top:6px">Default fallback for comparisons, aggregations, and top-n result sets.</div>
        </div>
      </div>
    </section>

    <!-- SERVER -->
    <section class="section" id="server">
      <div class="section-header">
        <span class="section-num">04</span>
        <h2 class="section-title">Server Architecture</h2>
        <div class="section-divider"></div>
      </div>

      <p>A FastAPI backend that loads the dataset into memory at startup, translates natural-language queries via Gemini, validates and sanitises the structured output, then executes safe Pandas operations without ever calling <code>eval()</code> or <code>exec()</code>.</p>

      <h3>Tech Stack</h3>
      <div class="tech-grid">
        <div class="tech-chip"><span class="dot" style="background:var(--green)"></span>FastAPI + Uvicorn</div>
        <div class="tech-chip"><span class="dot" style="background:var(--purple)"></span>Gemini 2.5 Flash</div>
        <div class="tech-chip"><span class="dot" style="background:var(--amber)"></span>LangChain + LangChain Google GenAI</div>
        <div class="tech-chip"><span class="dot" style="background:var(--cyan)"></span>Pandas</div>
        <div class="tech-chip"><span class="dot" style="background:var(--accent)"></span>Python-Dotenv + Pydantic</div>
      </div>

      <h3>File Structure</h3>
      <div class="file-list">
        <div class="file-item" style="background:var(--surface);border-bottom:1px solid var(--border2)">
          <div class="file-name" style="color:var(--text3);font-size:10px;letter-spacing:0.08em;text-transform:uppercase">Server /</div>
          <div></div>
        </div>
        <div class="file-item"><div class="file-name">app.py</div><div class="file-desc">Entry point. Controls startup lifespan, loads the dataset, instantiates services, configures CORS, and binds routing endpoints.</div></div>
        <div class="file-item"><div class="file-name">routes/query_routes.py</div><div class="file-desc">Query entry point. Wraps execution in an async timeout handler (60 s cap) and appends each query to the audit log.</div></div>
        <div class="file-item"><div class="file-name">schemas/query_schema.py</div><div class="file-desc">Pydantic definitions for <code>UserQueryRequest</code> (min 3 / max 500 chars) and <code>StructuredQuery</code> output from the LLM.</div></div>
        <div class="file-item"><div class="file-name">schemas/response_schema.py</div><div class="file-desc">Validation rules for endpoint response data structures.</div></div>
        <div class="file-item"><div class="file-name">services/llm_service.py</div><div class="file-desc">Generates the structured query JSON from natural language via Gemini; synthesises the final natural-language answer from the result DataFrame.</div></div>
        <div class="file-item"><div class="file-name">services/validation_service.py</div><div class="file-desc">Inspects generated JSON against schema constraints; fuzzy-matches misspelled city names or parameter values; rejects out-of-scope requests with descriptive errors.</div></div>
        <div class="file-item"><div class="file-name">services/pandas_engine.py</div><div class="file-desc">Safe query executor. Routes by intent (aggregate, compare, trend, top_n, distribution, filter) to dedicated Pandas methods — no eval / exec.</div></div>
        <div class="file-item"><div class="file-name">services/answer_service.py</div><div class="file-desc">Local fallback answer formatter invoked when LLM generation fails or times out.</div></div>
        <div class="file-item"><div class="file-name">utils/metadata.py</div><div class="file-desc">Computes ranges, categorical values, and numeric statistics from the dataset at startup; passes them as LLM prompt context.</div></div>
        <div class="file-item"><div class="file-name">utils/constants.py</div><div class="file-desc">Whitelists of allowed columns, query intents, and aggregation methods that secure the pipeline against injection.</div></div>
      </div>
    </section>

    <!-- DATA FLOW -->
    <section class="section" id="dataflow">
      <div class="section-header">
        <span class="section-num">05</span>
        <h2 class="section-title">Data Flow</h2>
        <div class="section-divider"></div>
      </div>

      <p>Each query traverses three layers — Client, FastAPI Router, and Service Layer — before results stream back to the React renderer. The numbered steps below map to the diagram.</p>

      <div class="flow-diagram">
        <svg width="100%" viewBox="0 0 820 600" xmlns="http://www.w3.org/2000/svg" style="min-width:700px">
          <defs>
            <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </marker>
          </defs>

          <!-- CLIENT GROUP -->
          <rect x="20" y="20" width="230" height="370" rx="10" fill="rgba(79,142,247,0.04)" stroke="rgba(79,142,247,0.2)" stroke-width="1"/>
          <text x="35" y="42" font-family="DM Mono,monospace" font-size="10" fill="rgba(110,168,255,0.7)" font-weight="500" letter-spacing="0.1em">CLIENT</text>

          <!-- Client boxes -->
          <rect x="40" y="55" width="190" height="38" rx="7" fill="#1a2035" stroke="rgba(79,142,247,0.3)" stroke-width="0.75"/>
          <text x="135" y="79" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">SearchBar / Suggestions</text>

          <rect x="40" y="120" width="190" height="38" rx="7" fill="#1a2035" stroke="rgba(79,142,247,0.3)" stroke-width="0.75"/>
          <text x="135" y="144" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">useQuery Hook</text>

          <rect x="40" y="185" width="190" height="38" rx="7" fill="#1a2035" stroke="rgba(79,142,247,0.3)" stroke-width="0.75"/>
          <text x="135" y="209" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">queryApi Client</text>

          <rect x="40" y="315" width="190" height="38" rx="7" fill="#1a2035" stroke="rgba(110,168,255,0.4)" stroke-width="0.75"/>
          <text x="135" y="339" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">Render Components</text>

          <!-- Renderer sub-labels -->
          <text x="48" y="367" font-family="DM Mono,monospace" font-size="9.5" fill="rgba(110,168,255,0.55)">AnswerCard  ChartPanel  ResultTable  QueryDebugPanel</text>

          <!-- Client arrows -->
          <line x1="135" y1="93" x2="135" y2="118" stroke="rgba(79,142,247,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="148" y="110" font-family="DM Mono,monospace" font-size="9" fill="rgba(79,142,247,0.6)">1. submit</text>

          <line x1="135" y1="158" x2="135" y2="183" stroke="rgba(79,142,247,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="148" y="176" font-family="DM Mono,monospace" font-size="9" fill="rgba(79,142,247,0.6)">2. cancel / fetch</text>

          <!-- React state update (right side) -->
          <path d="M230 204 Q270 270 230 330" fill="none" stroke="rgba(79,142,247,0.35)" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>
          <text x="256" y="275" font-family="DM Mono,monospace" font-size="9" fill="rgba(79,142,247,0.5)">11. state</text>

          <!-- ROUTER GROUP -->
          <rect x="290" y="20" width="215" height="175" rx="10" fill="rgba(62,207,142,0.04)" stroke="rgba(62,207,142,0.2)" stroke-width="1"/>
          <text x="305" y="42" font-family="DM Mono,monospace" font-size="10" fill="rgba(62,207,142,0.7)" font-weight="500" letter-spacing="0.1em">FASTAPI ROUTER</text>

          <rect x="310" y="55" width="175" height="38" rx="7" fill="#101c18" stroke="rgba(62,207,142,0.35)" stroke-width="0.75"/>
          <text x="397" y="79" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">process_query</text>

          <rect x="310" y="120" width="175" height="38" rx="7" fill="#101c18" stroke="rgba(62,207,142,0.35)" stroke-width="0.75"/>
          <text x="397" y="144" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">llm_service</text>

          <!-- CLIENT -> ROUTER -->
          <line x1="232" y1="199" x2="308" y2="76" stroke="rgba(110,168,255,0.45)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="258" y="148" font-family="DM Mono,monospace" font-size="9" fill="rgba(110,168,255,0.6)">3. POST /api/query</text>

          <line x1="397" y1="93" x2="397" y2="118" stroke="rgba(62,207,142,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="410" y="112" font-family="DM Mono,monospace" font-size="9" fill="rgba(62,207,142,0.6)">4. lifespan state</text>

          <!-- SERVICE GROUP -->
          <rect x="555" y="20" width="245" height="480" rx="10" fill="rgba(167,139,250,0.04)" stroke="rgba(167,139,250,0.2)" stroke-width="1"/>
          <text x="570" y="42" font-family="DM Mono,monospace" font-size="10" fill="rgba(167,139,250,0.7)" font-weight="500" letter-spacing="0.1em">SERVICE LAYER</text>

          <!-- Gemini -->
          <rect x="575" y="55" width="205" height="38" rx="7" fill="#1c1630" stroke="rgba(167,139,250,0.4)" stroke-width="0.75"/>
          <text x="677" y="79" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">Gemini 2.5 Flash</text>

          <!-- Validation -->
          <rect x="575" y="130" width="205" height="38" rx="7" fill="#1c1630" stroke="rgba(167,139,250,0.3)" stroke-width="0.75"/>
          <text x="677" y="154" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">validation_service</text>

          <!-- Pandas engine -->
          <rect x="575" y="210" width="205" height="38" rx="7" fill="#1c1630" stroke="rgba(245,158,11,0.35)" stroke-width="0.75"/>
          <text x="677" y="234" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">pandas_engine</text>

          <!-- CSV -->
          <rect x="575" y="290" width="205" height="38" rx="7" fill="#1c1a10" stroke="rgba(245,158,11,0.4)" stroke-width="0.75"/>
          <text x="677" y="314" text-anchor="middle" font-family="DM Mono,monospace" font-size="11.5" fill="#f59e0b">indian_roads_dataset.csv</text>

          <!-- LLM synth answer -->
          <rect x="575" y="370" width="205" height="38" rx="7" fill="#1c1630" stroke="rgba(167,139,250,0.3)" stroke-width="0.75"/>
          <text x="677" y="394" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="12" fill="#e8eaf0">Synthesise answer</text>

          <!-- Service arrows -->
          <!-- router -> gemini -->
          <line x1="485" y1="139" x2="573" y2="74" stroke="rgba(167,139,250,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="509" y="115" font-family="DM Mono,monospace" font-size="9" fill="rgba(167,139,250,0.6)">5. prompt</text>

          <!-- gemini response -->
          <line x1="677" y1="93" x2="677" y2="128" stroke="rgba(167,139,250,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="690" y="117" font-family="DM Mono,monospace" font-size="9" fill="rgba(167,139,250,0.6)">6. JSON</text>

          <!-- validation -> pandas -->
          <line x1="677" y1="168" x2="677" y2="208" stroke="rgba(167,139,250,0.4)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="690" y="195" font-family="DM Mono,monospace" font-size="9" fill="rgba(167,139,250,0.55)">7. clean query</text>

          <!-- pandas -> csv -->
          <line x1="677" y1="248" x2="677" y2="288" stroke="rgba(245,158,11,0.5)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="690" y="275" font-family="DM Mono,monospace" font-size="9" fill="rgba(245,158,11,0.65)">8. run Pandas</text>

          <!-- csv -> pandas (return) -->
          <line x1="640" y1="288" x2="640" y2="250" stroke="rgba(245,158,11,0.35)" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#arr)"/>

          <!-- pandas -> synth (via router back) -->
          <path d="M677 328 L677 360 L677 368" fill="none" stroke="rgba(167,139,250,0.4)" stroke-width="1.2" marker-end="url(#arr)"/>
          <text x="690" y="352" font-family="DM Mono,monospace" font-size="9" fill="rgba(167,139,250,0.55)">9. DataFrame</text>

          <!-- synth -> router response -->
          <path d="M575 389 L500 389 L500 155 L487 155" fill="none" stroke="rgba(62,207,142,0.4)" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>
          <text x="502" y="382" font-family="DM Mono,monospace" font-size="9" fill="rgba(62,207,142,0.6)">10. answer</text>

          <!-- router -> client (serialised response) -->
          <path d="M308 155 L260 200" fill="none" stroke="rgba(110,168,255,0.4)" stroke-width="1" stroke-dasharray="4 3" marker-end="url(#arr)"/>
        </svg>
      </div>

      <h3>Step-by-step walkthrough</h3>
      <div class="file-list">
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 1–2</div><div class="file-desc">User submits a question (e.g. "Compare average risk score between Delhi and Mumbai"). The <code>useQuery</code> hook aborts any in-flight request, sets the loading skeleton, and fires a POST via <code>queryApi</code>.</div></div>
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 3–4</div><div class="file-desc">FastAPI router receives <code>POST /api/query</code>. The 60-second async timeout is set; the request passes to <code>llm_service</code> with the lifespan-initialised dataset metadata.</div></div>
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 5–6</div><div class="file-desc">Gemini 2.5 Flash receives the system + user prompt and returns a structured JSON query object specifying intent, metric, aggregation, filters, and group-by columns.</div></div>
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 7</div><div class="file-desc"><code>validation_service</code> maps the JSON to whitelisted columns, fuzzy-corrects city spelling variants, and rejects out-of-scope fields with a descriptive 400 response.</div></div>
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 8–9</div><div class="file-desc"><code>pandas_engine</code> routes by intent to a dedicated method (aggregate, compare, trend, top_n, distribution, filter) and returns the resulting DataFrame — no eval/exec involved.</div></div>
        <div class="file-item"><div class="file-name" style="color:var(--text3);font-size:11px">Step 10–11</div><div class="file-desc">The DataFrame is fed back to <code>llm_service</code> for natural-language synthesis. The router serialises the full <code>QueryResponse</code> and returns it to the client, which updates React state and renders Answer, Chart, Table, and Debug panels.</div></div>
      </div>
    </section>

    <!-- API -->
    <section class="section" id="api">
      <div class="section-header">
        <span class="section-num">06</span>
        <h2 class="section-title">API Reference</h2>
        <div class="section-divider"></div>
      </div>

      <!-- Root -->
      <div class="endpoint">
        <div class="endpoint-header">
          <span class="method method-get">GET</span>
          <span class="endpoint-path">/</span>
          <span class="endpoint-summary">Service info</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="cmt">// Response 200</span>
<span class="key">"service"</span>: <span class="str">"Road Safety Analytics API"</span>
<span class="key">"version"</span>: <span class="str">"1.0.0"</span>
<span class="key">"docs"</span>:    <span class="str">"/docs"</span>
<span class="key">"status"</span>:  <span class="str">"running"</span></pre>
        </div>
      </div>

      <!-- Health -->
      <div class="endpoint">
        <div class="endpoint-header">
          <span class="method method-get">GET</span>
          <span class="endpoint-path">/health</span>
          <span class="endpoint-summary">Backend health + dataset summary</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="cmt">// Response 200</span>
<span class="key">"status"</span>:        <span class="str">"healthy"</span>
<span class="key">"total_records"</span>: <span class="num">20002</span>
<span class="key">"columns"</span>:       <span class="cmt">[ "accident_id", "city", "state", … 24 total ]</span>
<span class="key">"date_range"</span>:    <span class="cmt">{ "min": "2022-01-01", "max": "2025-05-30" }</span></pre>
        </div>
      </div>

      <!-- Metadata -->
      <div class="endpoint">
        <div class="endpoint-header">
          <span class="method method-get">GET</span>
          <span class="endpoint-path">/api/metadata</span>
          <span class="endpoint-summary">Schema statistics (computed at startup)</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="cmt">// Response 200</span>
<span class="key">"total_records"</span>: <span class="num">20002</span>
<span class="key">"cities"</span>:        <span class="cmt">[ "Bangalore", "Chandigarh", "Chennai", "Delhi", … ]</span>
<span class="key">"categorical_values"</span>: {
  <span class="key">"weather"</span>:          <span class="cmt">[ "clear", "fog", "rain" ]</span>
  <span class="key">"accident_severity"</span>: <span class="cmt">[ "fatal", "major", "minor" ]</span>
  <span class="key">"cause"</span>:            <span class="cmt">[ "distraction", "drunk driving", "overspeeding", … ]</span>
}
<span class="key">"numeric_stats"</span>: {
  <span class="key">"risk_score"</span>: <span class="cmt">{ "min": 0.0, "max": 1.0, "mean": 0.48 }</span>
  <span class="key">"casualties"</span>: <span class="cmt">{ "min": 0.0, "max": 5.0, "mean": 2.15 }</span>
}</pre>
        </div>
      </div>

      <!-- Audit log -->
      <div class="endpoint">
        <div class="endpoint-header">
          <span class="method method-get">GET</span>
          <span class="endpoint-path">/api/audit-log</span>
          <span class="endpoint-summary">Last 50 query operations</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="cmt">// Response 200</span>
<span class="key">"total_queries"</span>: <span class="num">12</span>
<span class="key">"logs"</span>: [{
  <span class="key">"timestamp"</span>:     <span class="str">"2026-06-05T10:41:03+05:30"</span>
  <span class="key">"user_query"</span>:    <span class="str">"Compare average risk score between Delhi and Mumbai"</span>
  <span class="key">"generated_json"</span>: {
    <span class="key">"intent"</span>:          <span class="str">"compare"</span>
    <span class="key">"metric"</span>:          <span class="str">"risk_score"</span>
    <span class="key">"aggregation"</span>:     <span class="str">"mean"</span>
    <span class="key">"compare_values"</span>:  <span class="cmt">[ "Delhi", "Mumbai" ]</span>
    <span class="key">"compare_column"</span>:  <span class="str">"city"</span>
  }
  <span class="key">"result_summary"</span>: <span class="str">"2 rows returned"</span>
}]</pre>
        </div>
      </div>

      <!-- POST query -->
      <div class="endpoint">
        <div class="endpoint-header">
          <span class="method method-post">POST</span>
          <span class="endpoint-path">/api/query</span>
          <span class="endpoint-summary">Main analytics pipeline</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="cmt">// Request body</span>
{ <span class="key">"question"</span>: <span class="str">"Top 5 cities with the highest casualties"</span> }
<span class="cmt">// min 3 chars · max 500 chars</span>

<span class="cmt">// Response 200</span>
<span class="key">"answer"</span>:               <span class="str">"The top 5 cities with the highest casualties are …"</span>
<span class="key">"operation_description"</span>: <span class="str">"Computed sum(casualties) grouped by city"</span>
<span class="key">"query_json"</span>: {
  <span class="key">"intent"</span>:      <span class="str">"top_n"</span>
  <span class="key">"metric"</span>:      <span class="str">"casualties"</span>
  <span class="key">"group_by"</span>:    <span class="str">"city"</span>
  <span class="key">"aggregation"</span>: <span class="str">"sum"</span>
  <span class="key">"top_n"</span>:       <span class="num">5</span>
  <span class="key">"sort_order"</span>:  <span class="str">"desc"</span>
}
<span class="key">"result_table"</span>: [
  { <span class="key">"city"</span>: <span class="str">"Delhi"</span>,     <span class="key">"casualties_sum"</span>: <span class="num">6120</span> }
  { <span class="key">"city"</span>: <span class="str">"Bangalore"</span>, <span class="key">"casualties_sum"</span>: <span class="num">5890</span> }
  <span class="cmt">… up to 50 rows</span>
]</pre>
        </div>
      </div>
    </section>

    <!-- ERRORS -->
    <section class="section" id="errors">
      <div class="section-header">
        <span class="section-num">07</span>
        <h2 class="section-title">Error Codes</h2>
        <div class="section-divider"></div>
      </div>

      <div class="status-row">
        <span class="status-pill status-200">200 OK</span>
        <span class="status-pill status-400">400 Bad Request</span>
        <span class="status-pill status-408">408 Timeout</span>
        <span class="status-pill status-500">500 Server Error</span>
      </div>

      <div class="endpoint">
        <div class="endpoint-header">
          <span class="status-pill status-400">400</span>
          <span class="endpoint-path">Invalid or out-of-scope query</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="key">"detail"</span>: {
  <span class="key">"answer"</span>:    <span class="str">"Query validation failed: Cannot group by 'unknown_column'."</span>
  <span class="key">"reason"</span>:    <span class="str">"Cannot group by 'unknown_column'"</span>
  <span class="key">"query_json"</span>: { <span class="key">"intent"</span>: <span class="str">"aggregate"</span>, <span class="key">"group_by"</span>: <span class="str">"unknown_column"</span> }
}</pre>
        </div>
      </div>

      <div class="endpoint">
        <div class="endpoint-header">
          <span class="status-pill status-408">408</span>
          <span class="endpoint-path">Pipeline exceeded 60-second timeout</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="key">"detail"</span>: {
  <span class="key">"answer"</span>: <span class="str">"The request took too long. Please try rephrasing your question."</span>
  <span class="key">"reason"</span>: <span class="str">"Pipeline timeout"</span>
}</pre>
        </div>
      </div>

      <div class="endpoint">
        <div class="endpoint-header">
          <span class="status-pill status-500">500</span>
          <span class="endpoint-path">Unexpected model or engine error</span>
        </div>
        <div class="endpoint-body">
          <pre><span class="key">"detail"</span>: {
  <span class="key">"answer"</span>: <span class="str">"An internal error occurred while processing your question."</span>
  <span class="key">"reason"</span>: <span class="str">"Detailed system traceback or error description"</span>
}</pre>
        </div>
      </div>
    </section>

  </main>
</div>

<script>
  const links = document.querySelectorAll('.sidebar-link');
  const sections = document.querySelectorAll('section[id]');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.sidebar-link[href="#${e.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { threshold: 0.35 });

  sections.forEach(s => observer.observe(s));

  links.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
</script>
</body>
</html>
