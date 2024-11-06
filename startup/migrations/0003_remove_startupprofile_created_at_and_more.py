# Generated by Django 5.1.3 on 2024-11-06 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_alter_baseuser_email_alter_investoruser_categories_and_more'),
        ('startup', '0002_remove_startupprofile_categories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='startupprofile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='required_budget',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='start_date',
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='categories',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='page',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='startupprofile',
            name='startup_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authenticator.startupuser'),
        ),
    ]
