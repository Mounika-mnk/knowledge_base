import smtplib
import ssl
from email.message import EmailMessage

# === Email credentials ===
EMAIL = "knowledgebaseagent6@gmail.com"              
APP_PASSWORD = "xhdmivtxxfoigckn" 
# === Reply details ===
TO = "mounikaboppudi8@gmail.com"  # Replace with the real sender's email
SUBJECT = "Re: Test password issue"
BODY = "Please reset your password using this secure link: https://reset.example.com"

# === Build email ===
msg = EmailMessage()
msg["From"] = EMAIL
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.set_content(BODY)

# === Send via Gmail SMTP ===
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)

print("✅ Email reply sent successfully!")
