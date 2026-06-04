"""
Dataset Metadata Generator.
Extracts and stores schema information from the accident dataset at startup.
This metadata is passed to the LLM so it knows what can be queried.
"""

from __future__ import annotations

import pandas as pd
from typing import Any


class DatasetMetadata:
    """Extracts and holds metadata about the loaded dataset."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        self._metadata: dict[str, Any] = {}
        self._build_metadata()

    # ── Core Builder ─────────────────────────────────────────────────────────
    def _build_metadata(self) -> None:
        df = self._df

        self._metadata = {
            "total_records": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dt) for col, dt in df.dtypes.items()},
            "date_range": {
                "min": str(df["date"].min()) if "date" in df.columns else None,
                "max": str(df["date"].max()) if "date" in df.columns else None,
            },
            "cities": sorted(df["city"].dropna().unique().tolist()) if "city" in df.columns else [],
            "states": sorted(df["state"].dropna().unique().tolist()) if "state" in df.columns else [],
            "categorical_values": self._extract_categorical_values(),
            "numeric_stats": self._extract_numeric_stats(),
        }

    def _extract_categorical_values(self) -> dict[str, list[str]]:
        """Store unique values for each categorical column."""
        categorical_cols = self._df.select_dtypes(include=["object", "category"]).columns
        result: dict[str, list[str]] = {}
        for col in categorical_cols:
            unique_vals = self._df[col].dropna().unique().tolist()
            # Only include if reasonable number of unique values
            if len(unique_vals) <= 50:
                result[col] = sorted([str(v) for v in unique_vals])
        return result

    def _extract_numeric_stats(self) -> dict[str, dict[str, float]]:
        """Extract min/max/mean for numeric columns."""
        numeric_cols = self._df.select_dtypes(include=["number"]).columns
        result: dict[str, dict[str, float]] = {}
        for col in numeric_cols:
            result[col] = {
                "min": round(float(self._df[col].min()), 2),
                "max": round(float(self._df[col].max()), 2),
                "mean": round(float(self._df[col].mean()), 2),
            }
        return result

    # ── Accessors ────────────────────────────────────────────────────────────
    @property
    def metadata(self) -> dict[str, Any]:
        return self._metadata

    @property
    def columns(self) -> list[str]:
        return self._metadata["columns"]

    @property
    def cities(self) -> list[str]:
        return self._metadata["cities"]

    @property
    def states(self) -> list[str]:
        return self._metadata["states"]

    @property
    def categorical_values(self) -> dict[str, list[str]]:
        return self._metadata["categorical_values"]

    def get_schema_summary(self) -> str:
        """Generate a human-readable schema summary for the LLM prompt."""
        lines = [
            "Dataset: Indian Road Accident Data (2022–2025)",
            f"Total Records: {self._metadata['total_records']}",
            f"Date Range: {self._metadata['date_range']['min']} to {self._metadata['date_range']['max']}",
            "",
            "Columns and Types:",
        ]
        for col, dtype in self._metadata["dtypes"].items():
            lines.append(f"  - {col} ({dtype})")

        lines.append("")
        lines.append("Categorical Values:")
        for col, values in self._metadata["categorical_values"].items():
            vals_str = ", ".join(values[:15])
            suffix = f" ... ({len(values)} total)" if len(values) > 15 else ""
            lines.append(f"  - {col}: [{vals_str}{suffix}]")

        lines.append("")
        lines.append("Cities: " + ", ".join(self._metadata["cities"]))
        lines.append("States: " + ", ".join(self._metadata["states"]))

        return "\n".join(lines)
