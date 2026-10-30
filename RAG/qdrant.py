# 1. IMPORTS
import os
from groq import Groq
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


# 2. SETUP (clients + model)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)
model = SentenceTransformer("all-MiniLM-L6-v2")
db = QdrantClient(path="./qdrant_db")  # a database saved to disk (no server needed)


# 3. DATA + FUNCTIONS
document = """Ritik Tech Pvt Ltd - HR Policy. Employees get 24 paid leaves per year. \
Unused leaves can be carried forward up to 10 days. Sick leave is separate and allows \
12 days per year with a doctor's note. Work from home is allowed on Mondays and Fridays. \
Employees must be online between 10 AM and 4 PM on WFH days. The office is closed on \
the last Friday of every month. Laptop reimbursement limit is Rs 80,000, claimable once \
every 3 years. Internet bills up to Rs 1,000 per month are reimbursed for remote work. \
Health insurance covers employees and their parents up to Rs 5 lakh per year."""


def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def ask(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )
    return response.choices[0].message.content


def build_prompt(context, question):
    return f"""Answer only using the context below. If the answer is not there say "I don't know"
Context:{context}
Question:{question}
"""


# 4. INDEXING (store the chunks in Qdrant)
chunks = chunk_text(document, chunk_size=150, overlap=50)
chunk_vectors = model.encode(chunks)

# create a collection, telling it the vector size + similarity metric
if not db.collection_exists("hr_policy"):
    db.create_collection(
        collection_name="hr_policy",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

db.upsert(
    collection_name="hr_policy",
    points=[
        PointStruct(
            id=i,
            vector=chunk_vectors[i].tolist(),
            payload={"text": chunks[i], "source": "hr_policy.txt"},   # payload = metadata
        )
        for i in range(len(chunks))
    ],
)
print("Stored:", db.count("hr_policy").count, "chunks")


# 5. RETRIEVE + RAG
def retrieve(question, k=2):
    q_vec = model.encode(question).tolist()
    results = db.query_points(collection_name="hr_policy", query=q_vec, limit=k).points  # TODO: fill the blank
    return [point.payload["text"] for point in results]                                       # TODO: fill the blank


def rag(question):
    top_chunks = retrieve(question)
    context = ""
    for chunk in top_chunks:
        context += chunk + "\n\n"
    return ask(build_prompt(context, question))


# 6. RUN
print("Q1:", rag("How much internet bill is reimbursed?"))
print("Q2:", rag("Can I carry forward unused leaves?"))
print("Q3:", rag("What is the dress code?"))
