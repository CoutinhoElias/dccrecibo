from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.i18n import JavaScriptCatalog

from dccrecibo.accounts import views

app_name = 'accounts'


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.auth_login,{'template_name': 'registration/login.html'}, name='login'),
    path('registro/', views.register, name='register'),


    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]