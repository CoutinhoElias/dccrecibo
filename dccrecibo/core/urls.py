from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from dccrecibo.core import views
from .views import GeneratePDF, person_autocomplete

app_name = 'core'


urlpatterns = [
    path('<int:id>/',  GeneratePDF.as_view(), name='generatepdf'),
    path('<int:id>/pdf/', views.admin_receipt_pdf, name='admin_receipt_pdf'),

    path('recibo/novo/', views.receipt_create, name='receipt_create'),
    path('edido/editar/<int:id>/', views.receipt_update, name='receipt_update'),

    path('lista/', views.receipt_return, name='receipt_return'),

    path('pessoa/novo/', views.person_create, name='person_create'),
    path('person-autocomplete', person_autocomplete, name='person_autocomplete'),
    path('pessoa/popular/', views.populate, name='populate'),
    path('pessoa/listar/', views.person_list, name='person_list'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]