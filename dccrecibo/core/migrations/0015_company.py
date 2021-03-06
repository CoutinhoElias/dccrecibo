# Generated by Django 2.1 on 2019-06-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190518_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome Empresa (Fantasia)')),
                ('cpf_cnpj', models.CharField(max_length=18, unique=True, verbose_name='CPF/CNPJ')),
                ('uf', models.CharField(max_length=18, unique=True, verbose_name='UF')),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
            },
        ),
    ]
