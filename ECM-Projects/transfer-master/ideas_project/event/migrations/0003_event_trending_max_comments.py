# Generated by Django 2.2.8 on 2019-12-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20191214_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='trending_max_comments',
            field=models.IntegerField(default=0),
        ),
    ]
