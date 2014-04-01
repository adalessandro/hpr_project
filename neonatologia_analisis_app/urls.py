# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns(
    '',
    url(
        r'^$',
        login_required(views.IndexView.as_view()),
        name='neonatologia_analisis_index'
    ),
    url(
        r'^list/(?P<estado>[\w]+)/$',
        login_required(views.EntradaAnalisisListView.as_view()),
        name='entradaanalisis_list'
    ),
    url(
        r'^create/$',
        login_required(views.EntradaAnalisisCreateView.as_view()),
        name='entradaanalisis_create'
    ),
    url(
        r'^delete/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisDeleteView.as_view()),
        name='entradaanalisis_delete'
    ),
    url(
        r'^restore/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisRestore),
        name='entradaanalisis_restore'
    ),
    url(
        r'^import/$',
        login_required(views.EntradaAnalisisExcelImport),
        name='entradaanalisis_import'
    ),
    url(
        r'^update/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisUpdateView.as_view()),
        name='entradaanalisis_update'
    ),
    url(
        r'^excel/(?P<pk>[\d]+)/$',
        login_required(views.export_to_excel),
        name='entradaanalisis_excel'
    ),
    url(
        r'^files/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisAdjuntoList.as_view()),
        name='entradaanalisisadjunto_list'
    ),
    url(
        r'^files/download/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisAdjuntoDownload),
        name='entradaanalisisadjunto_download'
    ),
    url(
        r'^files/delete/(?P<pk>[\d]+)/$',
        login_required(views.EntradaAnalisisAdjuntoDeleteView.as_view()),
        name='entradaanalisisadjunto_delete'
    ),
)
