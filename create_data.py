import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dccrecibo.settings")
django.setup()

#from django.utils.text import slugfy
from dccrecibo.core.models import Person


def populate(request):

    PERSONS_ADD = [
        {'cpf_cnpj':'00.000.000/3875-09','name':'BANCO DO BRASIL S.A'},
            {'cpf_cnpj':'00.000.320/6413-68','name':'JOSE CELIO GURGEL DE CASTRO'},
            {'cpf_cnpj':'00.000.885/0001-29','name':'BRASAL BRASÍLIA SERVIÇOS AUTOMOTORES S/A'},
            {'cpf_cnpj':'00.004.309/0001-50','name':'DF VEICULOS LTDA'},
            {'cpf_cnpj':'00.025.131/0001-23','name':'RDA Com e Rep. e Imp. de Mat. Elet. S/A'},
            {'cpf_cnpj':'00.025.131/0002-04','name':'RDA COM. REPRES. E IMPORT DE MATER. ELETR. LTDA'},
            {'cpf_cnpj':'00.025.131/0004-76','name':'RDA COMÉRCIO REP. IMP. de MAT. ELETRÔNICOS S/A'},
            {'cpf_cnpj':'00.048.785/0018-10','name':'INDAIA BRASIL AGUAS MINERAIS LTDA'},
            {'cpf_cnpj':'00.057.733/0001-62','name':'MB GUIMARAES NETO CIA LTDA'},
            {'cpf_cnpj':'00.058.387/0001-37','name':'TRANSPORTADORA ARRUDA LTDA EPP'},
            {'cpf_cnpj':'00.063.405/0001-79','name':'Dafonte Veiculos LTDA'},
            {'cpf_cnpj':'00.063.557/0001-71','name':'IVASCONCELOS COM E REPRESENTACOES LTDA'},
            {'cpf_cnpj':'00.066.871/0001-08','name':'HAIKAR VEICULOS LTDA'},
            {'cpf_cnpj':'00.070.112/0005-42','name':'ALL NATIONS COMERCIO EXTERIOR S/A'},
            {'cpf_cnpj':'00.075.306/0001-07','name':'TAPAJÓS DISTRIBUIDORA DE VEÍCULOS LTDA'},
            {'cpf_cnpj':'00.095.051/0001-44','name':'BIOCILIN IND. DE COSMETICOS LTDA'},
            {'cpf_cnpj':'00.101.378/0001-81','name':'TAGUAUTO - TAGUATINGA AUTOMÓVEIS E SERVIÇOS LTDA'},
            {'cpf_cnpj':'00.113.024/0001-57','name':'BRANDAO IND. COM. DE MATERIAL CONSTRUCAO LTDA'},
            {'cpf_cnpj':'00.118.331/0004-73','name':'IGREJA PRESBITERIANA DO BRASIL'},
            {'cpf_cnpj':'00.126.621/0001-16','name':'TRANSSEERV TRANSPORTE DE SERV. LTDA'},
            {'cpf_cnpj':'00.127.655/0001-25','name':'CORSA VEICULOS LTDA'},
            {'cpf_cnpj':'00.130.073/0001-06','name':'ESPART MOVEIS LTDA'},
            {'cpf_cnpj':'999.974.953-49','name':'GRAZIELA COSTA ARAUJO'}
    ]

    lista = []

    for person in PERSONS_ADD:
        obj = Person(**person)
        lista.append(obj)

    Person.objects.bulk_create(lista)