from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from .views import GeneratePDF, admin_receipt_pdf, receipt_return

app_name = 'core'


urlpatterns = [
    url(r'(?P<id>\d+)/$', GeneratePDF.as_view(), name='generatepdf'),
    url(r'(?P<id>\d+)/pdf/$', admin_receipt_pdf, name='admin_receipt_pdf'),
    url(r'lista/$', receipt_return, name='receipt_return'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]