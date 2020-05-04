from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, re_path
from .views import *
from .router import router

urlpatterns = [
    path('signup/', AccountCreateView.as_view(), name='signup'),
    path('login/', AccountLoginView.as_view(), name='login', ),
    path('logout/', AccountLogOut.as_view(), name='logout', ),
    path('detail/<int:id>/', AccountDetailView.as_view(), name='account_detail'),
    path('update/', AccountEditView.as_view(), name='account_update'),
    path('api/', include(router.urls)),
    path('api/login/', login),
]
