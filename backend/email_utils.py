import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
import os

# SMTP Configuration
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "quizmaster@noreply.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message, content="html", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    # Attach message body (HTML or plain text)
    msg.attach(MIMEText(message, content))

    # Attach file (if provided)
    if attachment_file and os.path.exists(attachment_file):
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_file)}")
        msg.attach(part)

    
    server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    if SENDER_PASSWORD:  # Only login if a password is set
        server.starttls()
        server.login(SENDER_ADDRESS, SENDER_PASSWORD)

    server.sendmail(SENDER_ADDRESS, to_address, msg.as_string())
    server.quit()
    print(f"Email sent to {to_address} with subject: {subject}")
    return True