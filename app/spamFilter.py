from app.imapUtils import connect_imap_ssl, login_to_mailbox, select_mailbox, search_all_emails, fetch_emails, process

def spam_filter(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD):
    ssl_connection = connect_imap_ssl(IMAP_SERVER, 993)
    if ssl_connection:
        login_to_mailbox(ssl_connection, EMAIL_ACCOUNT, EMAIL_PASSWORD)
        select_mailbox(ssl_connection, "INBOX")
        status, messages = search_all_emails(ssl_connection, date_since="01-Jan-2025", date_before="31-Dec-2025")
        if status == "OK":
            email_ids = messages[0].split()
            if email_ids:
                print(f"Found {len(email_ids)} emails.")
                msgs = fetch_emails(ssl_connection, email_ids, len(email_ids))
                for msg in msgs:
                    email_text, from_, subject, date_, body = process_email(msg)
                    # You can now use email_text for further processing
                    print(email_text)
            else:
                print("No emails found.")
        ssl_connection.logout()
