# Generated by Django 4.1.7 on 2023-03-22 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchat',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
    ]
