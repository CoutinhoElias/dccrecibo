from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('', include('dccrecibo.core.urls')),

    path('', include('dccrecibo.accounts.urls')),
    path('admin/', admin.site.urls),
]
