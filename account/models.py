from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class Account(AbstractUser):
    avatar = models.FileField(upload_to='avatars', null=True, blank=True)
    date_of_create = models.DateTimeField(auto_now_add=True)

    def check_password(self, password):
        if self.password == password:
            return True
        return False

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'id': self.id})


