# Generated by Django 3.2.25 on 2024-07-01 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_userprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='default_user', max_length=25),
        ),
    ]
