import os
import smtplib
import imghdr
from email.message import EmailMessage

class SendEmail():

    def __init__(self):
        self.username = os.environ.get("email_username")
        self.password = os.environ.get("email_password")
        self.server = os.environ.get("email_smtp_address")

    def email_content(self, to, cc, subject, body):
        self.msg = EmailMessage()
        self.msg["From"] = os.environ.get("email_from")
        self.msg["To"] = to
        self.msg["Cc"] = cc
        self.msg["Bcc"] = []
        self.msg["Subject"] = subject
        self.msg.set_content(body)

    def add_attachments(self, attachments):
        for file in attachments:
            with open(file, "rb") as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            self.msg.add_attachment(
                file_data,
                maintype="image",
                subtype=file_type,
                filename=file_name
            )

    def send_mail(self):
        with smtplib.SMTP_SSL(self.server, 465) as smtp:
            smtp.login(self.username, self.password)
            smtp.send_message(self.msg)
            print("Email sent")


if __name__ == '__main__':

    oEmail = SendEmail()

    oEmail.email_content(
        to="portfedh@gmail.com",
        cc="pablo.cruz.lemini@gmail.com",
        subject="TestSubject",
        body="This is a test message"
        )

    oEmail.add_attachments(["TipoDeCambio.png"])

    oEmail.send_email()