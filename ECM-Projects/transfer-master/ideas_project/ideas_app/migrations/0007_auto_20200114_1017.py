# Generated by Django 2.2.8 on 2020-01-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_app', '0006_auto_20200114_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True),
        ),
    ]
