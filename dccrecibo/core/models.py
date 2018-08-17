from django.db import models

# Create your models here.
from django.db.models import Sum
from django.urls import reverse


class Person(models.Model):
    cdalterdata = models.CharField('Cód. Alterdata', max_length=6)
    name = models.CharField('Nome',max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Pessoas'
        verbose_name = 'Pessoa'

class Receipt(models.Model):
    person = models.ForeignKey('core.Person', related_name='person_item',on_delete=models.CASCADE, verbose_name='Cliente')
    vehicle = models.CharField('Veículo',max_length=100)
    chassis = models.CharField('Chassi', max_length=100)
    color = models.CharField('Cor', max_length=100)
    form_of_payment = models.CharField('Forma de pagamento', max_length=100)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    @property
    def value_total(self):
        return ReceiptMovimento.objects.all().aggregate(Sum('value_moved'))['value_moved__sum']

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse('core:admin_receipt_pdf', args=[str(self.id)])


TRANSACTION_KIND = (
    ("servico", "SERVIÇO"),
    ("produto", "PRODUTO")
)


class ReceiptMovimento(models.Model):
    receipt = models.ForeignKey('core.Receipt', related_name='recibo_item', on_delete=models.CASCADE, verbose_name='Recibo')
    kind = models.CharField('Tipo Movimento', max_length=10, choices=TRANSACTION_KIND)
    description = models.CharField('Nome',max_length=100)
    value_moved = models.DecimalField('Valor Movimento', max_digits=10, decimal_places=2)


    class Meta:
        verbose_name_plural = 'Movimentos'
        verbose_name = 'Movimento'