# Generated by Django 5.1.3 on 2024-11-30 11:46

import authenticator.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
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
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(default=' ', max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('investor', 'Investor'), ('startup', 'Startup'), ('basic', 'Basic')], default='basic', max_length=10)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(code='invalid_password', message='Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.', regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&#])[A-Za-z\\d@$!%*?&#]{8,}$')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BasicUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestorUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('page', models.JSONField(blank=True, null=True)),
                ('categories', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StartupUser',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=50, null=True)),
                ('email', models.EmailField(editable=False, max_length=100, null=True)),
                ('socials', models.JSONField(default=dict, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pics/default_profile.jpg', null=True, upload_to=authenticator.models.user_profile_picture_path)),
                ('header_picture', models.ImageField(blank=True, default='header_pics/default_header.jpg', null=True, upload_to=authenticator.models.user_header_picture_path)),
                ('base_user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BaseuserComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('time', models.DateTimeField()),
                ('baseuser_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticator.baseprofile')),
                ('username', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
