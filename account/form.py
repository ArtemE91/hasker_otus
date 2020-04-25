from django import forms
from django.core.exceptions import ValidationError

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("username", "email", "password", "avatar", )

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def clean_username(self):
        new_username = self.cleaned_data['username']

        if Account.objects.filter(username__iexact=new_username).count():
            raise ValidationError('Such username is already registered!')

        return new_username
