import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)


def ask(prompt):
    response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role":"user",
                    "content":prompt
                }],
            )
    return response.choices[0].message.content;

# print("Without notes", ask("How many paid leaves do employees at Ritik Tech get?"))
# Context :Ritik Tech Pvt Ltd - Internal HR Policy
# - Employees get 24 paid leaves per year.
# - Work from home is allowed on Mondays and Fridays.
# - The office is closed on the last Friday of every month.
# - Laptop reimbursement limit is Rs 80,000.

# Question:How many paid leaves do employees at Ritik Tech get?
#  """
# print("with notes:", ask(rag_prompt))


# rag_prompt = f""" Answer ONLY using the context below. If the answer isn't there, say "I don't know"."""

company_notes = """
Ritik Tech Pvt Ltd - Internal HR Policy # type: ignore
- Employees get 24 paid leaves per year.
- Work from home is allowed on Mondays and Fridays.
- The office is closed on the last Friday of every month.
- Laptop reimbursement limit is Rs 80,000.
"""


def build_prompt(context,question):
    return f"""Answer only using the context below. If the answer is not there say "I don't know" 
Context:{context}
Question:{question}
"""

print("Q1:", ask(build_prompt(company_notes, "How many paid leaves do employees at Ritik Tech get?")))
print("Q2:", ask(build_prompt(company_notes, "What is the maternity leave policy?")))