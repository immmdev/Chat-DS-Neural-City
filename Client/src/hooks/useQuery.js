/**
 * useQuery.js — Custom React hook for managing query state and fetch lifecycle.
 */

import { useState, useCallback, useRef } from "react";
import { askQuestion } from "../api/queryApi";

/**
 * @typedef {Object} UseQueryReturn
 * @property {import('../api/queryApi').QueryResponse|null} data
 * @property {boolean} loading
 * @property {string|null} error
 * @property {string} currentQuestion
 * @property {(question: string) => Promise<void>} submit
 * @property {() => void} reset
 */

export function useQuery() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const abortRef = useRef(null);

  const submit = useCallback(async (question) => {
    if (!question.trim()) return;

    // Cancel any in-flight request
    if (abortRef.current) {
      abortRef.current.abort();
    }

    const controller = new AbortController();
    abortRef.current = controller;

    setCurrentQuestion(question);
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await askQuestion(question, { signal: controller.signal });
      setData(result);
    } catch (err) {
      if (err.name === "AbortError") return;
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    if (abortRef.current) abortRef.current.abort();
    setData(null);
    setError(null);
    setLoading(false);
    setCurrentQuestion("");
  }, []);

  return { data, loading, error, currentQuestion, submit, reset };
}
