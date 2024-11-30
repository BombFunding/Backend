# Generated by Django 5.1.3 on 2024-11-30 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('total', models.IntegerField(default=0)),
                ('available', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticator.investoruser')),
            ],
        ),
        migrations.CreateModel(
            name='InvestorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticator.investoruser')),
                ('investor_position', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.investposition')),
            ],
        ),
    ]
