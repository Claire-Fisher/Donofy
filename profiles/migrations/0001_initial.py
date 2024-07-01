# Generated by Django 3.2.25 on 2024-06-27 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_user', models.BooleanField(default=True)),
                ('first_name', models.CharField(blank=True, max_length=25)),
                ('last_name', models.CharField(blank=True, max_length=25)),
                ('phone_num', models.CharField(blank=True, max_length=20)),
                ('street_address_1', models.CharField(blank=True, max_length=80)),
                ('street_address_2', models.CharField(blank=True, max_length=80)),
                ('town_or_city', models.CharField(blank=True, max_length=40)),
                ('county', models.CharField(blank=True, max_length=80)),
                ('post_code_zip', models.CharField(blank=True, max_length=20)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('charity_favs', models.JSONField(blank=True, default=list)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]