from rest_framework.routers import DefaultRouter
from .views import QuestionsViewSet, AnswerViewSet

router = DefaultRouter(trailing_slash=True)

router.register('questions', QuestionsViewSet)
router.register('answer', AnswerViewSet)
