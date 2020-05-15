from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, View
from django.db.models import Q, Count, F
from django.core.paginator import Paginator

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Questions, Tag, Answer
from .form import QuestionForm, AnswerForm
from .serializers import (QuestionsListSerializer, AnswerSerializer,
                          QuestionDetailSerializer, AnswerCreteSerializer)


class QuestionMixin:
    paginate_by = 2

    class Meta:
        abstract: True

    def get_related_activities(self, queryset):
        queryset = self.sort_by_like(queryset)
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities

    def get_context_populate_q(self):
        populate_q = Questions.objects.all()
        return self.sort_by_like(populate_q)

    @staticmethod
    def sort_by_like(queryset):
        return queryset.annotate(likes=Count("like"), dislikes=Count("dislike")
                                 , ).order_by(F("dislikes") - F("likes"), '-date_create')


class QuestionList(ListView, QuestionMixin):
    model = Questions
    template_name = 'question/question_list.html'
    paginate_by = 30
    sort_by_date = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['populate_q'] = self.get_context_populate_q()
        return context

    def get_queryset(self):
        queryset = Questions.objects.all()
        question = self.request.GET.get("q")
        if question and 'tag:' in question:
            name_tag = question.split('tag:')[-1]
            tag = get_object_or_404(Tag, name=name_tag)
            queryset = tag.questions.all()
        elif question:
            queryset = queryset.filter(Q(title__contains=question) | Q(text__contains=question))

        if not self.sort_by_date:
            queryset = self.sort_by_like(queryset)
            return queryset

        return queryset.order_by("date_create")


class TagDetail(DetailView, QuestionMixin):
    model = Tag
    template_name = "question/tag_detail.html"
    pk_url_kwarg = "name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context['object'].questions.all()
        activities = self.get_related_activities(queryset)
        context['object'] = activities.object_list
        context['page_obj'] = activities
        context['populate_q'] = self.get_context_populate_q()
        return context


class QuestionDetail(DetailView, QuestionMixin):
    model = Questions
    template_name = "question/question_detail.html"
    pk_url_kwarg = "id"
    login_url = '/account/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = context['object'].answers.all()
        activities = self.get_related_activities(answers)
        context["page_obj"] = activities
        context['answers'] = activities.object_list
        context['answer_form'] = AnswerForm()
        context['populate_q'] = self.get_context_populate_q()
        return context

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)

        form = AnswerForm(request.POST)
        if form.is_valid():
            Answer.objects.create(
                text=form.cleaned_data['text'],
                author=request.user,
                question=Questions.objects.get(id=kwargs['id'])
            )
            redirect(request.path)
        return redirect(request.path)


class QuestionAddView(LoginRequiredMixin, CreateView):
    login_url = '/account/login/'
    form_class = QuestionForm
    template_name = "question/question_create.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request):
        question_form = self.form_class(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            tags = question_form.cleaned_data['tags']
            if tags:
                tags = self.create_tag(tags)
                for tag in tags:
                    question.tags.add(tag)
            return redirect(question.get_absolute_url())
        return render(request, "question/question_list.html", {"form": question_form})

    @staticmethod
    def create_tag(tags):
        for name_tag in tags:
            try:
                tag = Tag.objects.get(name=name_tag)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(name=name_tag)
            yield tag


class ChangeLikeDisView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        id_obj = kwargs['id']
        type_obj = kwargs['type']
        action = kwargs['action']
        if type_obj == 'answer':
            obj = Answer.objects.get(id=id_obj)
            path_redirect = obj.question.get_absolute_url()
        else:
            obj = Questions.objects.get(id=id_obj)
            path_redirect = obj.get_absolute_url()
        obj.vote(request.user, action)
        return redirect(path_redirect)


'''############# REST API ################'''


class QAMixin:
    def get_serializer_class(self):
        if self.action in self.serializers_class:
            return self.serializers_class[self.action]
        return self.serializers_class['default']


class QuestionsViewSet(QAMixin, ModelViewSet):
    queryset = Questions.objects.all()
    serializers_class = {
        'default': QuestionsListSerializer,
        'retrieve': QuestionDetailSerializer,
    }
    http_method_names = ['get', 'post', 'head']
    permission_classes = [IsAuthenticated]


class AnswerViewSet(QAMixin, ModelViewSet):
    queryset = Answer.objects.all()
    serializers_class = {
        'default': AnswerSerializer,
        'create': AnswerCreteSerializer,
    }
    http_method_names = ['get', 'post', 'head', ]
    permission_classes = [IsAuthenticated]
