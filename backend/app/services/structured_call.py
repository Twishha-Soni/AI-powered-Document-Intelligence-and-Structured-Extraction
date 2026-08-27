# backend/app/services/structured_call.py
import json
import logging
from pydantic import BaseModel, ValidationError
from openai import RateLimitError, APIError, APITimeoutError, APIConnectionError
from fastapi import HTTPException

from app.services.llm_client import client, MODEL

logger = logging.getLogger(__name__)


def call_structured(system_prompt: str, human_prompt: str, schema: type[BaseModel]) -> BaseModel:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": human_prompt},
    ]

    # ---- Attempt 1: native structured output (json_schema, strict) ----
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "strict": True,
                    "schema": schema.model_json_schema(),
                },
            },
        )
        content = resp.choices[0].message.content
        return schema.model_validate_json(content)

    except RateLimitError as e:
        _raise_rate_limit(e)
    except (APITimeoutError, APIConnectionError, APIError) as e:
        _raise_llm_unavailable(e)
    except (ValidationError, json.JSONDecodeError, Exception) as first_error:
        # Only fall back for validation / parsing problems, not for rate limits
        logger.warning("Structured output failed, falling back to json_object mode: %s", first_error)

    # ---- Attempt 2: fallback — plain JSON mode + explicit instruction ----
    fallback_messages = messages + [
        {
            "role": "system",
            "content": (
                "Respond with ONLY a valid JSON object matching this schema, "
                "no prose, no markdown code fences:\n"
                f"{json.dumps(schema.model_json_schema())}"
            ),
        }
    ]

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=fallback_messages,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        content = _strip_code_fences(content)
        return schema.model_validate_json(content)

    except RateLimitError as e:
        _raise_rate_limit(e)
    except (APITimeoutError, APIConnectionError, APIError) as e:
        _raise_llm_unavailable(e)
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error("Fallback JSON validation also failed: %s", e)
        raise HTTPException(
            status_code=502,
            detail={
                "error": "llm_parse_error",
                "message": "AI returned invalid structured data. Please try again.",
            },
        ) from e


def _raise_rate_limit(exc: Exception) -> None:
    logger.warning("LLM rate limit hit: %s", exc)
    raise HTTPException(
        status_code=429,
        detail={
            "error": "rate_limit",
            "message": "The AI provider is temporarily rate-limited. Please try again in a few seconds.",
            "retry_after": 10,  # optional hint for frontend
        },
    ) from exc


def _raise_llm_unavailable(exc: Exception) -> None:
    logger.error("LLM service error: %s", exc)
    raise HTTPException(
        status_code=503,
        detail={
            "error": "llm_unavailable",
            "message": "AI service is temporarily unavailable. Please try again shortly.",
        },
    ) from exc


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()