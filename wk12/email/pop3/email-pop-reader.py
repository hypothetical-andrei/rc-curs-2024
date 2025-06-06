import poplib
import getpass
from email import parser
from email.parser import Parser

# Email credentials and POP3 server configuration
pop3_server = 'pop.gmail.com'
username = "andrei.toma@ie.ase.ro"
password = getpass.getpass("Email password: ")

# Connect to the POP3 server
mail = poplib.POP3_SSL(pop3_server)
mail.user(username)
mail.pass_(password)

# Get statistics on the number of emails and total size
numMessages = len(mail.list()[1])
print(f"Total emails: {numMessages}")

# Fetch the latest email
latest_email_number = numMessages  # Adjust this to fetch a specific email number
response, lines, bytes = mail.retr(latest_email_number)

# Concatenate message lines and parse into an email object
message = b"\r\n".join(lines).decode('utf-8')
parsed_email = Parser().parsestr(message)

# Display the email details
print("From: ", parsed_email['from'])
print("Subject: ", parsed_email['subject'])
print("Body: ", parsed_email.get_payload())

# Logout from the server
mail.quit()
