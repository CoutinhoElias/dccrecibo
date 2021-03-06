from django.conf.urls import url, include
from django.urls import path

from django.views.i18n import JavaScriptCatalog

from dccrecibo.core import views
from .views import GeneratePDF
app_name = 'core'


urlpatterns = [
    path('<int:id>/',  GeneratePDF.as_view(), name='generatepdf'),
    path('<int:id>/pdf/', views.admin_receipt_pdf, name='admin_receipt_pdf'),

    path('recibo/novo/', views.receipt_create, name='receipt_create'),
    path('pedido/editar/<int:id>/', views.receipt_update, name='receipt_update'),

    path('lista/', views.receipt_return, name='receipt_return'),
    path('lista/recibo/', views.receipt_return, name='receipt_return'),
    path('lista/recibo2/', views.receipt_return2, name='receipt_return2'),

    path('pessoa/novo/', views.person_create, name='person_create'),

    path('person-autocomplete/', views.PersonAutocomplete.as_view(), name='person-autocomplete'),

    path('pessoa/popular/', views.populate, name='populate'),
    path('pessoa/listar/', views.person_list, name='person_list'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]