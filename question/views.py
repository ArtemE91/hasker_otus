from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (ListView, DetailView,
                                  CreateView, View)
from django.db.models import Q, Count, F
from .models import Questions, Tag, Answer
from .form import QuestionForm, AnswerForm


class QuestionList(ListView):
    model = Questions
    template_name = 'question/question_list.html'

    def get_queryset(self):
        queryset = Questions.objects.all()
        question = self.request.GET.get("q")
        if question and 'tag:' in question:
            name_tag = question.split('tag:')[-1]
            tag = get_object_or_404(Tag, name=name_tag)
            queryset = tag.questions.all()
        elif question:
            queryset = queryset.filter(Q(title__contains=question) | Q(text__contains=question))

        queryset = queryset.annotate(
                likes=Count("like"),
                dislikes=Count("dislike"),
            ).order_by(F("dislikes") - F("likes"), "-date_create")

        return queryset


class TagDetail(DetailView):
    model = Tag
    template_name = "question/tag_detail.html"
    pk_url_kwarg = "name"


class QuestionDetail(DetailView):
    model = Questions
    template_name = "question/question_detail.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        answers = context['object'].answers.all().annotate(
            likes=Count("like"),
            dislikes=Count("dislike"),
        ).order_by(F("dislikes") - F("likes"), '-date_create')

        context['answers'] = answers
        context['answer_form'] = AnswerForm()
        return context

    def post(self, request, **kwargs):
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
