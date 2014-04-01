# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import core.views as coreviews

urlpatterns = patterns(
    '',
    url(
        r'^$',
        login_required(TemplateView.as_view(template_name='index.html')),
        name='dermatologia_index'
    ),
    # Examples:
    # url(r'^$', 'discapacidad_project.views.home', name='home'),
    # url(r'^discapacidad_project/', include('discapacidad_project.foo.urls')),
    url(r'^pie_diabetico/', include('pie_diabetico_app.urls')),
    url(r'^neonatologia_analisis/', include('neonatologia_analisis_app.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', coreviews.login_user, name='login_view'),
    url(
        r'^accounts/logout/$',
        login_required(coreviews.logout_user),
        name='logout_view'
    ),
)
