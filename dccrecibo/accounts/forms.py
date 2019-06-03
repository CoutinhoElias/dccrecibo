from django import forms
from django.contrib.auth.forms import UserCreationForm
from dccrecibo.accounts.models import UserAdress
from material import *


class RegistrationForm(forms.Form, UserCreationForm):
    class Meta:
        model = UserAdress
        fields = (
            'username',
            'nomecompleto',
            'company',
            'cep',
            'logradouro',
            'numero',
            'bairro',
            'cidade',
            'estado',
        )

    layout = Layout(
        Fieldset('Faça seu cadastro agora.', 'username',
                 Row('password1', 'password2')),
        Fieldset('Dados Pessoais',
                 Row(Span12('nomecompleto')),
                 Row(Span12('company')),
                 Row(Span2('cep'), Span8('logradouro'), Span2('numero')),
                 Row(Span5('bairro'), Span5('cidade'), Span2('estado'))))

