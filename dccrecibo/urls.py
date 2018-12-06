from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('', include('dccrecibo.core.urls')),

    path('', include('dccrecibo.accounts.urls')),
    #path('conta/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
