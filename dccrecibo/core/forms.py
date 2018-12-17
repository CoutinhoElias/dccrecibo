
from django import forms
from django.contrib.auth.models import User

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
    # person = forms.ModelChoiceField(
    #     queryset=Person.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='core:person_autocomplete')
    # )

    # person = ModelMultipleChoiceField(queryset=Person.objects.all()[:15], widget=HeavySelect2Widget(
    #     data_url='http://127.0.0.1:8000/pessoa/'
    # ))

    # person = ModelMultipleChoiceField(queryset=Person.objects.all()[:15], widget=Select2Widget)

    author = forms.ModelChoiceField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Receipt
        fields = '__all__'

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
