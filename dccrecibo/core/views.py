from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template


#from dccrecibo.person.forms import PersonForm, MovimentoForm
#from dccrecibo.person.models import Person, Movimento

from django.views.generic import View

from dccrecibo.core.forms import PersonForm
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