# Generated by Django 5.1.2 on 2024-10-28 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=50)),
                ('about_me', models.TextField()),
                ('user_type', models.CharField(choices=[('Investor', 'Investor'), ('Startup', 'Startup'), ('Basic', 'Basic')], default='Basic', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='InvestPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('total', models.IntegerField()),
                ('available', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StartupProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('page', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='BasicUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bombfunding.baseuser')),
            ],
        ),
        migrations.CreateModel(
            name='InvestorUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bombfunding.baseuser')),
                ('page', models.JSONField()),
                ('categories', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='StartupUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bombfunding.baseuser')),
            ],
        ),
        migrations.CreateModel(
            name='StartupPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('total', models.IntegerField()),
                ('funded', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('startup_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.startupprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StartupComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('time', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.baseuser')),
                ('startup_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.startupprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StartupApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.investposition')),
                ('startup_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.startupprofile')),
            ],
        ),
        migrations.AddField(
            model_name='investposition',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.investoruser'),
        ),
        migrations.CreateModel(
            name='InvestorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startup_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.startupposition')),
                ('investor_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.investoruser')),
            ],
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='startup_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Bombfunding.startupuser'),
        ),
    ]
