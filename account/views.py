
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, View
from django.shortcuts import render
from .form import AccountForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Account


class AccountLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm


class AccountCreateView(CreateView):
    template_name = 'account/signup.html'
    form_class = AccountForm


class AccountEditView(View):
    def get(self, request, username):
        user = Account.objects.get(username=username)
        bound_form = AccountForm(instance=user)
        return render(request, 'account/signup.html', context={'form': bound_form})
