# Generated by Django 3.1.7 on 2021-03-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfig',
            name='enable_telegram',
            field=models.BooleanField(default=False),
        ),
    ]