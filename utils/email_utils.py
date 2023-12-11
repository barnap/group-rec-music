from flask import Flask
from flask_mail import Mail, Message
import os

import config

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'grouprecexperiments@gmail.com',
    "MAIL_PASSWORD": 'GroupRec1986@'
}


app.config.update(mail_settings)
mail = Mail(app)

if __name__ == '__main__':
    # This is the test for sending e-mail from python app.
    # with app.app_context():
    #     msg = Message(subject="Invitation to join Music Group!",
    #                   sender=app.config.get("MAIL_USERNAME"),
    #                   recipients=["barile.francesco@gmail.com"], # replace with your email for testing
    #                   body="This is a test email I sent with Gmail and Python!")
    #     mail.send(msg)
    # # https://www.lifewire.com/what-are-the-gmail-smtp-settings-1170854
    friend_email = "barile.francesco86@gmail.com"
    current_user_email = "asd@asd.asd"
    mail

    email_address = friend_email
    email_subject = "Invitation to participate in a user study"
    email_message = config.INVITATION_EMAIL_TEXT.replace("<EmailFriend>", current_user_email) \
        .replace("<Host>", config.HOST).replace("<Port>", config.PORT)

    sender_email = "f.barile@maastrichtuniversity.nl" #config.mail_settings["MAIL_DEFAULT_SENDER"]
    # sender_password = config.mail_settings["MAIL_PASSWORD"]
    receiver_email = friend_email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_message, 'plain'))

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login(sender_email, sender_password)
    # server.sendmail(sender_email, receiver_email, message.as_string())

    server = smtplib.SMTP('smtp.maastrichtuniversity.nl', 25)
    server.send_message(message)
    server.quit()