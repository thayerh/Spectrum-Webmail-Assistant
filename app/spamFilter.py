from imapUtils import connect_imap_ssl, login_to_mailbox, select_mailbox, search_by_criteria, fetch_emails, process_email
import json
from model.utils.classifySpam import classify_email_spam, vectorize

STATE_FILE = "/var/lib/spectrum_webmail_filter/state.json"

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_uid": None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def load_whitelist():
    try:
        with open("app/model/utils/whitelist.json", 'r') as f:
            return json.load(f).get("keywords", [])
    except FileNotFoundError:
        return []


def spam_filter(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD):
    WHITELIST_KEYWORDS = load_whitelist()

    ssl_connection = connect_imap_ssl(IMAP_SERVER, 993)
    if ssl_connection:
        login_to_mailbox(ssl_connection, EMAIL_ACCOUNT, EMAIL_PASSWORD)
        select_mailbox(ssl_connection, "INBOX")

        state = load_state()
        last_uid = state.get("last_uid")
        # Get all emails since last processed UID
        search_criteria = "SINCE 01-Sep-2025" if last_uid is None else f"(UID {last_uid}:*)"

        status, messages = search_by_criteria(ssl_connection, search_criteria)
        if status == "OK":
            email_ids = messages[0].split()
            if email_ids:
                print(f"Found {len(email_ids)} emails.")
                msgs = fetch_emails(ssl_connection, email_ids, len(email_ids))
                for msg in msgs:
                    email_text, from_, subject, date_, body = process_email(msg)
                    
                    whitelisted = False
                    lower_text = email_text.lower()
                    for keyword in WHITELIST_KEYWORDS:
                        if keyword.lower() in lower_text:
                            print(f"Whitelisted email with subject '{subject}'")
                            whitelisted = True # Skip whitelisted emails
                            break
                    if whitelisted:
                        continue

                    # Vectorize and classify the email_text
                    email_vector = vectorize(email_text)
                    print(classify_email_spam(email_vector), subject)
            else:
                print("No emails found.")
        ssl_connection.logout()

