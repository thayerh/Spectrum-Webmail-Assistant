import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import ssl
from bs4 import BeautifulSoup
import email.message
from model.utils.transformText import transform_text


def load_env_variables():
    """Load environment variables for IMAP connection."""
    load_dotenv()
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    return IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD

def select_mailbox(mail, mailbox="INBOX"):
    """Select mailbox in readonly mode."""
    mail.select(mailbox, readonly=True)

def search_unseen_emails(mail):
    """Search for unseen (new) emails."""
    status, messages = mail.search(None, 'UNSEEN')
    return status, messages

def search_all_emails(mail, date_since="01-Jan-2025", date_before="31-Dec-2025"):
    """Search for all emails since a specific date."""
    status, messages = mail.search(None, f'SINCE {date_since} BEFORE {date_before}')
    return status, messages

def search_by_criteria(mail, criteria):
    """Search emails by specific criteria."""
    status, messages = mail.search(None, criteria)
    return status, messages

def fetch_emails(mail, email_ids, limit=8):
    """Fetch emails by IDs."""
    msgs = []
    for email_id in email_ids[::-1][:limit]:  # Process in reverse order (newest first)
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        if res != "OK":
            print(f"Failed to fetch email ID {email_id}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        msgs.append(msg)
    return msgs

def process_email(msg: email.message.Message):
    try:
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from_ = msg.get("From")
        date_ = msg.get("Date")

        # Get email body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                elif content_type == "multipart/alternative":
                    for subpart in part.get_payload():
                        if subpart.get_content_type() == "text/plain":
                            body += subpart.get_payload(decode=True).decode('utf-8', errors='replace')
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    soup = BeautifulSoup(html_content, "html.parser")
                    body += soup.get_text()
        else:
            if msg.get_content_type() == "text/plain":
                body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
            elif msg.get_content_type() == "text/html":
                html_content = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                soup = BeautifulSoup(html_content, "html.parser")
                body = soup.get_text()

        # Remove excessive whitespace and newlines
        body = ' '.join(body.split())
        # Remove urls
        body = ' '.join(word for word in body.split() if not word.startswith('http'))
        body = ' '.join(word for word in body.split() if not word.startswith('<http'))
        # Process email for text analysis
        transformed_subject = transform_text(subject)
        transformed_body = transform_text(body)
        email_text = f"Subject: {transformed_subject}\n{transformed_body}"

        return email_text, from_, subject, date_, body
    except Exception as e:
        print(f"Error processing email: {e}")
        return "", "", "", "", ""

def connect_imap_ssl(hostname, port=993) -> imaplib.IMAP4_SSL:
    try:
        # Create context that matches the working OpenSSL session
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        
        # Force TLS 1.2 (like the working session)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        
        # Set the exact cipher that worked: AES256-SHA256
        context.set_ciphers('AES256-SHA256')
        
        # Match other SSL options
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_default_certs()

        
        # Connect using IMAP4_SSL
        mail = imaplib.IMAP4_SSL(hostname, port, ssl_context=context)
        print(f"✓ IMAP SSL connection successful to {hostname}:{port}")
        
        # You would normally login here: mail.login(username, password)
        
        return mail
        
    except Exception as e:
        print(f"IMAP connection failed: {e}")
        return None

def login_to_mailbox(mail, email_account, email_password):
    """Login to the mailbox."""
    try:
        mail.login(email_account, email_password)
        print("Login successful")
    except imaplib.IMAP4.error as e:
        print(f"Login failed: {e}")