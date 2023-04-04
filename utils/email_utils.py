from flask import Flask
from flask_mail import Mail, Message
import os

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
    with app.app_context():
        msg = Message(subject="Invitation to join Music Group!",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["barile.francesco@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
    # https://www.lifewire.com/what-are-the-gmail-smtp-settings-1170854