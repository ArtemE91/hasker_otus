# Generated by Django 3.0.5 on 2020-05-02 09:54

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to=account.models.user_directory_path),
        ),
    ]