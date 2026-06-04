"""
API Routes for query processing.
Handles the full pipeline: LLM → Validation → Pandas → Chart → Answer.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from ..schemas.query_schema import UserQueryRequest
from ..schemas.response_schema import QueryResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Query"])

# Overall request timeout — the entire pipeline must finish within this
PIPELINE_TIMEOUT = 60


@router.post(
    "/query",
    response_model=QueryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or out-of-scope query"},
        408: {"model": ErrorResponse, "description": "Request timed out"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Process a natural language question about road accidents",
)
async def process_query(request: Request, body: UserQueryRequest):
    """
    Full query pipeline:
    1. Send user question to Gemini via LangChain
    2. Validate the structured JSON query
    3. Execute against the dataset using Pandas
    4. Generate a chart
    5. Format a natural language answer
    6. Return the complete response
    """
    try:
        return await asyncio.wait_for(
            _run_pipeline(request, body),
            timeout=PIPELINE_TIMEOUT,
        )
    except asyncio.TimeoutError:
        logger.error(
            f"Entire pipeline timed out after {PIPELINE_TIMEOUT}s "
            f"for question: {body.question}"
        )
        raise HTTPException(
            status_code=408,
            detail={
                "answer": "The request took too long to process. Please try rephrasing your question.",
                "reason": "Pipeline timeout",
            },
        )


async def _run_pipeline(request: Request, body: UserQueryRequest) -> QueryResponse:
    """Inner pipeline logic — separated so we can wrap it in a timeout."""
    # Retrieve services from app state
    llm_service = request.app.state.llm_service
    validation_service = request.app.state.validation_service
    pandas_engine = request.app.state.pandas_engine
    answer_service = request.app.state.answer_service
    audit_log = request.app.state.audit_log

    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # ── Step 1: Generate structured query from LLM ───────────────────
        structured_query = await llm_service.generate_query(body.question)
        query_dict = structured_query.model_dump(exclude_none=True)

        logger.info(f"Generated query: {query_dict}")

        # ── Step 2: Handle out_of_scope ──────────────────────────────────
        if structured_query.intent == "out_of_scope":
            answer = (
                structured_query.reason
                or "This dataset does not contain information required to answer the question."
            )

            # Log audit
            audit_log.append({
                "timestamp": timestamp,
                "user_query": body.question,
                "generated_json": query_dict,
                "result_summary": "out_of_scope",
            })

            return QueryResponse(
                answer=answer,
                chart_path=None,
                chart_base64=None,
                operation_description="Query classified as out of scope.",
                query_json=query_dict,
                result_table=[],
            )

        # ── Step 3: Validate the query ───────────────────────────────────
        from ..services.validation_service import ValidationError
        try:
            validated_query = validation_service.validate(structured_query)
        except ValidationError as ve:
            logger.warning(f"Validation failed: {ve}")
            raise HTTPException(
                status_code=400,
                detail={
                    "answer": f"Query validation failed: {ve}",
                    "reason": str(ve),
                    "query_json": query_dict,
                },
            )

        # ── Step 4: Execute against Pandas ───────────────────────────────
        result_df, operation_desc = pandas_engine.execute(validated_query)

        # ── Step 5: Skip chart generation ────────────────────────────────
        chart_path, chart_b64 = None, None

        # ── Step 6: Format answer ────────────────────────────────────────
        # Use local AnswerService first (instant, reliable, never hangs)
        local_answer = answer_service.format_answer(
            result_df, validated_query, operation_desc
        )

        # Try to enhance with LLM answer (but don't block if it fails)
        answer = local_answer
        try:
            llm_answer = await llm_service.generate_answer(
                body.question,
                result_df,
                operation_desc,
            )
            if llm_answer and len(llm_answer) > 10:
                answer = llm_answer
        except Exception as e:
            logger.warning(f"LLM answer generation failed, using local: {e}")
            # local_answer is already set as the fallback

        # ── Step 7: Prepare result table ─────────────────────────────────
        result_table = result_df.head(50).to_dict(orient="records")
        # Clean NaN values for JSON serialization
        for row in result_table:
            for key, val in row.items():
                if isinstance(val, float) and (val != val):  # NaN check
                    row[key] = None

        # ── Audit log ────────────────────────────────────────────────────
        audit_log.append({
            "timestamp": timestamp,
            "user_query": body.question,
            "generated_json": query_dict,
            "result_summary": f"{len(result_df)} rows returned",
        })

        return QueryResponse(
            answer=answer,
            chart_path=chart_path,
            chart_base64=chart_b64,
            operation_description=operation_desc,
            query_json=query_dict,
            result_table=result_table,
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error in query pipeline: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "answer": str(e),
                "reason": "Query processing failed",
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error in query pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "answer": "An internal error occurred while processing your question.",
                "reason": str(e),
            },
        )
