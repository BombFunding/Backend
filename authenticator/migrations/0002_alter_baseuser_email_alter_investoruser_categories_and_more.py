# Generated by Django 5.1.3 on 2024-11-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='investoruser',
            name='categories',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investoruser',
            name='page',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
