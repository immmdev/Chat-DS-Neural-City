"""
Pydantic models for API response formatting.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Optional


class QueryResponse(BaseModel):
    """Standard successful response returned to the client."""
    answer: str = Field(..., description="Natural language answer to the user's question")
    chart_path: Optional[str] = Field(default=None, description="Path to the generated chart image")
    chart_base64: Optional[str] = Field(default=None, description="Base64-encoded chart image")
    operation_description: str = Field(..., description="Description of the Pandas operations performed")
    query_json: dict[str, Any] = Field(..., description="The structured query JSON used for execution")
    result_table: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Tabular result data as a list of row dicts"
    )


class ErrorResponse(BaseModel):
    """Error response for failed or out-of-scope queries."""
    answer: str = Field(..., description="Error explanation")
    reason: Optional[str] = Field(default=None, description="Detailed reason for the error")
    query_json: Optional[dict[str, Any]] = Field(default=None, description="The query that caused the error")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    total_records: int = 0
    columns: list[str] = Field(default_factory=list)
    date_range: dict[str, Optional[str]] = Field(default_factory=dict)
