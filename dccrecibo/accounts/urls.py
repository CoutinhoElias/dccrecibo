from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.i18n import JavaScriptCatalog


app_name = 'accounts'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.auth_login,{'template_name': 'registration/login.html'}, name='login'),
    path('logout/', auth_views.auth_logout, {'next': 'accounts:login'}, name='logout'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]