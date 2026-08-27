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

    # ---- Attempt 1: native structured output ----
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
        content = _extract_content(resp)
        return schema.model_validate_json(content)

    except RateLimitError as e:
        _raise_rate_limit(e)
    except (APITimeoutError, APIConnectionError, APIError) as e:
        _raise_llm_unavailable(e)
    except (ValidationError, json.JSONDecodeError, ValueError, TypeError) as first_error:
        logger.warning("Structured output failed, falling back to json_object mode: %s", first_error)

    # ---- Attempt 2: plain JSON mode ----
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
        content = _extract_content(resp)
        content = _strip_code_fences(content)
        return schema.model_validate_json(content)

    except RateLimitError as e:
        _raise_rate_limit(e)
    except (APITimeoutError, APIConnectionError, APIError) as e:
        _raise_llm_unavailable(e)
    except (ValidationError, json.JSONDecodeError, ValueError, TypeError) as e:
        logger.error("Fallback JSON validation also failed: %s", e)
        raise HTTPException(
            status_code=502,
            detail={
                "error": "llm_parse_error",
                "message": "AI returned invalid or empty structured data. Please try again.",
            },
        ) from e


def _extract_content(resp) -> str:
    """Safely pull the message content. Raises ValueError if the response is empty/malformed."""
    if resp is None:
        raise ValueError("LLM returned None response")

    choices = getattr(resp, "choices", None)
    if not choices:
        # Log the whole response so you can see what OpenRouter actually sent
        logger.error("LLM response has no choices. Full response: %s", resp)
        raise ValueError("LLM response contains no choices (model may not support this response_format)")

    message = getattr(choices[0], "message", None)
    if message is None:
        raise ValueError("LLM choice has no message")

    content = getattr(message, "content", None)
    if not content:
        raise ValueError("LLM message content is empty")

    return content


def _raise_rate_limit(exc: Exception) -> None:
    logger.warning("LLM rate limit hit: %s", exc)
    raise HTTPException(
        status_code=429,
        detail={
            "error": "rate_limit",
            "message": "The AI provider is temporarily rate-limited. Please try again in a few seconds.",
            "retry_after": 10,
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
    ) from exp


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()