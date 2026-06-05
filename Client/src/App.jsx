import { useRef, useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import SearchBar from "./components/SearchBar";
import SuggestionChips from "./components/SuggestionChips";
import LoadingState from "./components/LoadingState";
import ErrorCard from "./components/ErrorCard";
import ResultSection from "./components/ResultSection";
import { useQuery } from "./hooks/useQuery";
import { DEFAULT_QUESTIONS } from "./constants/questions";
import { fetchHealth } from "./api/queryApi";

const HERO_BG ="hero.jpg"

export default function App() {
  const searchRef = useRef(null);
  const [healthy, setHealthy] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const { data, loading, error, currentQuestion, submit, reset } = useQuery();

  // ── Health check ──────────────────────────────────────────────────────────
  useEffect(() => {
    fetchHealth()
      .then(() => setHealthy(true))
      .catch(() => setHealthy(false));
  }, []);

  // Auto-scroll to search section after submitting 
  useEffect(() => {
    if (loading || data) {
      searchRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [loading, data]);

  function handleSuggestion(question) {
    setInputValue(question);
    submit(question);
    searchRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function handleReset() {
    reset();
    setInputValue("");
    searchRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <div className="min-h-screen" >
      {/* ── Top Navigation ──────────────────────────────────────────────── */}
      <Navbar healthy={healthy} />

      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <HeroSection
        heroBgUrl={HERO_BG}
        onScrollToSearch={() =>
          searchRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
        }
      />

      {/* ── Search + Results Section ─────────────────────────────────────── */}
      <section
        ref={searchRef}
        id="search-section"
        className="relative min-h-screen px-4 pb-24 pt-12"
      >
        {/* Section heading */}
        <div className="text-center mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">
            Test Road Safety 
          </h2>
          <p className="text-slate-500 text-sm">
            Plain English → Data-backed answer + chart
          </p>
        </div>

        {/* Search bar */}
        <div className="mb-8">
          <SearchBar
            onSubmit={(q) => {
              setInputValue(q);
              submit(q);
            }}
            loading={loading}
            initialValue={inputValue}
          />
        </div>

        {/* Suggestion chips — hide when results are shown */}
        {!data && !loading && !error && (
          <div className="mb-12">
            <SuggestionChips
              questions={DEFAULT_QUESTIONS}
              onSelect={handleSuggestion}
            />
          </div>
        )}

        {/* Loading skeleton */}
        {loading && (
          <div className="mt-8">
            <LoadingState question={currentQuestion} />
          </div>
        )}

        {/* Error state */}
        {error && !loading && (
          <div className="mt-8">
            <ErrorCard message={error} onRetry={handleReset} />
          </div>
        )}

        {/* Result */}
        {data && !loading && (
          <>
            <div className="mt-8">
              <ResultSection data={data} question={currentQuestion} />
            </div>

            {/* New query button */}
            <div className="flex justify-center mt-10">
              <button
                onClick={handleReset}
                className="
                  px-6 py-3 rounded-2xl text-sm font-semibold
                  bg-white/6 border border-white/12 text-slate-300
                  hover:bg-white/10 hover:border-white/20 hover:text-white
                  transition-all duration-200
                "
              >
                ← Ask another question
              </button>
            </div>
          </>
        )}
      </section>

      {/* ── Footer ───────────────────────────────────────────────────────── */}
      <footer className="border-t border-white/6 py-8 text-center text-xs text-slate-600">
        <p>
          NeuralCity · Powered by{" "}
          <span className="text-violet-400 font-semibold">Gemini 2.5 Flash</span> ·
          Indian Roads Open Dataset
        </p>
      </footer>
    </div>
  );
}
