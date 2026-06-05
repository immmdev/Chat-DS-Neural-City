const BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://neural-city.onrender.com";

// ── Simple in-memory cache ──
const cache = new Map();

/**
 * Send a natural-language question to the backend.
 * Returns a QueryResponse or throws an error.
 *
 * @param {string} question
 * @param {{ signal?: AbortSignal }} options
 * @returns {Promise<import('./types').QueryResponse>}
 */
export async function askQuestion(question, { signal } = {}) {
  const cacheKey = question.trim().toLowerCase();

  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  const res = await fetch(`${BASE_URL}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
    signal,
  });

  if (!res.ok) {
    let errBody;
    try {
      errBody = await res.json();
    } catch {
      errBody = { answer: `HTTP ${res.status}: ${res.statusText}` };
    }
    const err = new Error(errBody?.detail?.answer || errBody?.answer || "Request failed");
    err.status = res.status;
    err.detail = errBody;
    throw err;
  }

  const data = await res.json();
  cache.set(cacheKey, data);
  return data;
}

/**
 * Fetch dataset metadata from /api/metadata.
 */
export async function fetchMetadata() {
  const res = await fetch(`${BASE_URL}/api/metadata`);
  if (!res.ok) throw new Error("Failed to fetch metadata");
  return res.json();
}

/**
 * Fetch health status from /health.
 */
export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error("Failed to fetch health");
  return res.json();
}

/**
 * Clear the query cache (useful for testing / refresh).
 */
export function clearCache() {
  cache.clear();
}
