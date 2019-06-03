from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from django.template.loader import get_template


from django.views.generic import View

from dccrecibo.accounts.models import UserAdress
from dccrecibo.core.forms import PersonForm, ReceiptForm, ReceiptMovimentoFormSet, ReceiptSearchForm
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
    weasyprint.HTML(string=html,
                    base_url=request.build_absolute_uri()).write_pdf(response,
                                                                     stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +
                                                                                                 '/css/pdf.css')])
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


# def receipt_return1(request):
#     q = request.GET.get('searchInput')
#
#     if q:
#         receipts = Receipt.objects.select_related('person')\
#             .all().order_by('created').filter(person__name__icontains=q)
#     else:
#         receipts = Receipt.objects.select_related('person')\
#             .all().order_by('created')
#     context = {'receipts': receipts}
#     return render(request, 'lista_recibo.html', context)


def receipt_return(request):


    if request.method == 'POST':

        form = ReceiptSearchForm(request.POST)

        if form.is_valid():
            # vehicle1=form.cleaned_data['vehicle'],

            # criar_filter(vehicle)
            # print(criar_filter(vehicle), 'POST')
            # (vehicle) = criar_filter()

            # pvehicle = form.cleaned_data['vehicle']
            receipts = Receipt.objects.select_related('person').all().order_by('created')

            # return HttpResponseRedirect('/lista/recibo/')
        else:
            return render(request, 'person_create.html', {'form': form})
        return HttpResponseRedirect('/lista/recibo')
    else:
        person = request.GET.get('person') or 0
        vehicle = request.GET.get('vehicle') or '#@!%$#'
        chassis = request.GET.get('chassis') or '#@!%$#'
        color = request.GET.get('color') or '#@!%$#'
        author = request.GET.get('author') or 0


        receipts = Receipt.objects.select_related('person').filter(Q(vehicle__icontains=vehicle) |
                                                                   Q(person=person) |
                                                                   Q(chassis__icontains=chassis) |
                                                                   Q(color__icontains=color) |
                                                                   Q(author=author)
                                                                   ).order_by('created')
        context = {'form': ReceiptSearchForm(), 'receipts': receipts}

        return render(request, 'lista_recibo.html', context)


def criar_filtro(regras_filtro):
    filtro = {}

    if 'vehicle' in regras_filtro:
        filtro['vehicle__icontains'] = regras_filtro['vehicle']

    if 'person' in regras_filtro:
        filtro['person__name__icontains'] = regras_filtro['person']
    # E por ai vai
    return filtro


# ----------------------------------------------------------------------------------------------------------
def receipt_return2(request):
    form = ReceiptSearchForm(request.GET or None)
    if form.is_valid():  # Existe filtro
        filtro = criar_filtro(form.cleaned_data)
        print(**filtro)
        receipts = Receipt.objects.select_related('person').filter(**filtro).order_by('created')
    else:  # Lista todo mundo
        receipts = Receipt.objects.select_related('person').all().order_by('created')
    context = {'form': form, 'receipts': receipts}
    return render(request, 'lista_recibo.html', context)


def search_receipt(request):
    receipt_list = Receipt.objects.all()
    receipt_filter = ReceiptFilter(request.GET, queryset=receipt_list)
    return render(request, 'lista_recibo.html', {'filter': receipt_filter})
# ----------------------------------------------------------------------------------------------------------


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            # form.save_m2m()

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


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def receipt_create(request):
    success_message = 'The receipt was edited correctly.'
    if request.method == 'POST':
        movements = get_object_or_404(UserAdress, user_ptr_id=request.user)

        form = ReceiptForm(request.POST)
        formset = ReceiptMovimentoFormSet(request.POST)

        # form.errors.pop('person')
        # form.errors.pop('hidden_person')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                new = form.save(commit=False)
                new.company_id = movements.company_id
                new.save()
                formset.instance = new
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
    # joga na variável invoice na linha abaixo passando o modelo MESTRE e os parâmetros que desejo como filtro
    receipt = get_object_or_404(Receipt, pk=pk)
    # print(request.method)
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
        # Caso não seja POST ele trará o formulário com as informações preenchidas do parâmetro invoice
        # que pegamos da URL quando passamoso request de pk na entrada da função acima.
        form = ReceiptForm(instance=receipt)
        formset = ReceiptMovimentoFormSet(instance=receipt)

    # Passamos os dois forms para uma variável com um nome qualquer
    # (Neste caso usamos o nome "forms" afim de dar a idéia
    # demais de um formulário conforme abaixo:
    # Na linha context passamos também os dois contextos e
    # por fim na linha final passamos o retorno da função onde chamamos o template com o context.
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'checkout/invoice_form.html', context)

# ----------------------------------------------------------------------------------------------------------------------


def register(request):
    template_name: 'accounts/register.html'
    # context = {
    #     'form': UserCreationForm()
    # }
    return render(request, template_name)


def populate(request):

    from dccrecibo.core import create_data

    print(create_data.person_add)

    lista = []

    for person in create_data.person_add:
        obj = Person(**person)
        lista.append(obj)

    Person.objects.bulk_create(lista)

    return person_list
