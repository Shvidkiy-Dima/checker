# Generated by Django 3.1.7 on 2021-03-22 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('keyword', models.CharField(blank=True, default=None, max_length=124, null=True)),
                ('monitor_type', models.PositiveSmallIntegerField(choices=[(0, 'HTTP-HTTPS'), (1, 'Check HTML')])),
                ('last_request', models.DateTimeField(blank=True, default=None, null=True)),
                ('next_request', models.DateTimeField()),
                ('interval', models.DurationField()),
                ('url', models.URLField()),
                ('name', models.CharField(max_length=124)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monitors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonitorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('response_code', models.IntegerField()),
                ('response_time', models.FloatField()),
                ('keyword', models.BooleanField(blank=True, default=None, null=True)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
