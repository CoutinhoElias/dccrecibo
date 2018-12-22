
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

    hidden_person = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )

    class Meta:
        model = Receipt
        fields = 'hidden_person', 'person','vehicle', 'chassis', 'color', 'author', 'observation'
        #fields = 'hidden_person', 'person','vehicle', 'chassis', 'color', 'author', 'observation'

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
