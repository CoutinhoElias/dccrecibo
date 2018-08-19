# Generated by Django 2.1 on 2018-08-18 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180809_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='form_of_payment',
        ),
        migrations.RemoveField(
            model_name='receiptmovimento',
            name='description',
        ),
        migrations.AddField(
            model_name='receiptmovimento',
            name='form_of_payment',
            field=models.CharField(choices=[('dinheiro', 'DINHEIRO'), ('cartao_credito', 'CARTÃO DE CRÉDITO'), ('cartao_debito', 'CARTÃO DE DÉBITO'), ('cheque', 'CHEQUE')], default='dinheiro', max_length=30, verbose_name='Forma de pagamento'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receiptmovimento',
            name='kind',
            field=models.CharField(choices=[('acessorios', 'ACESSÓRIOS'), ('servico_instalacao', 'SERVIÇO DE INSTALAÇÃO'), ('acessorios_instalacao', 'ACESSÓRIOS E INSTALAÇÃO')], max_length=30, verbose_name='Tipo Movimento'),
        ),
    ]