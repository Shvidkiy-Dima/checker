from typing import Union
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http.request import HttpRequest
from django.utils.translation import override


def send_email(to: Union[str, list], subject_template: str,
               html_body_template: str,
               context: Union[dict, None] = None,
               request: Union[HttpRequest, None] = None,
               language: Union[str, None] = None):

    context = context or {}
    context.setdefault('STATIC_HOST', settings.API_HOST)
    with override(language):
        subject = render_to_string(subject_template, context,
                                   request=request).strip()

        html_body = render_to_string(html_body_template, context,
                                     request=request)

    msg = EmailMultiAlternatives(
        to=to if isinstance(to, list) else [to],
        subject=subject
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
