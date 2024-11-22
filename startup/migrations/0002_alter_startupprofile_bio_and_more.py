# Generated by Django 5.1.3 on 2024-11-22 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_remove_baseuser_about_me_remove_baseuser_name_and_more'),
        ('startup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startupprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='categories',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='page',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='startup_user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='authenticator.startupuser'),
        ),
    ]
