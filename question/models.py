from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class MessageQA(models.Model):

    text = models.TextField(max_length=5000)
    date_create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
    dislike = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislakes')

    class Meta:
        abstract = True

    @property
    def votes(self):
        return self.like.count() - self.dislike.count()


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Questions(MessageQA):
    max_tag = 3
    title = models.CharField(max_length=200)

    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'id': self.id})


class Answer(MessageQA):
    text = models.TextField(max_length=5000)

    question = models.ForeignKey(Questions, related_name="answers", on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="a_like")
    dislike = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="a_dislike")