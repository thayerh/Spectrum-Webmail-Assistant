from imapTest import *
IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD = load_env_variables()

# mail = connect_to_mailbox(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
ssl_connection = connect_imap_ssl(IMAP_SERVER, 993)
if ssl_connection:
    ssl_connection.logout()


print("Hello from Docker`s Python container!")