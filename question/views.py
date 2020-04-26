from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (ListView, DetailView,
                                  CreateView)

from .models import Questions, Tag
from .form import QuestionForm


class QuestionList(ListView):
    model = Questions
    template_name = 'question/question_list.html'


class TagDetail(DetailView):
    model = Tag
    template_name = "question/tag_detail.html"
    pk_url_kwarg = "name"


class QuestionDetail(DetailView):
    model = Questions
    template_name = "question/question_detail.html"
    pk_url_kwarg = "id"


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
            tags = self.create_tag(question_form.cleaned_data['tags'])
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


