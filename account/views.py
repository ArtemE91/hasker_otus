from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from .form import AccountForm, AccountEditForm
from .models import Account


class AccountLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm


class AccountLogOut(LogoutView):
    next = reverse_lazy('question:question_list')


class AccountCreateView(CreateView):
    template_name = 'account/signup.html'
    form_class = AccountForm
    success_url = reverse_lazy('login')


class AccountEditView(UpdateView):
    form_class = AccountEditForm
    template_name = "account/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class AccountDetailView(DetailView):
    model = Account
    template_name = "account/detail_profile.html"
    pk_url_kwarg = "id"