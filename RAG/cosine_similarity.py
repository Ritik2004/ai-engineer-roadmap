import math
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
    "Employees get 24 paid leaves per year.",
    "How many holidays do workers get?",
    "Work from home is allowed on Mondays and Fridays.",
    "The office has a new coffee machine.",
    "I love playing cricket on weekends.",
    "I love lionel messi",
    "I am not feeling well. Can i take 3 leave?"
]
embeddings = model.encode(sentences)
def cosine(a,b):
    dot = sum(x*y for x,y in zip(a,b))
    len_a = math.sqrt(sum(x * x for x in a))
    len_b = math.sqrt(sum(x * x for x in b))
    return dot / (len_a * len_b)


question = "How many leaves i can take in a year?"
q_vec = model.encode(question)

for sentence,vector in zip(sentences, embeddings):
    # print(f"{sentence},{vector[:5]}")
    score = cosine(q_vec,vector)
    # print(f"{score:.3f}{sentence}\n")
    if score>0.400:
        best_score = score
        best_sentence = sentence

print("\n Best match:",best_sentence)
