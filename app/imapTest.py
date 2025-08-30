import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import ssl

def load_env_variables():
    """Load environment variables for IMAP connection."""
    load_dotenv()
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    print(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
    return IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD

def connect_to_mailbox(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD):
    """Connect and login to the IMAP server."""
    mySsl = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=993, ssl_context=mySsl)
    exit()
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    return mail

def select_mailbox(mail, mailbox="INBOX"):
    """Select mailbox in readonly mode."""
    mail.select(mailbox, readonly=True)

def search_unseen_emails(mail):
    """Search for unseen (new) emails."""
    status, messages = mail.search(None, 'UNSEEN')
    return status, messages

def fetch_and_print_emails(mail, email_ids):
    """Fetch and print details of emails by IDs."""
    for email_id in email_ids:
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        if res != "OK":
            print(f"Failed to fetch email ID {email_id}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from_ = msg.get("From")
        date_ = msg.get("Date")

        print(f"From: {from_}")
        print(f"Subject: {subject}")
        print(f"Date: {date_}")
        print("-" * 50)


import ssl
import socket

def connect_ssl(hostname, port):
    # Create a regular socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap it with SSL
    context = ssl.create_default_context()
    ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
    
    try:
        # Connect to the server
        ssl_sock.connect((hostname, port))
        
        # Print connection info
        print(f"Connected to {hostname}:{port}")
        print(f"SSL version: {ssl_sock.version()}")
        print(f"Cipher: {ssl_sock.cipher()}")
        
        # Get certificate info
        cert = ssl_sock.getpeercert()
        print(f"Certificate subject: {cert.get('subject')}")
        print(f"Certificate issuer: {cert.get('issuer')}")
        
        return ssl_sock
        
    except Exception as e:
        print(f"Connection failed: {e}")
        ssl_sock.close()
        return None
    

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
