# Generated by Django 3.2.25 on 2024-07-10 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_userprofile_charity_favs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_num',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must start with a "+" followed by 1 to 14 digits.', regex='^\\+\\d{1,14}$')]),
        ),
    ]
