# Generated by Django 3.2.25 on 2024-07-04 19:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20240703_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_num',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must contain only digits.', regex='^\\+\\d{1,14}$')]),
        ),
    ]
