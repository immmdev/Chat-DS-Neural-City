"""
Answer Service — Natural Language Response Formatter.
Converts raw Pandas results into human-readable answers.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from ..schemas.query_schema import StructuredQuery

logger = logging.getLogger(__name__)


class AnswerService:
    """Generates natural language answers from structured query results."""

    def format_answer(
        self,
        result_df: pd.DataFrame,
        query: StructuredQuery,
        operation_desc: str,
    ) -> str:
        """
        Generate a natural language answer based on query results.
        
        Args:
            result_df: The Pandas DataFrame result from the engine.
            query: The structured query that was executed.
            operation_desc: Description of the Pandas operation performed.
            
        Returns:
            A human-readable answer string.
        """
        if query.intent == "out_of_scope":
            return (
                query.reason
                or "This dataset does not contain information required to answer the question."
            )

        if result_df.empty:
            return "No data found matching your query criteria."

        handler = {
            "aggregate": self._format_aggregate,
            "compare": self._format_compare,
            "trend": self._format_trend,
            "top_n": self._format_top_n,
            "distribution": self._format_distribution,
            "filter": self._format_filter,
        }.get(query.intent, self._format_generic)

        try:
            return handler(result_df, query)
        except Exception as e:
            logger.error(f"Answer formatting error: {e}")
            return self._format_generic(result_df, query)

    # ── Intent-Specific Formatters ───────────────────────────────────────────

    def _format_aggregate(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        if query.group_by is None and len(df) == 1:
            # Scalar result
            value = df.iloc[0]["value"]
            metric = query.metric or "accidents"
            agg = query.aggregation or "count"

            agg_labels = {
                "count": "total count",
                "sum": "total sum",
                "mean": "average",
                "min": "minimum",
                "max": "maximum",
            }
            agg_label = agg_labels.get(agg, agg)

            filters_desc = self._describe_filters(query)

            answer = f"The {agg_label} of **{metric}**{filters_desc} is **{self._fmt(value)}**."
            return answer

        # Grouped aggregation
        return self._format_grouped_result(df, query)

    def _format_compare(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        if df.empty:
            return "No data found for the comparison."

        lines = ["Here is the comparison:\n"]
        value_col = df.columns[-1]

        for _, row in df.iterrows():
            label_parts = [str(row[c]) for c in df.columns[:-1]]
            label = " — ".join(label_parts)
            lines.append(f"- **{label}**: {self._fmt(row[value_col])}")

        # Highlight highest/lowest
        if len(df) >= 2:
            max_row = df.loc[df[value_col].idxmax()]
            label_parts = [str(max_row[c]) for c in df.columns[:-1]]
            lines.append(f"\n**{' — '.join(label_parts)}** has the highest value at **{self._fmt(max_row[value_col])}**.")

        return "\n".join(lines)

    def _format_trend(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        if df.empty:
            return "No trend data available."

        value_col = df.columns[-1]
        time_col = df.columns[0]

        first_val = df.iloc[0][value_col]
        last_val = df.iloc[-1][value_col]

        if first_val != 0:
            change_pct = ((last_val - first_val) / first_val) * 100
            direction = "increased" if change_pct > 0 else "decreased"
            trend_summary = f"The values {direction} by **{abs(change_pct):.1f}%** from the beginning to the end of the period."
        else:
            trend_summary = f"Starting value was 0, ending at {self._fmt(last_val)}."

        peak_idx = df[value_col].idxmax()
        peak_row = df.loc[peak_idx]
        peak_info = f"The peak was in **{time_col} = {peak_row[time_col]}** with a value of **{self._fmt(peak_row[value_col])}**."

        lines = [
            f"Here is the trend of **{query.metric or 'accidents'}** over **{time_col}**:\n",
            trend_summary,
            peak_info,
            f"\nShowing {len(df)} data points in total.",
        ]

        return "\n".join(lines)

    def _format_top_n(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        n = query.top_n or len(df)
        metric = query.metric or "accidents"
        agg = query.aggregation or "count"
        value_col = df.columns[-1]
        group_col = df.columns[0]

        lines = [f"**Top {n}** by {agg} of {metric}:\n"]

        for rank, (_, row) in enumerate(df.iterrows(), 1):
            lines.append(f"{rank}. **{row[group_col]}** — {self._fmt(row[value_col])}")

        return "\n".join(lines)

    def _format_distribution(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        value_col = df.columns[-1]
        group_col = df.columns[0]
        total = df[value_col].sum()

        lines = [f"Distribution of **{group_col}**:\n"]

        for _, row in df.iterrows():
            pct = (row[value_col] / total * 100) if total > 0 else 0
            lines.append(
                f"- **{row[group_col]}**: {self._fmt(row[value_col])} ({pct:.1f}%)"
            )

        return "\n".join(lines)

    def _format_filter(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        count = len(df)
        filters_desc = self._describe_filters(query)

        lines = [
            f"Found **{count}** records{filters_desc}.",
        ]

        if count > 0:
            lines.append(f"Showing first {min(count, 100)} results in the table below.")

        return "\n".join(lines)

    def _format_generic(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        return f"Query executed successfully. Found {len(df)} result rows."

    def _format_grouped_result(self, df: pd.DataFrame, query: StructuredQuery) -> str:
        value_col = df.columns[-1]
        group_col = df.columns[0]

        lines = [f"Results grouped by **{group_col}**:\n"]
        for _, row in df.head(15).iterrows():
            lines.append(f"- **{row[group_col]}**: {self._fmt(row[value_col])}")

        if len(df) > 15:
            lines.append(f"\n... and {len(df) - 15} more rows.")

        return "\n".join(lines)

    # ── Utilities ────────────────────────────────────────────────────────────

    @staticmethod
    def _fmt(value: Any) -> str:
        """Format a numeric value for display."""
        if isinstance(value, float):
            if value == int(value):
                return f"{int(value):,}"
            return f"{value:,.2f}"
        if isinstance(value, int):
            return f"{value:,}"
        return str(value)

    @staticmethod
    def _describe_filters(query: StructuredQuery) -> str:
        """Generate a human-readable filter description."""
        if query.filters is None:
            return ""
        filters = query.filters.model_dump(exclude_none=True)
        if not filters:
            return ""
        parts = [f"{k}={v}" for k, v in filters.items()]
        return " (where " + ", ".join(parts) + ")"
