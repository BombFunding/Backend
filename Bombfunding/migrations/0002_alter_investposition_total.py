# Generated by Django 5.1.3 on 2024-11-07 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bombfunding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investposition',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
