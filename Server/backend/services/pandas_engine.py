"""
Pandas Query Engine.
Converts validated StructuredQuery objects into Pandas operations.
NO eval() or exec() — all operations are explicitly coded.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from ..schemas.query_schema import StructuredQuery
from ..utils.constants import DEFAULT_AGGREGATION, DEFAULT_METRIC, DEFAULT_TOP_N

logger = logging.getLogger(__name__)


class PandasEngine:
    """Executes structured queries using safe, explicit Pandas operations."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df.copy()
        self._prepare_data()

    def _prepare_data(self) -> None:
        """Add derived columns needed for analysis."""
        if "date" in self._df.columns:
            self._df["date"] = pd.to_datetime(self._df["date"], errors="coerce")
            self._df["month"] = self._df["date"].dt.month
            self._df["year"] = self._df["date"].dt.year
            self._df["day_of_week"] = self._df["date"].dt.day_name()
        
        if "time" in self._df.columns and "hour" not in self._df.columns:
            # Extract hour from time string (e.g. "14:30")
            self._df["hour"] = pd.to_datetime(self._df["time"], format="%H:%M", errors="coerce").dt.hour

    def execute(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        """
        Execute a structured query and return the result DataFrame 
        plus a description of the operations performed.
        
        Returns:
            (result_df, operation_description)
        """
        intent = query.intent

        dispatch = {
            "aggregate": self._execute_aggregate,
            "compare": self._execute_compare,
            "trend": self._execute_trend,
            "top_n": self._execute_top_n,
            "distribution": self._execute_distribution,
            "filter": self._execute_filter,
        }

        handler = dispatch.get(intent)
        if handler is None:
            raise ValueError(f"Unsupported intent: {intent}")

        return handler(query)

    # ── Private Helpers ──────────────────────────────────────────────────────

    def _apply_filters(self, df: pd.DataFrame, query: StructuredQuery) -> pd.DataFrame:
        """Apply all filters from the query to the dataframe."""
        if query.filters is None:
            return df

        filters = query.filters.model_dump(exclude_none=True)
        for col, value in filters.items():
            if col not in df.columns:
                logger.warning(f"Filter column '{col}' not in DataFrame. Skipping.")
                continue

            if isinstance(value, list):
                # Case-insensitive matching for string columns
                if df[col].dtype == "object":
                    # Handle "None" string values (e.g., festival column)
                    df = df[df[col].str.lower().isin([str(v).lower() for v in value])]
                else:
                    df = df[df[col].isin(value)]
            else:
                if df[col].dtype == "object":
                    str_val = str(value).lower()
                    df = df[df[col].str.lower() == str_val]
                else:
                    df = df[df[col] == value]

        return df

    def _aggregate_column(
        self,
        df: pd.DataFrame,
        metric: str,
        aggregation: str,
        group_by: str | list[str] | None = None,
    ) -> pd.DataFrame:
        """Perform groupby + aggregation safely."""
        metric = metric or DEFAULT_METRIC
        aggregation = aggregation or DEFAULT_AGGREGATION

        # For "accident_count" alias, use accident_id with count
        actual_metric = "accident_id" if metric in ("accident_count", "accident_id") and aggregation == "count" else metric
        # Ensure the actual metric column exists
        if actual_metric not in df.columns:
            # Fallback to accident_id for counting
            if aggregation == "count" and "accident_id" in df.columns:
                actual_metric = "accident_id"
            else:
                # Try to find the metric column
                available_numeric = df.select_dtypes(include=["number"]).columns.tolist()
                if actual_metric not in df.columns and available_numeric:
                    logger.warning(
                        f"Metric '{actual_metric}' not found. "
                        f"Available numeric columns: {available_numeric}"
                    )
                    raise ValueError(f"Metric column '{actual_metric}' not found in dataset.")

        if group_by is None:
            # Scalar aggregation
            value = self._safe_agg(df[actual_metric], aggregation)
            return pd.DataFrame({"metric": [metric], "value": [value]})

        groups = group_by if isinstance(group_by, list) else [group_by]

        # Validate all group columns exist
        valid_groups = [g for g in groups if g in df.columns]
        if not valid_groups:
            logger.warning(
                f"No valid group_by columns found ({groups}). "
                f"Available columns: {list(df.columns)}"
            )
            # Fallback to scalar aggregation
            value = self._safe_agg(df[actual_metric], aggregation)
            return pd.DataFrame({"metric": [metric], "value": [value]})

        if len(valid_groups) != len(groups):
            logger.warning(
                f"Some group_by columns missing: {set(groups) - set(valid_groups)}. "
                f"Using: {valid_groups}"
            )

        if aggregation == "count":
            result = df.groupby(valid_groups, dropna=False)[actual_metric].count().reset_index()
            result.columns = [*valid_groups, f"{metric}_{aggregation}"]
        else:
            result = getattr(df.groupby(valid_groups, dropna=False)[actual_metric], aggregation)().reset_index()
            result.columns = [*valid_groups, f"{metric}_{aggregation}"]

        return result

    @staticmethod
    def _safe_agg(series: pd.Series, aggregation: str) -> Any:
        """Safely apply aggregation function without eval."""
        agg_map = {
            "count": series.count,
            "sum": series.sum,
            "mean": series.mean,
            "min": series.min,
            "max": series.max,
        }
        func = agg_map.get(aggregation)
        if func is None:
            raise ValueError(f"Unsupported aggregation: {aggregation}")
        result = func()
        # Round floats for readability
        if isinstance(result, float):
            return round(result, 2)
        return result

    # ── Intent Handlers ──────────────────────────────────────────────────────

    def _execute_aggregate(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)
        metric = query.metric or DEFAULT_METRIC
        aggregation = query.aggregation or DEFAULT_AGGREGATION

        result = self._aggregate_column(df, metric, aggregation, query.group_by)

        # Sort if group_by present
        if query.group_by:
            value_col = result.columns[-1]
            ascending = query.sort_order == "asc"
            result = result.sort_values(value_col, ascending=ascending).reset_index(drop=True)

        desc = f"Computed {aggregation}({metric})"
        if query.group_by:
            desc += f" grouped by {query.group_by}"
        if query.filters:
            desc += f" with filters: {query.filters.model_dump(exclude_none=True)}"

        return result, desc

    def _execute_compare(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)
        metric = query.metric or DEFAULT_METRIC
        aggregation = query.aggregation or DEFAULT_AGGREGATION

        # If compare_values and compare_column provided, filter to those values
        if query.compare_values and query.compare_column:
            col = query.compare_column
            if col in df.columns:
                if df[col].dtype == "object":
                    df = df[
                        df[col]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .isin([str(v).strip().lower() for v in query.compare_values])
                    ]
                else:
                    # Handle mixed types (e.g., is_weekend with int values sent as strings)
                    try:
                        typed_values = [type(df[col].iloc[0])(v) for v in query.compare_values]
                        df = df[df[col].isin(typed_values)]
                    except (ValueError, IndexError):
                        df = df[df[col].isin(query.compare_values)]

        # Determine group columns for comparison
        group_by = query.group_by
        if query.compare_column and group_by:
            # Include both compare_column and group_by
            if isinstance(group_by, list):
                if query.compare_column not in group_by:
                    group_by = [query.compare_column] + group_by
            else:
                if query.compare_column != group_by:
                    group_by = [query.compare_column, group_by]
        elif query.compare_column and not group_by:
            group_by = query.compare_column

        result = self._aggregate_column(df, metric, aggregation, group_by)

        # Sort
        value_col = result.columns[-1]
        ascending = query.sort_order == "asc"
        result = result.sort_values(value_col, ascending=ascending).reset_index(drop=True)

        desc = f"Compared {aggregation}({metric}) across {query.compare_column or group_by}"
        if query.compare_values:
            desc += f" for values: {query.compare_values}"
        return result, desc

    def _execute_trend(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)
        metric = query.metric or DEFAULT_METRIC
        aggregation = query.aggregation or DEFAULT_AGGREGATION
        time_col = query.time_column or "month"

        # Ensure time column exists; fallback to month
        if time_col not in df.columns:
            logger.warning(f"Time column '{time_col}' not found. Falling back to 'month'.")
            time_col = "month"
            if time_col not in df.columns:
                raise ValueError(f"Neither '{query.time_column}' nor 'month' found in dataset.")

        # For trend, always group by the time column
        group_by = time_col
        # If additional group_by is specified, include it
        if query.group_by and query.group_by != time_col:
            if isinstance(query.group_by, list):
                if time_col not in query.group_by:
                    group_by = [time_col] + query.group_by
                else:
                    group_by = query.group_by
            else:
                if query.group_by != time_col:
                    group_by = [time_col, query.group_by]

        result = self._aggregate_column(df, metric, aggregation, group_by)

        # Sort by time column
        time_sort_col = time_col if time_col in result.columns else result.columns[0]
        result = result.sort_values(time_sort_col, ascending=True).reset_index(drop=True)

        desc = f"Trend analysis: {aggregation}({metric}) over {time_col}"
        if query.filters:
            desc += f" with filters: {query.filters.model_dump(exclude_none=True)}"
        return result, desc

    def _execute_top_n(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)
        metric = query.metric or DEFAULT_METRIC
        aggregation = query.aggregation or DEFAULT_AGGREGATION
        n = query.top_n or DEFAULT_TOP_N

        # Top N requires a group_by — if missing, try to infer
        group_by = query.group_by
        if group_by is None:
            # Sensible default: group by city
            logger.warning("top_n intent missing group_by. Defaulting to 'city'.")
            group_by = "city"

        result = self._aggregate_column(df, metric, aggregation, group_by)

        # Sort and take top N
        value_col = result.columns[-1]
        ascending = query.sort_order == "asc"
        result = result.sort_values(value_col, ascending=ascending).head(n).reset_index(drop=True)

        desc = f"Top {n} by {aggregation}({metric})"
        if group_by:
            desc += f" grouped by {group_by}"
        if query.filters:
            desc += f" with filters: {query.filters.model_dump(exclude_none=True)}"
        return result, desc

    def _execute_distribution(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)
        metric = query.metric or DEFAULT_METRIC
        aggregation = query.aggregation or DEFAULT_AGGREGATION
        group_by = query.group_by

        # Distribution requires group_by — provide a default if missing
        if group_by is None:
            # Try to infer from metric
            if metric in ("accident_severity", "weather", "road_type", "cause", "visibility"):
                group_by = metric
                metric = "accident_id"
                aggregation = "count"
                logger.warning(f"Distribution missing group_by. Using metric '{group_by}' as group.")
            else:
                logger.warning("Distribution missing group_by. Defaulting to 'accident_severity'.")
                group_by = "accident_severity"

        result = self._aggregate_column(df, metric, aggregation, group_by)

        # Sort by count descending
        value_col = result.columns[-1]
        result = result.sort_values(value_col, ascending=False).reset_index(drop=True)

        desc = f"Distribution of {group_by} by {aggregation}({metric})"
        return result, desc

    def _execute_filter(self, query: StructuredQuery) -> tuple[pd.DataFrame, str]:
        df = self._apply_filters(self._df, query)

        # Select relevant columns for display
        display_cols = [
            "accident_id", "city", "state", "date", "weather",
            "accident_severity", "cause", "casualties", "vehicles_involved",
            "risk_score", "road_type", "festival",
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        result = df[available_cols].head(100).reset_index(drop=True)

        filters_desc = ""
        if query.filters:
            filters_desc = str(query.filters.model_dump(exclude_none=True))

        desc = f"Filtered records with conditions: {filters_desc}. Showing up to 100 rows."
        return result, desc
