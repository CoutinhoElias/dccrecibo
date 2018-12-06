from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from django.contrib.auth.forms import UserCreationForm

from dccrecibo.accounts.forms import RegistrationForm


def register2(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
        else:
            form = UserCreationForm()

    context = {
        'form':UserCreationForm()
    }
    return render(request, template_name, context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            return redirect(settings.LOGIN_URL)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'accounts/register.html', {'form':form})
    else:
        context = {'form': RegistrationForm()}
        return render(request, 'accounts/register.html', context)