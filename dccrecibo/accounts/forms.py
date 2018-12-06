from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from material import *


class RegistrationForm(forms.Form, UserCreationForm):
    username = forms.CharField(max_length=30,required=True,label='Login')

    nomecompleto = forms.CharField(required=True,label='Nome Completo')
    cep  = forms.IntegerField(max_value=99999999,required=True,label='CEP')
    #tipo_logradouro = forms.CharField(required=True,label='Tipo')
    logradouro = forms.CharField(required=True,label='Logradouro')
    numero = forms.CharField(required=True,label='Número')
    bairro = forms.CharField(required=True,label='Bairro')
    cidade = forms.CharField(required=True,label='Cidade')
    estado = forms.CharField(required=True,label='UF')

    layout = Layout(
         Fieldset('Faça seu cadastro agora.', 'username',
            Row('password1', 'password2')),
         Fieldset('Dados Pessoais','nomecompleto',
            Row(Span2('cep'),Span8('logradouro'),Span2('numero')),
            Row(Span5('bairro'),Span5('cidade'),Span2('estado'))))