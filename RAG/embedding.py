from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Employees get 24 paid leaves per year.",
    "How many holidays do workers get?",
    "Work from home is allowed on Mondays and Fridays.",
    "The office has a new coffee machine.",
    "I love playing cricket on weekends.",
]

embeddings = model.encode(sentences)
print(type(embeddings))
# print(embeddings.shape)
print(embeddings[0][:5])
# print(embeddings[1])