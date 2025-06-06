import smtplib

sender = 'from@example.com'
receivers = ['to@example.com']

message = """From: From Person <from@example.com>
To: To Person <to@example.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP('localhost', 1025)
    smtpObj.sendmail(sender, receivers, message)
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print("Error: unable to send email", e)
