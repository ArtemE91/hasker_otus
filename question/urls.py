from django.urls import path

from .views import *

urlpatterns = [
    path('', QuestionList.as_view(), name='question_list'),
    path('question/<int:id>/', QuestionDetail.as_view(), name='question_detail'),
    path('question/create/', QuestionAddView.as_view(), name='question_create'),
    path('tag/<str:name>/', TagDetail.as_view(), name='tag_detail')
]