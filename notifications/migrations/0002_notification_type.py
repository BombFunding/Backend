# Generated by Django 5.1.5 on 2025-01-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(default='generic-notification', max_length=255),
        ),
    ]
