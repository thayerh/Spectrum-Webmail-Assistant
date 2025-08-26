import imaplib
import email
from email.header import decode_header
import os

# -- Load environment variables ---
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --- Connect to the server ---
mail = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=993)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)


exit()
# --- Select mailbox (readonly to avoid marking emails as read) ---
mail.select("INBOX", readonly=True)

# --- Search for unseen (new) emails ---
status, messages = mail.search(None, 'UNSEEN')

if status == "OK":
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} new email(s)")

    for email_id in email_ids:
        # Fetch the email by ID
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        if res != "OK":
            print(f"Failed to fetch email ID {email_id}")
            continue

        # Parse email content
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Decode email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Get sender
        from_ = msg.get("From")
        date_ = msg.get("Date")

        print(f"From: {from_}")
        print(f"Subject: {subject}")
        print(f"Date: {date_}")
        print("-" * 50)

else:
    print("Failed to search inbox.")

mail.logout()
