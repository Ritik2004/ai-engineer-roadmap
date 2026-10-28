
import os
import time
from groq import Groq
import time

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(
    api_key=api_key,
    timeout=20.0,
    max_retries=1
)

history = []

while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Chat ended.")
        break

    if not question:
        print("Question cannot be empty.")
        continue

    # Keep the most recent 10 messages
    recent_history = history[-10:]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior backend engineer. "
                "Explain concepts in simple language "
                "and give a short example."
            )
        }
    ]

    messages.extend(recent_history)
    messages.append({
        "role": "user",
        "content": question
    })

    start = time.perf_counter()

    try:
        print("Sending request to Groq...", flush=True)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.2,
            stream = True
        )

        answer = ""
        for chunk in response:
            text = chunk.choices[0].delta.content
            if text:
                print(text,end="",flush=True)
                answer+=text
                time.sleep(0.05)

        print()
        
        if answer:
            # print(f"\nGroq: {answer}")

            history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ])
        else:
            print("Groq returned an empty response.")

    except Exception as e:
        print(f"Request failed: {type(e).__name__}: {e}")

    elapsed = time.perf_counter() - start
    print(f"Response time: {elapsed:.2f} seconds")
