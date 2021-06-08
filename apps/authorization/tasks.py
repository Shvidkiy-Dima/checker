from django.urls import reverse
from celery import shared_task
from utils.mail import send_email
from authorization.models import ConfirmationEmail


@shared_task
def send_conf_email(confirmation_email_id):
    conf_email = ConfirmationEmail.objects.filter(id=confirmation_email_id).first()
    if conf_email is None:
        return

    email = conf_email.email
    subject = conf_email.SUBJECT
    html_body = conf_email.HTML_BODY
    context = {'url': conf_email.link}
    send_email(email, subject, html_body, context=context)
