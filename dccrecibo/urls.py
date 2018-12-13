from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from rest_framework import routers

from dccrecibo.core.api.viewsets import PersonViewSet

router = routers.DefaultRouter()
router.register(r'pessoa', PersonViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('', include('dccrecibo.core.urls')),
    path('', include(router.urls)),

    path('select2/', include('django_select2.urls')),

    path('', include('dccrecibo.accounts.urls')),
    path('admin/', admin.site.urls),
]
