# Revision Notes (for interviews)

One section per topic. Keep each one short: **what it is, how it works, key code, interview questions.**
Add a line **"In my words"** to each section yourself. If you can't write it, you haven't understood the topic yet.

**Topics so far:** Pydantic basics · LLM API calls + chat memory · Structured output · Streaming · Tool calling · Agent loop

---

## Pydantic basics (foundations)

**What:** A library that defines the **shape of data** with Python classes and **validates** it automatically.

**Key code:**
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class Employee(BaseModel):
    id: int                                  # "101" gets converted to 101 (type coercion)
    name: str = Field(..., min_length=3)     # ... = required
    skills: List[str]
    department: Optional[str] = "General"    # optional, with a default
    salary: float = Field(..., ge=10000)     # ge = greater than or equal

    @field_validator("name")
    def name_title_case(cls, v):
        return v.title()
```

**Remember:**
- Use `:` for type hints, not `=` (`rate: float`, not `rate=float`)
- Invalid data raises `ValidationError`
- `field_validator` checks one field · `model_validator` checks several fields together · `computed_field` is a value calculated from other fields

**Why it matters for AI:** LLM output is untrusted. Pydantic checks it before your code uses it (structured output, tool arguments, FastAPI requests).

**Interview Qs:**
- Why use Pydantic with LLMs? → To validate untrusted LLM output against a strict schema.
- What's the difference between `field_validator` and `model_validator`? → One field vs the whole model.

**In my words:**

---

## LLM API calls + chat memory (foundations)

**What:** Sending messages to an LLM over an API and getting a reply.

**Key code (Groq):**
```python
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=20.0, max_retries=1)

messages = [
    {"role": "system", "content": "You are a senior backend engineer..."},   # persona / rules
    *history[-10:],                                                        # memory: last 10 messages
    {"role": "user", "content": question},
]
response = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages, temperature=0.2)
answer = response.choices[0].message.content
history.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer}])
```

**Remember:**
- **Roles:** `system` = rules and persona · `user` = the question · `assistant` = the model's earlier replies · `tool` = tool results
- **The LLM has no memory.** "Memory" means you resend the history every time, so cost grows with history length. That's why we keep only the last 10 messages.
- **API keys** go in environment variables (`os.getenv`), never in code
- `timeout` stops waiting forever · `max_retries` retries temporary failures

**Interview Qs:**
- Does the LLM remember earlier messages? → No. The client sends the whole history with each request.
- Why trim history? → Context window limits and cost, since every token is paid for on every call.

**In my words:**

---

## Structured output (Day 4)

**What:** Getting typed, validated data from an LLM instead of free text.

**How:**
```
text → LLM (JSON mode + schema in prompt) → JSON string → Pydantic validates → Python object
```

**Key code:**
```python
Resume.model_json_schema()                  # Pydantic: model → schema dict (tells the LLM the shape)
json.dumps(schema)                          # dict → string (to put it in the prompt)
response_format={"type": "json_object"}     # Groq: force a valid JSON reply
Resume.model_validate_json(raw)             # string → validated object, raises ValidationError
```

**Remember:**
- `json.dumps` = dict → string · `json.loads` = string → dict
- Validation checks **format and rules**, not **truth**. With `ge=10` in the schema, the LLM may invent `10` instead of the real `4`.

**Interview Qs:**
- How do you get reliable JSON from an LLM? → JSON mode + schema in the prompt + Pydantic validation + retry on failure.
- What if the JSON is valid but wrong? → Validation can't catch it; you need evals.

**In my words:**

---

## Streaming (Day 5)

**What:** Printing the reply chunk by chunk as it's generated, instead of all at once.

**Why:** Better **perceived** latency (time to first token). The total time is the same.

**Key code:**
```python
stream = client.chat.completions.create(..., stream=True)
answer = ""
for chunk in stream:
    text = chunk.choices[0].delta.content   # delta = the NEW piece (not .message)
    if text:                                # some chunks are None
        print(text, end="", flush=True)
        answer += text                      # keep the full reply for history
```

**Remember:** Groq is very fast, so streaming looks instant there. It matters more with slower models.

**Interview Qs:**
- Does streaming make the response faster? → No, it reduces time to first token, so it *feels* faster.
- How do you save a streamed reply to chat history? → Join the deltas into one string.

**In my words:**

---

## Tool calling (Day 9)

**What:** The LLM **asks** your code to run a function. It never runs code itself.

**How:**
```
1. You → LLM:  question + tool schemas (name, description, parameters)
2. LLM → You:  tool_calls = [name="multiply", arguments='{"a":12,"b":7}']
3. You:        json.loads(arguments) → run multiply(12, 7) → 84
4. You → LLM:  {"role": "tool", "tool_call_id": ..., "content": "84"}
5. LLM → You:  final answer
```

**Key code (Groq):**
```python
tool = {"type": "function", "function": {"name": ..., "description": ..., "parameters": {...JSON schema...}}}
message = response.choices[0].message
if message.tool_calls:                     # None when no tool is needed
    for call in message.tool_calls:
        call.function.name                 # "multiply"
        call.function.arguments            # a STRING → json.loads()
else:
    message.content                        # direct answer
```

**Remember:**
- The model picks a tool using only its **name, description and parameters**. A vague description ("does stuff") made it hesitate.
- `tool_calls` is `None` (not `[]`) when no tool is needed, so check before looping.

**Interview Qs:**
- Does the LLM execute the tool? → No. It returns a structured request; my code runs it.
- How does it choose which tool? → From the name, description and parameter schema.

**In my words:**

---

## Agent loop (Days 8, 10–11)

**What:** Tool calling repeated until the LLM gives a final answer. **Agent = LLM + tools + loop.**

**How:**
```
repeat (max_steps):
    call the LLM with messages + tools
    if no tool_calls → final answer → STOP
    else → run each tool → append {"role": "tool", ...} → loop again
```

**Remember:**
- The `id` on each tool call links the result back to the request (`tool_call_id`).
- Always set `max_steps`, or a confused agent can loop forever and burn money.
- Every step costs more, because the whole growing history is sent again.

**Interview Qs:**
- How does your code know the agent is done? → No `tool_calls` in the response.
- How do you stop infinite loops? → max steps, cost limit, detecting repeated identical calls.
- Why do frameworks like LangGraph exist? → They manage this loop, state and branching for you.

**In my words:**
