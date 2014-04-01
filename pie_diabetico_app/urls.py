# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns(
    '',
    url(
        r'^$',
        login_required(views.IndexView.as_view()),
        name='pie_diabetico_index'
    ),
    url(
        r'^list/(?P<estado>[\w]+)/$',
        login_required(views.HistoriaClinicaListView.as_view()),
        name='historiaclinica_list'
    ),
    url(
        r'^create/$',
        login_required(views.HistoriaClinicaCreateView.as_view()),
        name='historiaclinica_create'
    ),
    url(
        r'^delete/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaDeleteView.as_view()),
        name='historiaclinica_delete'
    ),
    url(
        r'^restore/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaRestore),
        name='historiaclinica_restore'
    ),
    url(
        r'^update/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaUpdateView.as_view()),
        name='historiaclinica_update'
    ),
    url(
        r'^excel/(?P<pk>[\d]+)/$',
        login_required(views.export_to_excel),
        name='historiaclinica_excel'
    ),
    url(
        r'^files/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaAdjuntoList.as_view()),
        name='historiaclinicaadjunto_list'
    ),
    url(
        r'^files/download/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaAdjuntoDownload),
        name='historiaclinicaadjunto_download'
    ),
    url(
        r'^files/delete/(?P<pk>[\d]+)/$',
        login_required(views.HistoriaClinicaAdjuntoDeleteView.as_view()),
        name='historiaclinicaadjunto_delete'
    ),
)
