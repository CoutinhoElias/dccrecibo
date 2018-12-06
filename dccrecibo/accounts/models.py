from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(User):
    nomecompleto = models.CharField('Nome Completo', max_length=100, null=False, blank=False)
    cep = models.CharField('Cep', max_length=10, null=True, blank=False)
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.CharField('Número', max_length=10, null=False, blank=False)
    bairro = models.CharField('Bairro', max_length=50, null=False, blank=False)
    cidade = models.CharField('Cidade', max_length=50, null=False, blank=False)
    estado = models.CharField('estado', max_length=10, null=False, blank=False)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfil de Usuários'

    def __str__(self):
        return self.nomecompleto