# AI Email Support Agent

This project is an intelligent auto-reply agent that reads support emails from Gmail, identifies common issues, and automatically replies with helpful solutions — just like a human agent would.

---

## What This Agent Can Do

- Read unread emails from a Gmail inbox
- Match them to known issues using AI-based text similarity
- Automatically send the right resolution as a reply
- Add a polite “Thanks” message at the end
- Handle unknown issues with a fallback message
- Optionally show the knowledge base in a Streamlit web app

---

## Tech Stack

| Tool / Library         | Purpose                                 |
|------------------------|------------------------------------------|
| `imaplib`, `email`     | Read unread emails from Gmail            |
| `smtplib`, `ssl`       | Send automatic replies                   |
| `pandas`               | Handle email and KB data in CSV/JSON     |
| `sentence-transformers`| Compare email text using AI embeddings   |
| `scikit-learn` (KMeans)| Cluster similar support issues           |
| `streamlit`            | Web UI to view and manage the knowledge base |

---

## Folder Structure





---

## How It Works

1. **Prepare your Gmail**
   - Enable IMAP in Gmail settings
   - Create a Gmail App Password for access

2. **Train your knowledge base**
   - Run `build_knowledge_base.py` with sample emails
   - This clusters similar issues and creates `knowledge_base.json`

3. **Run the full agent**
   ```bash
   python3 support_agent_final.py
Reads new unread emails
Matches them to known issues
Sends the appropriate reply
Launch the web UI (optional)
streamlit run support_agent_ui.py
