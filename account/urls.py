from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.AccountCreateView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name='account/login.html'), name="login", ),
    path("update/<str:username>/", views.AccountEditView.as_view(), name='update'),
]