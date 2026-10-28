import os
from google import genai
from google.genai import types, errors
import time

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Key is not set")


# create a gemini client
client = genai.Client(
    api_key=api_key,
    # http_options=types.HttpOptions(
    #     timeout=10000
    # )
                      )

# store conversation history
history=[]

# keep chatting until user type exit

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Chat ended")
        break

    if not question:
        print("Question cannot be empty.")
        raise SystemExit(1)

    # add user message to history

    history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=question)]
        )
    )
    

    # response = client.models.generate_content(
    #     model="gemini-3.5-flash-lite",
    #     contents = question,
    #     config = types.GenerateContentConfig(
    #         system_instruction = (
    #             "you are senior backend engineer"
    #             "Explain concept in simple way and give short example"
    #         ),
    #     temperature = 0.2,
    #     max_output_tokens = 250,
    #     )
    # )
    # send entire conversation to gemini
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents = history
        )
    except Exception as e:
        print(f"something went wrong:{e}")
        continue

    answer = response.text or 'Answer cannot be generated'
    print(f"Response is:{answer}")


    # add gemini response to history
    history.append(
        types.Content(
            role="model",
            parts=[types.Part(text=answer)]
        )
    )