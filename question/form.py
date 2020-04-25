from django import forms
from django.core.exceptions import ValidationError

from .models import Questions


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['title', 'text', 'tags', ]

    tags = forms.CharField(required=False)

    def clean_tags(self):
        new_tags = self.cleaned_data['tags']
        new_tags = new_tags.split(',')

        if len(new_tags) > self.instance.max_tag:
            raise ValidationError('Number of tags cannot be more than 3')

        return new_tags


