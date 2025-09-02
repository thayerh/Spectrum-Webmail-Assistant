import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import csv
from imapTest import connect_imap_ssl, login_to_mailbox, select_mailbox, search_all_emails, fetch_emails, process_email, load_env_variables

FILEPATH = 'model/data/personal_spam_ham.csv'

def prompt_classification():
    """Feeds emails to user for classification of spam or ham and saves to CSV."""
    msgs = get_emails()        
    with open(FILEPATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for msg in msgs:
            email_text, from_, subject, date_, body = process_email(msg)
            if email_text == "":
                continue
            print(f"From: {from_}")
            print(f"Subject: {subject}")
            print(f"Date: {date_}")
            print(f"Body: {body[:200]}...")  # Print first 200 characters of the body
            classification = input("Classify this email as (spam=1/ham=0): ").strip().lower()
            while classification not in ['1', '0']:
                classification = input("Invalid input. Please classify as (spam=1/ham=0): ").strip().lower()
            writer.writerow([0, "spam" if classification == '1' else "ham", email_text, classification])
            print("Email classified and saved.\n")
        

def get_emails():
    IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD = load_env_variables()
    ssl_connection = connect_imap_ssl(IMAP_SERVER, 993)
    if ssl_connection:
        login_to_mailbox(ssl_connection, EMAIL_ACCOUNT, EMAIL_PASSWORD)
        select_mailbox(ssl_connection, "INBOX")
        status, messages = search_all_emails(ssl_connection, date_since="18-Aug-2025", date_before="18-Aug-2025")
        if status == "OK":
            email_ids = messages[0].split()
            if email_ids:
                print(f"Found {len(email_ids)} unseen emails.")
                return fetch_emails(ssl_connection, email_ids, len(email_ids))
            else:
                print("No new emails found.")
                return []
        ssl_connection.logout()
    return []