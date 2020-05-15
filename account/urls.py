from django.urls import path, include, re_path
from .views import *
from .router import router

urlpatterns = [
    path('signup/', AccountCreateView.as_view(), name='signup'),
    path('login/', AccountLoginView.as_view(), name='login', ),
    path('logout/', AccountLogOut.as_view(), name='logout', ),
    path('detail/<int:id>/', AccountDetailView.as_view(), name='account_detail'),
    path('update/', AccountEditView.as_view(), name='account_update'),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include(router.urls)),
]
