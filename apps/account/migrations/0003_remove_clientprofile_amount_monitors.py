# Generated by Django 3.1.7 on 2021-04-13 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_telegram_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientprofile',
            name='amount_monitors',
        ),
    ]