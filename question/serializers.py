from rest_framework import serializers

from .models import Tag, Questions, Answer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuestionsListSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Questions
        fields = ['id', 'title', 'text', 'date_create', 'author', 'tags']


class QuestionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ['id', 'title', 'text', 'date_create', 'author', 'tags', 'answers']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['text', 'date_create', 'author', 'question']


class AnswerCreteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text', 'question']