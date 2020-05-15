from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from requests import Response

from rest_framework import viewsets
from rest_framework.permissions import (BasePermission, SAFE_METHODS)
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from .form import AccountForm, AccountEditForm
from .models import Account
from .serializers import (AccountSerializer, AccountCreateSerializer,
                          AccountUpdateSerializer)


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


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user


class AccountMixin:
    queryset = Account.objects.all()
    serializers_class = {
        'default': AccountSerializer,
        'create': AccountCreateSerializer,
        'update': AccountUpdateSerializer,
        'partial_update': AccountUpdateSerializer
    }
    permission_classes = (IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.action in self.serializers_class:
            return self.serializers_class[self.action]
        return self.serializers_class['default']


class AccountViewSet(AccountMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'put']

    def create(self, request, *args, **kwargs):
        if request.user:
            raise PermissionDenied(detail='You already have an account')
        return super().create(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('list')
