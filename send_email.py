import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv #pip install python-dotenv

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Rocky from the Future", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},

        I hope you're well. Don't forget that you're on the Shaolin Path.
        Here is your {amount} USD for {invoice_no} that is payment {due_date}.

        I would be really grateful if you could confirm this information.

        Best regards

        Rocky from the Future.            
        """
    )

    # Add the HTML version. This converts the message into a multipart/alternative
    # container, with the orginal text message as teh first part and the new html
    # message as the second part.

    msg.add_alternative(
        f"""\
        <html>
            <body>
                <p>Hi {name},</p>
        
                <p>I hope you're well. Don't forget that you're on the Shaolin Path.</p>
                <p>Here is your {amount} USD for {invoice_no} that is payment {due_date}.</p>
                <p>I would be really grateful if you could confirm this information.</p>
                <p>Best regards</p>
                <p>Rocky from the Future.</p>
            </body>
        </html>
        """,
        subtype="html"
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    

if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="John Doe",
        receiver_email="rocky.rasakith@gmail.com",
        due_date="11, Aug 2022",
        invoice_no="INV-21-21-009",
        amount="5",
    )