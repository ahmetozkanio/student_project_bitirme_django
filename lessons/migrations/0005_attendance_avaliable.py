# Generated by Django 4.0 on 2021-12-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='avaliable',
            field=models.BooleanField(default=True),
        ),
    ]