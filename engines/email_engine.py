import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS
)


def send_email(to_email, subject, body):

    msg = MIMEMultipart()

    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.starttls()

        server.login(SMTP_USER, SMTP_PASS)

        server.sendmail(
            SMTP_USER,
            to_email,
            msg.as_string()
        )

        server.quit()

        return True, "Email sent successfully."

    except Exception as e:
        return False, str(e)