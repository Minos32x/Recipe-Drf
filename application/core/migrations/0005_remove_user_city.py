# Generated by Django 3.1.7 on 2021-07-09 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
    ]