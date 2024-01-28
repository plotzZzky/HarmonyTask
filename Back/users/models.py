from django.db import models
from django.contrib.auth.models import User


class Recovery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    question = models.CharField()
    answer = models.CharField()

    objects = models.Manager()
