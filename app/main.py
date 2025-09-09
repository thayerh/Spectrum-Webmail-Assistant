from imapUtils import *
from customData import *
from spamFilter import *


def main():
    IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD = load_env_variables()
    if not IMAP_SERVER or not EMAIL_ACCOUNT or not EMAIL_PASSWORD:
        print("Please set the IMAP_SERVER, EMAIL_ACCOUNT, and EMAIL_PASSWORD environment variables.")
        return

    spam_filter(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)

if __name__ == "__main__":
    main()