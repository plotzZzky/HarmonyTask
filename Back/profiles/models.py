from django.db import models
from django.contrib.auth.models import User
import os
import uuid


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profiles/', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to=get_file_path)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    area = models.CharField(max_length=128)
    profession = models.CharField(max_length=128)
    email = models.EmailField()
    telephone = models.CharField(max_length=255)
    description = models.CharField()
    active = models.CharField(default=True)  # Se o perfil estiver inativo ele não ser exibido

    objects = models.Manager()


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    professional = models.OneToOneField(Profile, on_delete=models.CASCADE)

    objects = models.Manager()
