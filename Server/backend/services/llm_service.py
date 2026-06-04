"""
LLM Service — LangChain + Gemini integration.
Sends user questions with dataset metadata to Gemini and parses
the structured JSON response.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import pandas as pd
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from ..prompts.query_prompt import SYSTEM_PROMPT, USER_PROMPT
from ..prompts.answer_prompt import ANSWER_SYSTEM_PROMPT, ANSWER_USER_PROMPT
from ..schemas.query_schema import StructuredQuery
from ..utils.metadata import DatasetMetadata

logger = logging.getLogger(__name__)

# Timeouts in seconds
QUERY_TIMEOUT = 30
ANSWER_TIMEOUT = 20
MAX_RETRIES = 2


class LLMService:
    """Interfaces with Gemini via LangChain to generate structured queries."""

    def __init__(self, api_key: str, metadata: DatasetMetadata) -> None:
        self._metadata = metadata
        # Use gemini-2.0-flash — a fast, non-thinking model that reliably
        # returns structured JSON without entering long reasoning loops.
        self._model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1,
            max_output_tokens=1024,
        )
        self._system_prompt = SYSTEM_PROMPT.format(
            schema_summary=metadata.get_schema_summary()
        )

    async def generate_query(self, question: str) -> StructuredQuery:
        """
        Send the user question to Gemini and parse the structured JSON response.

        Args:
            question: Natural language question from the user.

        Returns:
            Validated StructuredQuery object.

        Raises:
            ValueError: If the LLM returns invalid JSON or fails validation.
        """
        user_message = USER_PROMPT.format(question=question)

        messages = [
            SystemMessage(content=self._system_prompt),
            HumanMessage(content=user_message),
        ]

        logger.info(f"Sending question to Gemini: {question}")

        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Wrap the LLM call with a timeout to prevent infinite hangs
                response = await asyncio.wait_for(
                    self._model.ainvoke(messages),
                    timeout=QUERY_TIMEOUT,
                )
                raw_text = response.content.strip()
                logger.info(f"Raw LLM response (attempt {attempt}): {raw_text[:500]}")

                # Extract JSON from the response (handle markdown code blocks)
                json_str = self._extract_json(raw_text)
                parsed = json.loads(json_str)

                # Validate through Pydantic
                query = StructuredQuery(**parsed)
                logger.info(f"Parsed query: {query.model_dump()}")

                return query

            except asyncio.TimeoutError:
                logger.warning(
                    f"LLM query generation timed out after {QUERY_TIMEOUT}s "
                    f"(attempt {attempt}/{MAX_RETRIES})"
                )
                last_error = TimeoutError(
                    f"LLM did not respond within {QUERY_TIMEOUT}s"
                )
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                last_error = ValueError(f"LLM returned invalid JSON: {e}")
                # Don't retry JSON errors — the model gave a response, it was just bad
                break
            except Exception as e:
                logger.error(f"LLM service error (attempt {attempt}): {e}")
                last_error = ValueError(f"LLM query generation failed: {e}")
                if attempt < MAX_RETRIES:
                    # Brief pause before retry
                    await asyncio.sleep(1)

        raise last_error or ValueError("LLM query generation failed after all retries")

    async def generate_answer(
        self,
        question: str,
        result_df: pd.DataFrame,
        operation_desc: str,
    ) -> str:
        """
        Generate a natural language answer based on the data results.

        Args:
            question: The original user question.
            result_df: The DataFrame result from the engine.
            operation_desc: Description of the operation performed.

        Returns:
            A natural language answer string.
        """
        if result_df.empty:
            return "No data found matching your query criteria."

        # Convert DF to a concise JSON/string for the prompt
        # We limit to 30 rows to keep tokens manageable and speed up response
        data_json = result_df.head(30).to_json(orient="records")

        system_prompt = ANSWER_SYSTEM_PROMPT.format(
            question=question,
            data_json=data_json,
            operation_desc=operation_desc
        )
        user_message = ANSWER_USER_PROMPT.format(question=question)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        logger.info(f"Generating synthesized answer for: {question}")

        try:
            # Wrap with timeout to prevent infinite hangs
            response = await asyncio.wait_for(
                self._model.ainvoke(messages),
                timeout=ANSWER_TIMEOUT,
            )
            return response.content.strip()
        except asyncio.TimeoutError:
            logger.warning(
                f"Answer generation timed out after {ANSWER_TIMEOUT}s, "
                f"using local fallback."
            )
            return ""
        except Exception as e:
            logger.error(f"Answer synthesis failed: {e}")
            return ""

    @staticmethod
    def _extract_json(text: str) -> str:
        """Extract JSON from potential markdown code blocks or mixed text."""
        # Strip thinking tags if present (some models wrap in <think>...</think>)
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

        # Try to find JSON in code blocks
        code_block_match = re.search(
            r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL
        )
        if code_block_match:
            return code_block_match.group(1).strip()

        # Try to find raw JSON object (outermost braces)
        brace_depth = 0
        start = None
        for i, ch in enumerate(text):
            if ch == "{":
                if brace_depth == 0:
                    start = i
                brace_depth += 1
            elif ch == "}":
                brace_depth -= 1
                if brace_depth == 0 and start is not None:
                    return text[start : i + 1]

        # Last resort: regex
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json_match.group(0).strip()

        return text
