# Generated by Django 2.1 on 2018-11-28 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_receipt_observation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='cdalterdata',
        ),
    ]