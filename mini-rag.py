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


def build_prompt(context,question):
    return f"""Answer only using the context below. If the answer is not there say "I don't know" 
Context:{context}
Question:{question}
"""


document = """Ritik Tech Pvt Ltd - HR Policy. Employees get 24 paid leaves per year. \
Unused leaves can be carried forward up to 10 days. Sick leave is separate and allows \
12 days per year with a doctor's note. Work from home is allowed on Mondays and Fridays. \
Employees must be online between 10 AM and 4 PM on WFH days. The office is closed on \
the last Friday of every month. Laptop reimbursement limit is Rs 80,000, claimable once \
every 3 years. Internet bills up to Rs 1,000 per month are reimbursed for remote work. \
Health insurance covers employees and their parents up to Rs 5 lakh per year."""


# chunking
def chunk_text(text,chunk_size,overlap):
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunks.append(text[start:end])
        start=end-overlap
    return chunks

chunks = chunk_text(document,chunk_size=150,overlap=10)



# embedding + cosine similarity

import math
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_vectors = model.encode(chunks)

def cosine(a,b):
    dot = sum(x*y for x,y in zip(a,b))
    len_a = math.sqrt(sum(x * x for x in a))
    len_b = math.sqrt(sum(y * y for y in b))
    return dot/(len_a*len_b)


# it is used to retrieve topk chunk which are closest to our content

def retrieve(question,k=2):
    q_vec = model.encode(question)

    scored=[]
    for chunk,vec in zip(chunks, chunk_vectors):
        score = cosine(q_vec,vec)
        scored.append((score,chunk))

    scored.sort(reverse=True)
    return [chunk for score,chunk in scored[:k]]


def rag(question):
    top_chunks = retrieve(question)
    context = ""
    for chunk in top_chunks:
        context+=chunk+"\n\n"
    return ask(build_prompt(context,question))

print("Q1:", rag("How much internet bill is reimbursed?"))
print("Q2:", rag("Can I carry forward unused leaves?"))
print("Q3:", rag("What is the dress code?"))
print("Q4:", rag("Who is my favouritr football player?"))


