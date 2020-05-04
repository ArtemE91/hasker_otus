from rest_framework.routers import DefaultRouter
from .views import TagViewSet, QuestionsViewSet, AnswerViewSet

router = DefaultRouter(trailing_slash=True)

router.register('tag', TagViewSet)
router.register('questions', QuestionsViewSet)
router.register('answer', AnswerViewSet)
