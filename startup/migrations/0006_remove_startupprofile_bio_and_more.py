# Generated by Django 5.1.3 on 2024-11-21 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0005_rename_description_startupposition_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='startupprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='startupprofile',
            name='socials',
        ),
    ]
