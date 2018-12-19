
from django import forms
from django.db.models import TextField

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


class ReceiptForm(forms.ModelForm):

    person = forms.ModelChoiceField(
        queryset=Person.objects.none(),
        widget=forms.TextInput(attrs={'class': 'form-control autocomplete'})
    )

    class Meta:
        model = Receipt
        fields = '__all__'

        # widgets = {
        #     'person': forms.TextInput
        # }

    layout = Layout(
        Fieldset("A impressão desta tela não tem valor de recibo.",
                     Row('person', 'vehicle'),
                     Row('chassis', 'color'),
                     Row('author'),
                     Row('observation'),
                    )
        )


ReceiptMovimentoFormSet = inlineformset_factory(Receipt, ReceiptMovimento,
                                                can_delete=True, fields=('form_of_payment', 'kind', 'value_moved'),
                                                extra=5)
