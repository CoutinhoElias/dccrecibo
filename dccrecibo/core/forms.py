from django import forms
from django.forms import inlineformset_factory
from material import *

from dccrecibo.core.models import Person, Receipt, ReceiptMovimento


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = (
            'name',
            'cpf_cnpj',
        )


class ReceiptForm(forms.models.ModelForm):

    class Meta:
        model = Receipt
        #exclude = ['author']
        fields = '__all__'

    layout = Layout(
        Fieldset("A impressão desta tela não tem valor de recibo.",
                     Row('person','vehicle'),
                     Row('chassis', 'color'),
                     Row('author'),
                     Row('observation'),
                    )
        )

ReceiptMovimentoFormSet = inlineformset_factory(Receipt, ReceiptMovimento, can_delete=True,
        fields=('form_of_payment', 'kind', 'value_moved'), extra=5)