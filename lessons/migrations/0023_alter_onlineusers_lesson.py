# Generated by Django 4.0.1 on 2022-01-22 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0022_onlineusers_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineusers',
            name='lesson',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
            preserve_default=False,
        ),
    ]
