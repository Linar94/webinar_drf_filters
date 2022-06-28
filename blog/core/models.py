from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models


class Comment(models.Model):
    """ Модель для создания группы в соц.сети. """

    title = models.CharField(max_length=200)

    class Meta:
        abstract = True
