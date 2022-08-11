import os

from celery import Celery

from src.app.auth.send_email import send_new_account_email, send_reset_password_email
from src.config.settings import CELERY_RESULT_BACKEND, CELERY_BROKER_URL

app = Celery(__name__)
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', CELERY_BROKER_URL)
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', CELERY_RESULT_BACKEND)


@app.task(name='send_register_email')
def send_register_email(email_to: str, username: str, password: str, uuid: str):
    send_new_account_email(email_to, username, password, uuid)


@app.task(name='send_recover_email')
def send_recover_email(email_to: str, email: str, token: str):
    send_reset_password_email(email_to, email, token)
