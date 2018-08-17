from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from .views import GeneratePDF, admin_receipt_pdf, receipt_return

app_name = 'core'


urlpatterns = [
    # url(r'novo/$', person_create, name='person_create'),
    # url(r'consultar/(?P<id>\d+)/$', person_view, name='person_view'),
    #url(r'recibo/$', generatePdf, name='generatepdf'),
    url(r'(?P<id>\d+)/$', GeneratePDF.as_view(), name='generatepdf'),
    url(r'(?P<id>\d+)/pdf/$', admin_receipt_pdf, name='admin_receipt_pdf'),
    url(r'lista/$', receipt_return, name='receipt_return'),
    # url(r'giro/$', person_turn, name='person_turn'),
    # url(r'retorno/$', person_return, name='person_return'),
    # url(r'movimento/$', movement_create, name='movement_create'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]