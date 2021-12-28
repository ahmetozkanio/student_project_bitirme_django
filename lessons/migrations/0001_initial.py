# Generated by Django 4.0 on 2021-12-14 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(default='lessons/default_lesson_image.png', upload_to='lessons/%Y/%m/%d/')),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('avaliable', models.BooleanField(default=True)),
            ],
        ),
    ]