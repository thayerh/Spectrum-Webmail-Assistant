from imapUtils import connect_imap_ssl, login_to_mailbox, move_to_spam, select_mailbox, search_by_criteria, fetch_emails, process_email
import json
from model.utils.classifySpam import classify_email_spam, vectorize
import email.message

CONFIG_FILE = "app/model/utils/config.json"

def load_state():
    try:
        with open(CONFIG_FILE, 'r') as cf:
            with open(json.load(cf).get("state-file"), 'r') as sf:
                return json.load(sf)
    except FileNotFoundError:
        return {"last_uid": None}

def save_state(state):
    with open(CONFIG_FILE, 'r') as cf:
        # Make state file if not present
        with open(json.load(cf).get("state-file"), 'w') as sf:
            json.dump(state, sf)

def load_whitelist():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f).get("whitelist", [])
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
        search_criteria = "SINCE 06-Aug-2025" if last_uid is None else f"(UID {last_uid}:*)"

        status, messages = search_by_criteria(ssl_connection, search_criteria)
        if status == "OK":
            email_ids = messages[0].split()
            if email_ids:
                print(f"Found {len(email_ids)} emails.")
                msgs = fetch_emails(ssl_connection, email_ids, len(email_ids))
                try:
                    for email_id, msg in msgs:
                        email_text, from_, subject, date_, body = process_email(msg)

                        whitelisted = False
                        lower_text = email_text.lower()
                        for keyword in WHITELIST_KEYWORDS:
                            if keyword.lower() in lower_text:
                                whitelisted = True # Skip whitelisted emails
                                break
                        if not whitelisted:
                            # Vectorize and classify the email_text
                            email_vector = vectorize(email_text)
                            spam = classify_email_spam(email_vector)

                            if spam >= 8:
                                print(f"Moving email with subject '{subject}' to spam (spam score: {spam})")
                                move_to_spam(ssl_connection, email_id)

                        # Update the last processed UID
                        last_uid = email_id.decode()
                        save_state({"last_uid": last_uid})
                except Exception as e:
                    print(f"Error processing emails: {e}")
            else:
                print("No emails found.")
        ssl_connection.logout()

