# Generated by Django 5.1.3 on 2024-11-21 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0002_startupprofile_email_startupprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startupposition',
            old_name='description',
            new_name='bio',
        ),
        migrations.RenameField(
            model_name='startupprofile',
            old_name='description',
            new_name='bio',
        ),
    ]
