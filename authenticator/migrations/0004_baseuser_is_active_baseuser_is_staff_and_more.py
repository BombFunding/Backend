# Generated by Django 5.1.3 on 2024-11-13 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0003_remove_baseuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]