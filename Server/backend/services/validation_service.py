"""
Query Validation Service.
Validates structured queries against the dataset schema before execution.
Ensures all referenced columns, values, and operations exist.
Auto-corrects minor LLM output mismatches where possible.
"""

from __future__ import annotations

import difflib
import logging
from typing import Any

from ..schemas.query_schema import StructuredQuery
from ..utils.constants import (
    ALLOWED_COLUMNS,
    ALLOWED_AGGREGATIONS,
    ALLOWED_INTENTS,
    ALLOWED_METRICS,
    GROUPABLE_COLUMNS,
    MAX_TOP_N,
)
from ..utils.metadata import DatasetMetadata

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when query validation fails."""
    pass


# ── Common LLM metric aliases → actual column names ─────────────────────────
METRIC_ALIASES = {
    "accidents": "accident_id",
    "accident_count": "accident_id",
    "accident": "accident_id",
    "count": "accident_id",
    "total_accidents": "accident_id",
    "num_accidents": "accident_id",
    "number_of_accidents": "accident_id",
    "severity": "accident_severity",
    "risk": "risk_score",
    "casualty": "casualties",
    "vehicle": "vehicles_involved",
    "vehicles": "vehicles_involved",
    "temp": "temperature",
}

# ── Common LLM group_by aliases → actual column names ───────────────────────
GROUP_BY_ALIASES = {
    "road": "road_type",
    "road_type_name": "road_type",
    "severity": "accident_severity",
    "accident_type": "accident_severity",
    "weather_condition": "weather",
    "weather_conditions": "weather",
    "day": "day_of_week",
    "dayofweek": "day_of_week",
    "weekend": "is_weekend",
    "peak_hour": "is_peak_hour",
    "signal": "traffic_signal",
    "traffic": "traffic_density",
    "density": "traffic_density",
}


class ValidationService:
    """Validates structured queries against the dataset schema."""

    def __init__(self, metadata: DatasetMetadata) -> None:
        self._metadata = metadata
        self._categorical_values = metadata.categorical_values

    def validate(self, query: StructuredQuery) -> StructuredQuery:
        """
        Run all validation checks on a structured query.
        Auto-corrects minor mismatches before raising errors.

        Raises:
            ValidationError: If any validation check fails and can't be auto-fixed.
        """
        self._validate_intent(query)

        # No further validation needed for out_of_scope
        if query.intent == "out_of_scope":
            return query

        self._auto_correct_metric(query)
        self._auto_correct_group_by(query)
        self._validate_aggregation(query)
        self._validate_filters(query)
        self._validate_top_n(query)
        self._validate_compare(query)
        self._validate_trend(query)

        logger.info(f"Query validated successfully: {query.intent}")
        return query

    def _validate_intent(self, query: StructuredQuery) -> None:
        if query.intent not in ALLOWED_INTENTS:
            raise ValidationError(
                f"Unknown intent '{query.intent}'. "
                f"Allowed intents: {ALLOWED_INTENTS}"
            )

    def _auto_correct_metric(self, query: StructuredQuery) -> None:
        """Try to auto-correct the metric if it's an alias or close match."""
        if query.metric is None:
            return

        metric = query.metric.lower().strip()

        # Check aliases first
        if metric in METRIC_ALIASES:
            corrected = METRIC_ALIASES[metric]
            if corrected != query.metric:
                logger.info(f"Auto-corrected metric: '{query.metric}' → '{corrected}'")
                query.metric = corrected
            return

        # "accident_count" is an explicit alias
        if query.metric == "accident_count":
            return

        # Already a valid column
        if query.metric in ALLOWED_COLUMNS:
            return

        # Try fuzzy matching against allowed metrics
        close = difflib.get_close_matches(
            query.metric, ALLOWED_METRICS + ALLOWED_COLUMNS, n=1, cutoff=0.6
        )
        if close:
            logger.info(f"Auto-corrected metric: '{query.metric}' → '{close[0]}'")
            query.metric = close[0]
            return

        raise ValidationError(
            f"Metric '{query.metric}' is not a valid column. "
            f"Available columns: {ALLOWED_COLUMNS}"
        )

    def _auto_correct_group_by(self, query: StructuredQuery) -> None:
        """Try to auto-correct group_by columns."""
        if query.group_by is None:
            return

        groups = query.group_by if isinstance(query.group_by, list) else [query.group_by]
        corrected_groups = []

        for g in groups:
            g_lower = g.lower().strip()

            # Check aliases
            if g_lower in GROUP_BY_ALIASES:
                corrected = GROUP_BY_ALIASES[g_lower]
                logger.info(f"Auto-corrected group_by: '{g}' → '{corrected}'")
                corrected_groups.append(corrected)
                continue

            # Already valid
            if g in GROUPABLE_COLUMNS:
                corrected_groups.append(g)
                continue

            # Fuzzy match
            close = difflib.get_close_matches(g, GROUPABLE_COLUMNS, n=1, cutoff=0.6)
            if close:
                logger.info(f"Auto-corrected group_by: '{g}' → '{close[0]}'")
                corrected_groups.append(close[0])
                continue

            raise ValidationError(
                f"Cannot group by '{g}'. "
                f"Allowed group_by columns: {GROUPABLE_COLUMNS}"
            )

        # Update query with corrected group_by
        if isinstance(query.group_by, list):
            query.group_by = corrected_groups
        else:
            query.group_by = corrected_groups[0] if corrected_groups else None

    def _validate_aggregation(self, query: StructuredQuery) -> None:
        if query.aggregation and query.aggregation not in ALLOWED_AGGREGATIONS:
            # Try to auto-correct common alternatives
            agg_map = {"average": "mean", "avg": "mean", "total": "sum", "minimum": "min", "maximum": "max"}
            corrected = agg_map.get(query.aggregation.lower())
            if corrected:
                logger.info(f"Auto-corrected aggregation: '{query.aggregation}' → '{corrected}'")
                query.aggregation = corrected
                return
            raise ValidationError(
                f"Aggregation '{query.aggregation}' is not allowed. "
                f"Allowed: {ALLOWED_AGGREGATIONS}"
            )

    def _validate_filters(self, query: StructuredQuery) -> None:
        if query.filters is None:
            return

        filters_dict = query.filters.model_dump(exclude_none=True)

        for col, value in filters_dict.items():
            # "year", "month", "hour" are derived columns, skip column existence check
            if col in ("year", "month", "hour"):
                continue

            if col not in ALLOWED_COLUMNS:
                logger.warning(
                    f"Filter column '{col}' does not exist in the dataset. Ignoring."
                )
                # Clear the invalid filter instead of raising
                setattr(query.filters, col, None)
                continue

            # Check categorical values exist in dataset (with fuzzy matching)
            if col in self._categorical_values:
                valid_values = self._categorical_values[col]
                values_to_check = value if isinstance(value, list) else [value]
                corrected_values = []
                for v in values_to_check:
                    v_str = str(v)
                    # Case-insensitive exact match first
                    match = next(
                        (vv for vv in valid_values if vv.lower() == v_str.lower()),
                        None,
                    )
                    if match:
                        corrected_values.append(match)
                        continue

                    # Fuzzy match
                    close = difflib.get_close_matches(v_str, valid_values, n=1, cutoff=0.6)
                    if close:
                        logger.info(
                            f"Auto-corrected filter value: '{v_str}' → '{close[0]}' for column '{col}'"
                        )
                        corrected_values.append(close[0])
                        continue

                    # If no match found, log a warning but still allow it
                    # (could be a partial string or edge case)
                    logger.warning(
                        f"Filter value '{v}' for column '{col}' not found in known values. "
                        f"Allowing anyway — Pandas filtering will handle it."
                    )
                    corrected_values.append(v_str)

                # Update filter with corrected values
                if isinstance(value, list):
                    setattr(query.filters, col, corrected_values)
                else:
                    setattr(query.filters, col, corrected_values[0] if corrected_values else value)

    def _validate_top_n(self, query: StructuredQuery) -> None:
        if query.intent == "top_n":
            if query.top_n is not None and query.top_n > MAX_TOP_N:
                logger.warning(
                    f"top_n value {query.top_n} exceeds maximum of {MAX_TOP_N}. "
                    f"Capping to {MAX_TOP_N}."
                )
                query.top_n = MAX_TOP_N

    def _validate_compare(self, query: StructuredQuery) -> None:
        if query.intent == "compare":
            if query.compare_column:
                col = query.compare_column
                if col not in ALLOWED_COLUMNS + ["is_weekend"]:
                    # Try alias
                    alias = GROUP_BY_ALIASES.get(col.lower())
                    if alias:
                        logger.info(f"Auto-corrected compare_column: '{col}' → '{alias}'")
                        query.compare_column = alias
                    else:
                        close = difflib.get_close_matches(
                            col, ALLOWED_COLUMNS + ["is_weekend"], n=1, cutoff=0.6
                        )
                        if close:
                            logger.info(f"Auto-corrected compare_column: '{col}' → '{close[0]}'")
                            query.compare_column = close[0]
                        else:
                            raise ValidationError(
                                f"compare_column '{col}' is not a valid column."
                            )

    def _validate_trend(self, query: StructuredQuery) -> None:
        if query.intent == "trend":
            allowed_time = ["month", "year", "day_of_week", "hour", "date"]
            if query.time_column and query.time_column not in allowed_time:
                close = difflib.get_close_matches(
                    query.time_column, allowed_time, n=1, cutoff=0.5
                )
                if close:
                    logger.info(f"Auto-corrected time_column: '{query.time_column}' → '{close[0]}'")
                    query.time_column = close[0]
                else:
                    logger.warning(
                        f"time_column '{query.time_column}' not valid. Defaulting to 'month'."
                    )
                    query.time_column = "month"
