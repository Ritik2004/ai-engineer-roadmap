import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=120000)
)

print("Sending request...", flush=True)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain a race condition in two sentences.",
        config=types.GenerateContentConfig(
            max_output_tokens=100,
        )
    )
    print(response.text)

except Exception as e:
    print(type(e).__name__, e)