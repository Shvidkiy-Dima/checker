# Generated by Django 3.1.7 on 2021-06-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20210612_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='by_email',
            field=models.BooleanField(default=False),
        ),
    ]
