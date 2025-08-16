import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the knowledge base
with open("knowledge_base.json") as f:
    knowledge_base = json.load(f)

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute embeddings of each cluster's example subjects
cluster_embeddings = []
for entry in knowledge_base:
    examples_text = " ".join(entry["example_subjects"])
    embedding = model.encode([examples_text])[0]
    cluster_embeddings.append(embedding)

# Load new emails
df = pd.read_csv("new_unread_emails.csv")

# Process each new email
for index, row in df.iterrows():
    subject = str(row["subject"])
    body = str(row["body"])
    text = subject + ". " + body
    embedding = model.encode([text])[0]

    # Match to cluster
    similarities = cosine_similarity([embedding], cluster_embeddings)[0]
    best_match_idx = similarities.argmax()
    best_entry = knowledge_base[best_match_idx]

    print(f"\n📨 Email: {subject}")
    print("🧠 Matched cluster:", best_entry["example_subjects"])
    print("✅ Auto-reply:\n" + best_entry["resolution"])
    print("\n" + "-"*50)
