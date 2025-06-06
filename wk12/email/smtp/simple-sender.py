import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your email credentials
sender_email = "andrei.toma@ie.ase.ro"
receiver_email = "andrei.toma@nextlab.tech"
password = getpass.getpass("Email password: ")

# Create the MIME structure
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Hello from Python, live!"
body = "This is an example of sending an email from Python using SMTP."
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
