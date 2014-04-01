# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import DeterminacionEstudioNeonatologia


class DeterminacionEstudioNeonatologiaAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    DeterminacionEstudioNeonatologia,
    DeterminacionEstudioNeonatologiaAdmin
)
