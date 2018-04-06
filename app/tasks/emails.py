from app import celery
from flask_sendgrid import SendGrid
from flask import current_app
from flask import request


@celery.task(bind=True)
def send(self, from_email, to_email, subject, text):
    with current_app.app_context():
        sg = SendGrid(current_app)
        sg.send_email(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            text=text)
