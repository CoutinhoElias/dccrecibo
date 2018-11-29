from django import forms
from material import *

from dccrecibo.core.models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = (
            'name',
            'cpf_cnpj',
        )