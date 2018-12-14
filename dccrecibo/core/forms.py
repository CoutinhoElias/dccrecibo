
from django import forms
from django.contrib.auth.models import User

from django.forms import inlineformset_factory, ModelMultipleChoiceField
from django_select2.forms import Select2MultipleWidget
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
    #last_search = forms.DateField(label='Última pesquisa', widget=forms.TextInput(attrs={'class': 'datepicker'}))
    #person = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.TextInput(attrs={'class': 'hide'}))

    # person = forms.ModelChoiceField(
    #     queryset=Person.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='core:person_autocomplete')
    # )

    person = ModelMultipleChoiceField (queryset=Person.objects.all()[:5], widget=Select2MultipleWidget)

    author = forms.ModelChoiceField(
        queryset=User.objects.all()
    )


    class Meta:
        model = Receipt
        #exclude = ['author']
        fields = '__all__'

        # widgets = {
        #     'person': autocomplete.ModelSelect2(attrs={'class': 'select'}, url='core:person_autocomplete')
        # }

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