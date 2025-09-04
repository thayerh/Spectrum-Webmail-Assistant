from imapTest import *
IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD = load_env_variables()

from customData import *


# mail = connect_to_mailbox(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
ssl_connection = connect_imap_ssl(IMAP_SERVER, 993)
if ssl_connection:
    login_to_mailbox(ssl_connection, EMAIL_ACCOUNT, EMAIL_PASSWORD)
    select_mailbox(ssl_connection, "INBOX")
    status, messages = search_unseen_emails(ssl_connection)
    # status, messages = search_all_emails(ssl_connection, "01-Aug-2025")
    if status == "OK":
        email_ids = messages[0].split()
        if email_ids:
            # print(f"Found {len(email_ids)} emails.")
            msgs = fetch_emails(ssl_connection, email_ids)
            for msg in msgs:
                email_text, from_, subject, date_, body = process_email(msg)
                # You can now use email_text for further processing
                print(email_text)
        else:
            print("No new emails found.")
    ssl_connection.logout()