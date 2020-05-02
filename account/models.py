from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class Account(AbstractUser):
    avatar = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    date_of_create = models.DateTimeField(auto_now_add=True)

    def check_password(self, password):
        if self.password == password:
            return True
        return False

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'id': self.id})


