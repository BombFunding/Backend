# Generated by Django 5.1.3 on 2024-11-30 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Bombfunding', '0001_initial'),
        ('authenticator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartupApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_position', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.investposition')),
                ('startup_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticator.baseprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StartupProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startup_rank', models.PositiveSmallIntegerField(default=1)),
                ('startup_categories', models.CharField(choices=[('Technology', 'Technology'), ('Food', 'Food'), ('Beauty', 'Beauty'), ('Art', 'Art'), ('Health', 'Health'), ('Tourism', 'Tourism'), ('Education', 'Education'), ('Finance', 'Finance')], default='Art', max_length=50)),
                ('startup_starting_date', models.DateField(blank=True, null=True)),
                ('startup_profile_visit_count', models.PositiveIntegerField(default=0)),
                ('startup_user', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='authenticator.startupuser')),
            ],
        ),
        migrations.CreateModel(
            name='StartupPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bio', models.TextField()),
                ('total', models.IntegerField()),
                ('funded', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('startup_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup.startupprofile')),
            ],
        ),
    ]
