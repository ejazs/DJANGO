# Generated by Django 2.2.8 on 2020-01-14 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_app', '0007_auto_20200114_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
