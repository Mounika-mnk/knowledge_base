import imaplib, email, ssl, smtplib, json
from email.header import decode_header
from email.message import EmailMessage
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# === Your Gmail credentials ===
EMAIL = "knowledgebaseagent6@gmail.com"
APP_PASSWORD = "xhdmivtxxfoigckn"

# === Load knowledge base ===
with open("knowledge_base.json") as f:
    kb = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute cluster embeddings
cluster_embeddings = []
for entry in kb:
    example_text = " ".join(entry["examples"])
    cluster_embeddings.append(model.encode([example_text])[0])

# === Connect to Gmail and fetch unread emails ===
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, APP_PASSWORD)
imap.select("inbox")
status, messages = imap.search(None, 'UNSEEN')
email_ids = messages[0].split()

print(f"\n📬 Found {len(email_ids)} unread emails\n")

for mail_id in email_ids:
    _, msg_data = imap.fetch(mail_id, "(RFC822)")
    for part in msg_data:
        if isinstance(part, tuple):
            msg = email.message_from_bytes(part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_email = email.utils.parseaddr(msg["From"])[1]

            # Extract plain text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            print(f"📨 From: {from_email}")
            print(f"Subject: {subject}")

            # === Match to known issue ===
            text = subject + ". " + body
            email_embedding = model.encode([text])[0]
            similarities = cosine_similarity([email_embedding], cluster_embeddings)[0]

            best_index = similarities.argmax()
            best_score = similarities[best_index]

            # === Threshold: Only match if similarity is strong enough ===
            if best_score > 0.6:
                reply_text = kb[best_index]["resolution"] 
            else:
                reply_text = (
                    "Thanks for reaching out. We've received your query and will get back to you shortly.\n\n"
                    "If your request is urgent, please contact our support team directly.\n\nThanks,\nSupport Team"
                )

            # === Send reply email ===
            reply = EmailMessage()
            reply["From"] = EMAIL
            reply["To"] = from_email
            reply["Subject"] = "Re: " + subject
            reply.set_content(reply_text)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as smtp:
                smtp.login(EMAIL, APP_PASSWORD)
                smtp.send_message(reply)

            print("✅ Sent reply:\n" + reply_text)
            print("-" * 50)

imap.logout()
