from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template.loader import get_template


#from dccrecibo.person.forms import PersonForm, MovimentoForm
#from dccrecibo.person.models import Person, Movimento

from django.views.generic import View

from dccrecibo.core.forms import PersonForm, ReceiptForm, ReceiptMovimentoFormSet
from dccrecibo.core.models import Receipt, ReceiptMovimento, Person
from dccrecibo.utils import render_to_pdf# created in step 4

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import weasyprint

def home(request):
    return render(request, 'index.html')

def admin_receipt_pdf(request, id=id):
    recibo = Receipt.objects.get(id=id)
    movements = ReceiptMovimento.objects.filter(receipt_id=id)

    context = {
        'recibo': recibo,
        'movements': movements
    }

    html = render_to_string('recibo.html', context)
    response = HttpResponse(content_type='recibo/pdf')
    response['Content-Disposition'] = 'filename="recibo_{}.pdf"'.format(recibo.id)       #CONSULTAR UNIVERSITÁRIOS
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
    #print(request.GET)
    if q:
        receipts = Receipt.objects.select_related('person').all().order_by('created').filter(person__name__icontains=q)
    else:
        receipts = Receipt.objects.select_related('person').all().order_by('created')
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
    persons = Person.objects.all().order_by("name")
    return render(request, 'person_list.html', {'persons': persons})


#----------------------------------------------------------------------------------------------------------------------

def receipt_create(request):
    success_message = 'The receipt was edited correctly.'
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        formset = ReceiptMovimentoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                receipt = form.save()
                formset.instance = receipt
                formset.save()

            if 'btn_submit_1' in request.POST:
                return redirect('/lista/')
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

