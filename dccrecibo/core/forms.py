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


class ReceiptSearchForm(forms.ModelForm):
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
        Fieldset("Efetue sua pesquisa.",
                     Row('person', 'vehicle'),
                     Row('chassis', 'color'),
                     Row('author'),
                 )
        )