# Generated by Django 2.1 on 2018-08-24 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180818_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cpf_cnpj',
            field=models.CharField(default='11.111.111/0001-11', max_length=18, verbose_name='CPF/CNPJ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receiptmovimento',
            name='kind',
            field=models.CharField(choices=[('ACESSÓRIOS', 'ACESSÓRIOS'), ('SERVIÇO DE INSTALACÃO', 'SERVIÇO DE INSTALACÃO'), ('ACESSÓRIOS E INSTALACÃO', 'ACESSÓRIOS E INSTALACÃO')], max_length=30, verbose_name='Tipo Movimento'),
        ),
    ]
