# Generated by Django 4.0 on 2021-12-31 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0018_alter_attendance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='user_joined',
            field=models.ManyToManyField(blank=True, null=True, related_name='attendance_joined', to='lessons.Lesson'),
        ),
    ]