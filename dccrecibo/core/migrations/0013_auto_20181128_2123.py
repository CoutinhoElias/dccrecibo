# Generated by Django 2.1 on 2018-11-29 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_person_cdalterdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='cpf_cnpj',
            field=models.CharField(max_length=18, unique=True, verbose_name='CPF/CNPJ'),
        ),
    ]
