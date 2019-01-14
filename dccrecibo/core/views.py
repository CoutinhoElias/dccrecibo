from dal import autocomplete
from dal_select2.views import Select2QuerySetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from django.template.loader import get_template


from django.views.generic import View


import create_data
from dccrecibo.core.forms import PersonForm, ReceiptForm, ReceiptMovimentoFormSet
from dccrecibo.core.models import Receipt, ReceiptMovimento, Person
from dccrecibo.utils import render_to_pdf

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import weasyprint


def home(request):
    return render(request, 'index.html')


def admin_receipt_pdf(request, id=id):
    recibo = Receipt.objects.select_related('author__useradress', 'person').get(id=id)
    movements = ReceiptMovimento.objects.select_related('receipt').filter(receipt_id=id)

    context = {
        'recibo': recibo,
        'movements': movements
    }

    html = render_to_string('recibo.html', context)
    response = HttpResponse(content_type='recibo/pdf')
    response['Content-Disposition'] = 'filename="recibo_{}.pdf"'.format(recibo.id)
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response


class GeneratePDF(View):
    def get(self, request, id, *args, **kwargs):
        template = get_template('recibo.html')

        recibo = Receipt.objects.get(id=id)
        movements = ReceiptMovimento.objects.filter(receipt_id=id)

        context = {
            'recibo': recibo,
            'movements': movements
        }

        html = template.render(context)
        pdf = render_to_pdf('recibo.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def receipt_return(request):
    q = request.GET.get('searchInput')

    if q:
        receipts = Receipt.objects.select_related('person')\
            .all().order_by('created').filter(person__name__icontains=q)
    else:
        receipts = Receipt.objects.select_related('person')\
            .all().order_by('created')
    context = {'receipts': receipts}
    return render(request, 'lista_recibo.html', context)

#DEFINIR NOVO RECIBO COMO


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            #form.save_m2m()

            return HttpResponseRedirect('/pessoa/listar')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': PersonForm()}
        return render(request, 'person_create.html', context)


def person_list(request):
    q = request.GET.get('searchInput')
    if q:
        persons = Person.objects.all().order_by('name').filter(name__icontains=q)
    else:
        persons = Person.objects.all().order_by('name')
    context = {'persons': persons}
    return render(request, 'person_list.html', context)


def person_autocomplete(request):

    person_list = []
    parm = request.GET.get('term')
    persons = Person.objects.filter(
        Q(name__icontains=parm) |
        Q(cpf_cnpj__iexact=parm)
    )[:10]

    for person in persons:
        data = {}
        data['id'] = person.pk
        data['label'] = person.name
        data['value'] = person.name
        print(person_list.append(data))
        person_list.append(data)

    return JsonResponse(person_list, safe=False)


class PersonAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


#----------------------------------------------------------------------------------------------------------------------
@login_required
def receipt_create(request):
    success_message = 'The receipt was edited correctly.'
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        formset = ReceiptMovimentoFormSet(request.POST)

        #form.errors.pop('person')
        #form.errors.pop('hidden_person')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():

                receipt = form.save()
                formset.instance = receipt
                formset.save()

            if 'btn_submit_1' in request.POST:
                return redirect('/logout/')
            else:
                return redirect('/recibo/novo/')
    else:
        form = ReceiptForm(initial={'author': request.user})
        formset = ReceiptMovimentoFormSet()

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'receipt_form.html', context)


def receipt_update(request, pk):
    # Pega a chave da URL acima com (request, pk)
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e osparâmetros que desejo como filtro
    receipt = get_object_or_404(Receipt, pk=pk)
    #print(request.method)
    if request.method == 'POST':
        # Os formulários InvoiceForm receberá o request.POST com os campos em branco
        form = ReceiptForm(request.POST, instance=receipt)
        formset = ReceiptMovimentoFormSet(request.POST, instance=receipt)

        # Valida os formulários MESTRE(InvoiceForm) e DETALHE(ItemFormSet)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            return redirect('/lista/')
    else:
        #Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro invoice
        #que pegamos da URL quandopassamoso request de pk na entrada da função acima.
        form = ReceiptForm(instance=receipt)
        formset = ReceiptMovimentoFormSet(instance=receipt)
    #Passamos os dois forms para uma variável com um nome qualquer (Neste cado usamos o nome "forms" afim de dar a idéia
    # demais de um formulário conforme abaixo:
    #Na linha context passamos também os dois contextos e
    #por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'checkout/invoice_form.html', context)

#----------------------------------------------------------------------------------------------------------------------


def register(request):
    template_name: 'accounts/register.html'
    context = {
        'form': UserCreationForm()
    }
    return render(request, template_name)


def populate(request):

    person_add = create_data

    lista = []

    for person in person_add:
        obj = Person(**person)
        lista.append(obj)

    Person.objects.bulk_create(lista)

    return person_list
