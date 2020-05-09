# Generated by Django 3.0.5 on 2020-04-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0003_trackinglog_sys_uptime'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackinglog',
            name='idle_duration',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='trackinglog',
            name='idle_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='trackinglog',
            name='idle_start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
