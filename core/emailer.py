import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(
    smtp_server,
    port,
    sender,
    password,
    recipient,
    subject,
    body
):

    msg = MIMEMultipart()

    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_server, port)

    server.starttls()

    server.login(sender, password)

    server.sendmail(
        sender,
        recipient,
        msg.as_string()
    )

    server.quit()