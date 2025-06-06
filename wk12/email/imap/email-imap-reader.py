import imaplib
import getpass
import email
from email.parser import BytesParser

# Email credentials and IMAP server configuration
imap_host = 'imap.gmail.com'  
username = "andrei.toma@ie.ase.ro"
password = getpass.getpass("Email password: ")

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_host)

# Login to the server
mail.login(username, password)

# Select the mailbox you want to use (inbox by default)
mail.select("inbox")  # You can switch to another folder e.g., "Sent"

# Search for specific emails (e.g., all unread emails)
status, email_ids = mail.search(None, 'UNSEEN')

# Fetch emails by their IDs (get the latest email for example)
if email_ids[0]:  # Make sure there's at least one email
    latest_email_id = email_ids[0].split()[-1]
    status, data = mail.fetch(latest_email_id, '(RFC822)')  # Fetch the full email

    # Parse the email content
    raw_email = data[0][1]
    parsed_email = BytesParser().parsebytes(raw_email)

    # Print email details
    print("From: ", parsed_email['from'])
    print("Subject: ", parsed_email['subject'])
    print("Body: ", parsed_email.get_payload(decode=True))

# Logout from the server
mail.close()
mail.logout()
