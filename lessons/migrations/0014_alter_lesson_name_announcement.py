# Generated by Django 4.0 on 2021-12-19 23:31

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_attendance_date_now'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', ckeditor.fields.RichTextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('avaliable', models.BooleanField(default=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
    ]
