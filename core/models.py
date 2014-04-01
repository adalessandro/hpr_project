# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating "created" and "modified" fields.
    """
    created = models.DateTimeField()
    created_user = models.ForeignKey(User)

    class Meta:
        abstract = True
