# Generated by Django 2.1 on 2019-01-11 21:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20181128_2123'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UserAdress',
        ),
    ]
