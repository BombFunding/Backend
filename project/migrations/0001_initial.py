# Generated by Django 5.1.4 on 2025-01-02 13:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.JSONField(default=dict)),
                ('name', models.CharField(default='Startup Project', max_length=50)),
                ('image', models.ImageField(default='projects/default_project.jpg', upload_to='projects/')),
                ('description', models.TextField(blank=True, max_length=500)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('subcategories', models.JSONField(blank=True, default=list)),
                ('user', models.ForeignKey(limit_choices_to={'user_type__in': ['startup']}, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projectimages/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
