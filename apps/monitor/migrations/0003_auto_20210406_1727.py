# Generated by Django 3.1.7 on 2021-04-06 17:27

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20210325_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_log_rotation', models.IntegerField(default=300000)),
                ('free_log_rotation', models.IntegerField(default=20000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='monitor',
            name='last_error_notification',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='interval',
            field=models.DurationField(validators=[django.core.validators.MinValueValidator(datetime.timedelta(seconds=60)), django.core.validators.MaxValueValidator(datetime.timedelta(seconds=3600))]),
        ),
    ]