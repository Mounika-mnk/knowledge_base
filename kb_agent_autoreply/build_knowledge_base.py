import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import json

# Load CSV
df = pd.read_csv("simulated_support_emails.csv")
df["text"] = df["email_subject"] + ". " + df["email_body"]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

# Cluster similar issues
NUM_CLUSTERS = 3
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
df["cluster"] = kmeans.fit_predict(embeddings)

# Build knowledge base
knowledge_base = []
for cluster_id in sorted(df["cluster"].unique()):
    cluster_df = df[df["cluster"] == cluster_id]
    resolution = cluster_df["support_reply"].mode()[0]  # most frequent reply
    sample_subjects = cluster_df["email_subject"].tolist()[:3]
    
    knowledge_base.append({
        "cluster_id": int(cluster_id),
        "example_subjects": sample_subjects,
        "resolution": resolution
    })

# Save to JSON
with open("knowledge_base.json", "w") as f:
    json.dump(knowledge_base, f, indent=2)

print("✅ Knowledge base saved to knowledge_base.json")
