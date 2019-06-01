from dal import autocomplete
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
    person = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    widget=autocomplete.ModelSelect2(url='core:person-autocomplete',
                                                                     attrs={'style': 'width: 100%;'})
                                    )
    author = forms.ModelChoiceField(queryset=User.objects.all(),
                                    widget=autocomplete.ModelSelect2(attrs={'style': 'width: 100%;'})
                                    )

    class Meta:
        model = Receipt
        exclude = ()

    layout = Layout(
        Fieldset("A impressão desta tela não tem valor de recibo.",
                 Row('person', 'vehicle'),
                 Row('chassis', 'color'),
                 Row('author'),
                 Row('observation'),
                 )
    )


ReceiptMovimentoFormSet = inlineformset_factory(Receipt, ReceiptMovimento,
                                                widgets={'form_of_payment': autocomplete.ModelSelect2(
                                                    attrs={'style': 'width: auto;'}),

                                                    'kind': autocomplete.ModelSelect2(
                                                        attrs={'style': 'width: auto;'})
                                                },
                                                can_delete=True,
                                                fields=('form_of_payment',
                                                        'kind',
                                                        'value_moved'),
                                                extra=5)


class ReceiptSearchForm(forms.Form):
    person = forms.ModelChoiceField(label='Pessoa', queryset=Person.objects.all(),
                                    required=False,
                                    widget=autocomplete.ModelSelect2(url='core:person-autocomplete',
                                                                     attrs={'style': 'width: 100%;'}))
    author = forms.ModelChoiceField(label='Usuário', queryset=User.objects.all(),
                                    required=False,
                                    widget=autocomplete.ModelSelect2(attrs={'style': 'width: 100%;'})
                                    )

    vehicle = forms.CharField(label='Veículo', required=False)
    chassis = forms.CharField(label='Chassi', required=False)
    color = forms.CharField(label='Cor', required=False)

    class Meta:
        model = Receipt
        fields = (
            'person',
            'vehicle',
            'chassis',
            'color',
            'author',
        )
        exclude = ()

    layout = Layout(
        Fieldset("Use o critério OU em suas buscas."
                 "Ou Cliente IGUAL a 'X', OU Veículo contendo caractares 'xyz', OU Chassi contendo caractares '123...',"
                 "OU Usuário IGUAL ao selecionado.",
                 Row('person', 'vehicle'),
                 Row('chassis', 'color'),
                 Row('author'),
                 )
    )
