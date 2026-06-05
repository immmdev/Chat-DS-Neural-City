import { Sparkles, Info } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function AnswerCard({ answer, operationDescription }) {
  if (!answer) return null;

  return (
    <div
      className="rounded-3xl p-6 space-y-4"
      style={{
        background:
          "linear-gradient(135deg, rgba(99,103,255,0.10) 0%, rgba(197,197,240,0.06) 100%)",
        border: "1px solid rgba(99,103,255,0.22)",
        backdropFilter: "blur(16px)",
        boxShadow:
          "0 2px 0 rgba(255,255,255,0.06) inset, 0 8px 32px rgba(99,103,255,0.1)",
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-2.5">
        <div
          className="w-7 h-7 rounded-xl flex items-center justify-center shrink-0"
          style={{
            background: "linear-gradient(135deg,#6367FF,#C5C5F0)",
          }}
        >
          <Sparkles size={13} className="text-white" />
        </div>

        <span
          className="text-xs font-bold tracking-widest uppercase"
          style={{ color: "#7B8FE8" }}
        >
          AI Answer
        </span>
      </div>

      {/* Markdown Answer */}
      <div
        className="prose prose-invert max-w-none text-base leading-relaxed"
        style={{ color: "#e4e4f7" }}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {answer}
        </ReactMarkdown>
      </div>

      {/* Operation note */}
      {operationDescription && (
        <div
          className="flex items-start gap-2 pt-3"
          style={{
            borderTop: "1px solid rgba(99,103,255,0.12)",
          }}
        >
          <Info
            size={12}
            className="shrink-0 mt-0.5"
            style={{ color: "#7B8FE8" }}
          />

          <p
            className="text-xs leading-relaxed"
            style={{ color: "rgba(123,143,232,0.75)" }}
          >
            <span
              className="font-semibold"
              style={{ color: "#7B8FE8" }}
            >
              How computed:
            </span>{" "}
            {operationDescription}
          </p>
        </div>
      )}
    </div>
  );
}