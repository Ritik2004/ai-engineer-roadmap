import os 
import time
from groq import Groq
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key is not set")

client = Groq(
    api_key = api_key
)
multiply_tool = {
    "type":"function",
    "function":{
    "name":"multiply",
    "description":"does stuff",
    "parameters":{
        "type":"object",
        "properties":{
            "a":{"type":"number"},
            "b":{"type":"number"},
        },
        "required":["a","b"]
    },
    },
}
response = client.chat.completions.create(
   model="openai/gpt-oss-20b",
   messages=[{"role":"user","content":"what is 12 multiply by 7?"}],
   tools=[multiply_tool]
)

print(response.choices[0].message)
message = response.choices[0].message

for call in message.tool_calls:
    print(call.function.name)
    print(call.function.arguments)
