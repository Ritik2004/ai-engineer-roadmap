from pydantic import BaseModel,Field, ValidationError
from typing import List,Optional
import os,json
from groq import Groq

class Resume(BaseModel):
    name:str
    years_experience:int=Field(...,ge=10)
    skills:List[str]
    email:Optional[str]=None

resume_text = """
Hi, I'm Priya Sharma. I've been working as a backend developer for about
4 years, mostly with Python, FastAPI and PostgreSQL. Recently I've started
using Docker and AWS too. You can reach me at priya.sharma@example.com.
"""

client = Groq(
    api_key = os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages = [
        {
            "role":"system",
            "content":"Extract resume details. Reply only with JSON matching this schema" 
            + json.dumps(Resume.model_json_schema()),
        },
        {
            "role":"user","content":resume_text,
        }
    ],
    response_format={"type":"json_object"}
)

raw = response.choices[0].message.content

try:
    resume = Resume.model_validate_json(raw)
    print("Name:", resume.name)
    print("Skills:", resume.skills)
    print("Years:", resume.years_experience)
except ValidationError as e:
    print("Invalid data from LLM:", e)

