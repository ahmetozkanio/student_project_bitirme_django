# Generated by Django 4.0 on 2021-12-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=128, null=True),
        ),
    ]