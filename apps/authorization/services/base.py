from django.db import transaction
from account.models import User


@transaction.atomic
def confirm(confirmation_email):
    if User.objects.by_email(confirmation_email.email).exists():
        return

    confirmation_email.status = confirmation_email.CONFIRMED
    user = User.objects.make_client(confirmation_email.email, confirmation_email.password)
    confirmation_email.user = user
    confirmation_email.save(updae_fields=['user', 'status'])
