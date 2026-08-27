# backend/app/services/llm_client.py
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"