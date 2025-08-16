import imaplib
import email
from email.header import decode_header
import pandas as pd

# === Your Gmail credentials ===
EMAIL = "knowledgebaseagent6@gmail.com"            # Replace with your Gmail
APP_PASSWORD = "xhdmivtxxfoigckn"  # Paste App Password here

# === Connect to Gmail IMAP ===
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, APP_PASSWORD)
imap.select("inbox")

# === Search for unread emails ===
status, messages = imap.search(None, 'UNSEEN')
email_ids = messages[0].split()

print(f"📬 Found {len(email_ids)} unread emails\n")

emails = []

for mail_id in email_ids:
    _, msg_data = imap.fetch(mail_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            # Extract plain text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            emails.append({"subject": subject.strip(), "body": body.strip()})
            print(f"📨 Subject: {subject.strip()}")
            print(f"📝 Body (truncated): {body.strip()[:150]}...\n")

imap.logout()

# Save to CSV for now
if emails:
    df = pd.DataFrame(emails)
    df.to_csv("new_unread_emails.csv", index=False)
    print("✅ Saved unread emails to new_unread_emails.csv")
else:
    print("✅ No unread emails found.")
