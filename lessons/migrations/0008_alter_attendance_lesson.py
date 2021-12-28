# Generated by Django 4.0 on 2021-12-17 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_message_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_lesson', to='lessons.lesson'),
        ),
    ]