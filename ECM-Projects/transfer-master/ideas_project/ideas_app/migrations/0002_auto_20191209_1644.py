# Generated by Django 2.2.8 on 2019-12-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
