# Generated by Django 4.0 on 2021-12-14 15:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0002_lesson_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='lesson_joined', to=settings.AUTH_USER_MODEL),
        ),
    ]
