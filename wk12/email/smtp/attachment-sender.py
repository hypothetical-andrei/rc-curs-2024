import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email credentials and setup
sender_email = "andrei.toma@ie.ase.ro"
receiver_email = "andrei.toma@nextlab.tech"
password = getpass.getpass("Email password: ")
subject = "Email with Attachment from Python"

# Create MIME message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Email body
body = "This email contains an attachment sent from Python using SMTP."
message.attach(MIMEText(body, 'plain'))

# Specify the attachment file path
file_path = "./cat.jpg"  # Change this to your file path

# Open the file to be sent
with open(file_path, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    'Content-Disposition',
    f"attachment; filename= {file_path}",
)

# Attach the file to the message
message.attach(part)

# Send the email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
