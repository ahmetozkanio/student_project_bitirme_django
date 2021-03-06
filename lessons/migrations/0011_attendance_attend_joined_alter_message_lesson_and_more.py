# Generated by Django 4.0 on 2021-12-19 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0010_alter_message_lesson_alter_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attend_joined',
            field=models.ManyToManyField(blank=True, related_name='attendance_joined', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Mesajiniz'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
