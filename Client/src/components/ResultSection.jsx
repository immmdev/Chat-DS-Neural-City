/**
 * ResultSection — question echo + AnswerCard + ChartPanel + ResultTable + DebugPanel.
 */
import AnswerCard      from "./AnswerCard";
import ChartPanel      from "./ChartPanel";
import ResultTable     from "./ResultTable";
import QueryDebugPanel from "./QueryDebugPanel";
import { MessageSquare } from "lucide-react";

export default function ResultSection({ data, question }) {
  if (!data) return null;
  const { answer, operation_description, result_table, query_json } = data;

  return (
    <div className="w-full max-w-5xl mx-auto space-y-5 animate-fade-in">

      {/* Question echo */}
      <div className="flex items-start gap-3 px-5 py-4 rounded-2xl"
        style={{
          background: "rgba(99,103,255,0.07)",
          border: "1px solid rgba(99,103,255,0.18)",
        }}>
        <MessageSquare size={15} className="shrink-0 mt-0.5" style={{ color: "#6367FF" }} />
        <p className="text-sm italic leading-relaxed" style={{ color: "#C5C5F0" }}>
          {question}
        </p>
      </div>

      {/* Answer + Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <AnswerCard answer={answer} operationDescription={operation_description} />
        <ChartPanel resultTable={result_table} />
      </div>

      {/* Data table */}
      <ResultTable resultTable={result_table} />

      {/* Debug */}
      <QueryDebugPanel queryJson={query_json} />
    </div>
  );
}
