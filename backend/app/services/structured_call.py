# backend/app/services/structured_call.py
import json
from pydantic import BaseModel, ValidationError
from app.services.llm_client import client, MODEL

def call_structured(system_prompt: str, human_prompt: str, schema: type[BaseModel]) -> BaseModel:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "human" if False else "user", "content": human_prompt},
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

    except (ValidationError, json.JSONDecodeError, Exception) as first_error:
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
        resp = client.chat.completions.create(
            model=MODEL,
            messages=fallback_messages,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        content = _strip_code_fences(content)
        return schema.model_validate_json(content)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()