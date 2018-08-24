import socket

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.urls import reverse


from num2words import num2words


class Person(models.Model):
    cdalterdata = models.CharField('Cód. Alterdata', max_length=6)
    name = models.CharField('Nome',max_length=100)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Pessoas'
        verbose_name = 'Pessoa'

class Receipt(models.Model):
    person = models.ForeignKey('core.Person', related_name='person_item', on_delete=models.CASCADE, verbose_name='Cliente')
    vehicle = models.CharField('Veículo',max_length=100)
    chassis = models.CharField('Chassi', max_length=100)
    color = models.CharField('Cor', max_length=100)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,)

    @property
    def value_total(self):
        return ReceiptMovimento.objects.filter(receipt_id=self.id).aggregate(Sum('value_moved'))['value_moved__sum']

    @property
    def number_in_full(self):
        return num2words(self.value_total,to='currency',lang='pt_BR')

    @property
    def host_name(self):
        return socket.gethostbyaddr(socket.gethostname())

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse('core:admin_receipt_pdf', args=[str(self.id)])

TRANSACTION_PAYMENT = (
    ("DINHEIRO", "DINHEIRO"),
    ("CARTÃO DE CRÉDITO", "CARTÃO DE CRÉDITO"),
    ("CARTÃO DE DÉBITO", "CARTÃO DE DÉBITO"),
    ("CHEQUE", "CHEQUE")
)

TRANSACTION_KIND = (
    ("ACESSÓRIOS", "ACESSÓRIOS"),
    ("SERVIÇO DE INSTALACÃO", "SERVIÇO DE INSTALACÃO"),
    ("ACESSÓRIOS E INSTALACÃO", "ACESSÓRIOS E INSTALACÃO")
)


class ReceiptMovimento(models.Model):
    receipt = models.ForeignKey('core.Receipt', related_name='recibo_item', on_delete=models.CASCADE, verbose_name='Recibo')
    kind = models.CharField('Tipo Movimento', max_length=30, choices=TRANSACTION_KIND)
    #description = models.CharField('Nome',max_length=100)
    form_of_payment = models.CharField('Forma de pagamento', max_length=30, choices=TRANSACTION_PAYMENT)
    value_moved = models.DecimalField('Valor Movimento', max_digits=10, decimal_places=2)


    class Meta:
        verbose_name_plural = 'Movimentos'
        verbose_name = 'Movimento'