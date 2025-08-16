import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Paths to the knowledge base and unread emails
KB_PATH = Path("knowledge_base.json")
EMAILS_PATH = Path("new_unread_emails.csv")

# Load knowledge base
def load_knowledge_base():
    if KB_PATH.exists():
        with open(KB_PATH, "r") as f:
            return json.load(f)
    return {}

# Load unread emails
def load_unread_emails():
    if EMAILS_PATH.exists():
        return pd.read_csv(EMAILS_PATH)
    return pd.DataFrame()

# UI
st.set_page_config(page_title="AI Support Agent Dashboard", layout="wide")
st.title("📬 AI Support Agent Dashboard")

# Tabs for navigation
tabs = st.tabs(["📩 Unread Emails", "🧠 Knowledge Base", "➕ Add Resolution"])

# --- Tab 1: View Unread Emails ---
with tabs[0]:
    st.subheader("Unread Emails")
    df = load_unread_emails()
    if df.empty:
        st.info("No unread emails available.")
    else:
        st.dataframe(df, use_container_width=True)

# --- Tab 2: View Knowledge Base ---
with tabs[1]:
    st.subheader("Knowledge Base")
    kb = load_knowledge_base()
    if not kb:
        st.info("Knowledge base is empty.")
    else:
        kb_df = pd.DataFrame([
            {"Example Subjects": ", ".join(k["examples"]), "Resolution": k["resolution"]}
            for k in kb
        ])
        st.dataframe(kb_df, use_container_width=True)

# --- Tab 3: Add Resolution ---
with tabs[2]:
    st.subheader("Add New Issue Type")
    new_examples = st.text_area("Example Subjects (comma-separated)")
    new_resolution = st.text_area("Resolution Text")

    if st.button("Add to Knowledge Base"):
        if new_examples.strip() and new_resolution.strip():
            kb = load_knowledge_base()
            new_id = str(len(kb))
            kb[new_id] = {
                "examples": [e.strip() for e in new_examples.split(",")],
                "resolution": new_resolution.strip()
            }
            with open(KB_PATH, "w") as f:
                json.dump(kb, f, indent=2)
            st.success("New entry added to the knowledge base!")
        else:
            st.warning("Please fill out both fields before submitting.")
