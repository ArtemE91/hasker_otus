from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter(trailing_slash=True)

router.register('accounts', AccountViewSet, basename='accounts')