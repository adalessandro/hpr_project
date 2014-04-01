# -*- coding: utf-8 -*-

import datetime
import mimetypes
import re

from os.path import abspath, dirname

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.db.models import Q
from django.db.models.fields.related import ManyToManyField

from crispy_forms.bootstrap import UneditableField

from core.views import PaginationOverflowMixin, SessionMixin

from .models import EntradaAnalisis, EntradaAnalisisAdjunto,\
    DeterminacionEstudioNeonatologia

from .forms import EntradaAnalisisForm,\
    EntradaAnalisisBuscarForm, EntradaAnalisisAdjuntoCreateForm,\
    EntradaAnalisisFechaIrForm


class NeonatologiaAnalisisTopNavBar(object):
    def get_context_data(self, **kwargs):
        context = super(NeonatologiaAnalisisTopNavBar, self).\
            get_context_data(**kwargs)
        context["active"] = "neonatologia_analisis_index"
        return context


class TitleView(object):
    title = ""

    def get_context_data(self, **kwargs):
        context = super(TitleView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context


class IndexView(NeonatologiaAnalisisTopNavBar, TemplateView):
    template_name = "neonatologia_analisis_app/index.html"


class EntradaAnalisisListView(
    SessionMixin, PaginationOverflowMixin,
    NeonatologiaAnalisisTopNavBar, TitleView, ListView
):

    # Listview parms
    model = EntradaAnalisis
    paginate_by = 10
    # Titleview parms
    title = "Listado de Pedidos"
    # Forms
    formBuscar_class = EntradaAnalisisBuscarForm
    formFechaIr_class = EntradaAnalisisFechaIrForm

    def post(self, request, *args, **kwargs):
        # formBuscar
        stringBuscar = self.request.POST.get('stringBuscar', None)
        campoBuscar = self.request.POST.get('campoBuscar', None)
        submitBuscar = self.request.POST.get('submitBuscar', None)

        if submitBuscar == 'Filtrar':
            self.set_session('stringBuscar', stringBuscar)
            self.set_session('campoBuscar', campoBuscar)
            self.set_session('submitBuscar', submitBuscar)
        elif submitBuscar == 'Reiniciar':
            self.set_session('stringBuscar', None)
            self.set_session('campoBuscar', 'id')
            self.set_session('submitBuscar', None)

        # formFechaIr
        fechaIr = self.request.POST.get('fechaIr', None)
        submitIr = self.request.POST.get('submitIr', None)
        if submitIr == 'Ir':
            self.set_session('fechaIr', fechaIr)
            self.set_session('submitIr', submitIr)

        return super(EntradaAnalisisListView, self).get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        return super(EntradaAnalisisListView, self).get(request, args, kwargs)

    def get_queryset(self):

        # estado Top Buttons
        btn_filter = self.kwargs['estado']
        if btn_filter == 'todos':
            qs = self.model.objects.filter(estado='A')
        elif btn_filter == 'eliminado':
            qs = self.model.objects.filter(estado='E')
        elif btn_filter == 'urgente':
            qs = self.model.objects.filter(estado='A')
            qs = qs.filter(prioridad='U')
            qs = qs.exclude(etapa='COM')
        elif btn_filter == 'retrasado':
            qs = self.model.objects.filter(estado='A')
            qs_ids = [o.id for o in qs if o.is_analisis_retraso()]
            qs = qs.filter(id__in=qs_ids)
            qs = qs.exclude(etapa='COM')
        elif btn_filter == 'trabsoc':
            qs = self.model.objects.filter(estado='A')
            qs_ids = [o.id for o in qs if o.is_analisis_retraso()]
            qs = qs.filter(Q(etapa='NTS') | Q(id__in=qs_ids))
        elif btn_filter == 'notif':
            qs = self.model.objects.filter(estado='A')
            qs_ids = [o.id for o in qs if o.is_analisis_retraso()]
            qs = qs.filter(Q(etapa='NOT') | Q(id__in=qs_ids))
        elif btn_filter == 'completado':
            qs = self.model.objects.filter(estado='A')
            qs = qs.filter(etapa='COM')
        else:
            qs = self.model.objects.all()

        # formFechaIr
        fechaIr = self.get_session('fechaIr')
        dict = {
            'fechaIr': fechaIr,
        }
        qdict = QueryDict('')
        qdict = qdict.copy()
        qdict.update(dict)
        formFechaIr = self.formFechaIr_class(qdict)

        if formFechaIr.is_valid():
            f = fechaIr.split('/')
            month = f[0]
            year = f[1]
            self.set_session(
                'fechaFiltrado',
                datetime.date(int(year), int(month), 1).toordinal()
            )
        else:
            fechaFiltrado_ord = self.get_session('fechaFiltrado') or\
                datetime.date.today().toordinal()
            fechaFiltrado = datetime.date.fromordinal(fechaFiltrado_ord)
            month = fechaFiltrado.month
            year = fechaFiltrado.year
        qs = qs.filter(fecha__year=int(year))
        qs = qs.filter(fecha__month=int(month))

        # formBuscar
        stringBuscar = self.get_session('stringBuscar')
        campoBuscar = self.get_session('campoBuscar')
        dict = {
            'stringBuscar': stringBuscar,
            'campoBuscar': campoBuscar,
        }
        qdict = QueryDict('')
        qdict = qdict.copy()
        qdict.update(dict)
        formBuscar = self.formBuscar_class(qdict)

        if formBuscar.is_valid():
            if campoBuscar == 'id':
                try:
                    isinstance(int(stringBuscar), int)
                    filter_dict = {campoBuscar: stringBuscar}
                    qs = qs.filter(**filter_dict)
                except:
                    pass
            elif campoBuscar in [
                'fecha', 'fecha_nacimiento', 'muestra_fecha_1',
                'muestra_fecha_2', 'fecha_notif_familia'
            ]:
                f = stringBuscar.split('/')
                f_dia = int(f[0])
                f_mes = int(f[1])
                f_ano = int(f[2])
                fecha = datetime.date(f_ano, f_mes, f_dia)
                filter_dict = {campoBuscar: fecha}
                qs = qs.filter(**filter_dict)
            elif campoBuscar in [
                'apellido', 'nombre', 'apellido_madre',
                'nombre_madre', 'notificar_trabsoc'
            ]:
                filter_dict = {
                    campoBuscar + '__contains': stringBuscar
                }
                qs = qs.filter(**filter_dict)
            elif campoBuscar in ['determinaciones']:
                filter_dict = {campoBuscar + '__in': stringBuscar}
                qs = qs.filter(**filter_dict)
            else:
                pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(EntradaAnalisisListView, self).\
            get_context_data(**kwargs)

        # formBuscar
        stringBuscar = self.get_session('stringBuscar')
        campoBuscar = self.get_session('campoBuscar')
        submitBuscar = self.get_session('submitBuscar')
        if submitBuscar == 'Filtrar':
            dict = {
                'stringBuscar': stringBuscar or '',
                'campoBuscar': campoBuscar or '',
            }
            qdict = QueryDict('')
            qdict = qdict.copy()
            qdict.update(dict)
            formBuscar = self.formBuscar_class(qdict)
            context['formBuscar'] = formBuscar
        else:
            formBuscar = self.formBuscar_class(initial={
                'stringBuscar': stringBuscar or '',
                'campoBuscar': campoBuscar or '',
            })
            context['formBuscar'] = formBuscar

        # formFechaIr
        fechaIr = self.get_session('fechaIr') or\
            datetime.date.today().strftime('%m/%Y')
        submitIr = self.get_session('submitIr')
        fechaFiltrado_ord = self.get_session('fechaFiltrado') or\
            datetime.date.today().toordinal()
        fechaFiltrado = datetime.date.fromordinal(fechaFiltrado_ord)

        if submitIr == 'Ir':
            dict = {
                'fechaIr': fechaIr or '',
            }
            qdict = QueryDict('')
            qdict = qdict.copy()
            qdict.update(dict)
            formFechaIr = self.formFechaIr_class(qdict)
            context['formFechaIr'] = formFechaIr
        else:
            formFechaIr = self.formFechaIr_class(initial={
                'fechaIr': fechaIr or '',
            })
            context['formFechaIr'] = formFechaIr

        year = fechaFiltrado.year
        month = fechaFiltrado.month
        date_filter = datetime.date(int(year), int(month), 1)
        context['date'] = date_filter

        # Top Buttons
        btn_filter = self.kwargs['estado']
        top_btns = []
        # Botón ver eliminados
        btn = {}
        btn['class'] = 'btn-default'
        if btn_filter == 'todos':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-home'
        btn['text'] = 'Todos'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'todos'
        top_btns.append(btn)
        # Botón ver urgentes
        btn = {}
        btn['class'] = 'btn-default'
        if btn_filter == 'urgente':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-exclamation-sign'
        btn['text'] = 'Urgentes'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'urgente'
        top_btns.append(btn)
        # Botón ver retrasados
        btn = {}
        btn['class'] = 'btn-default'
        if btn_filter == 'retrasado':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-time'
        btn['text'] = 'Retrasados'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'retrasado'
        top_btns.append(btn)
        # Botón ver eliminados
        btn = {}
        btn['class'] = 'btn-danger'
        if btn_filter == 'eliminado':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-trash'
        btn['text'] = 'Eliminados'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'eliminado'
        top_btns.append(btn)
        # Botón ver Notificar Trab. Soc.
        btn = {}
        btn['class'] = 'btn-warning'
        if btn_filter == 'trabsoc':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-phone-alt'
        btn['text'] = 'Notificar Trab. Soc.'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'trabsoc'
        top_btns.append(btn)
        # Botón ver notificados
        btn = {}
        btn['class'] = 'btn-info'
        if btn_filter == 'notif':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-eye-open'
        btn['text'] = 'Notificados'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'notif'
        top_btns.append(btn)
        # Botón ver completados
        btn = {}
        btn['class'] = 'btn-success'
        if btn_filter == 'completado':
            btn['class'] += ' active '
        btn['icon'] = 'glyphicon-ok-sign'
        btn['text'] = 'Completados'
        btn['url'] = 'entradaanalisis_list'
        btn['url_args'] = 'completado'
        top_btns.append(btn)

        context['top_btns'] = top_btns

        # Select determinaciones
        det_options = []
        det_option = {}
        for det in DeterminacionEstudioNeonatologia.objects.all():
            det_option['id'] = det.id
            det_option['nombre'] = det.nombre
            det_options.append(det_option)
            det_option = {}

        context['det_options'] = det_options

        return context

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.view_entrada_analisis',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisListView, self).dispatch(*args, **kwargs)


class EntradaAnalisisCreateView(NeonatologiaAnalisisTopNavBar, TitleView,
                                CreateView):
    model = EntradaAnalisis
    template_name = 'neonatologia_analisis_app/entradaanalisis_form.html'
    form_class = EntradaAnalisisForm
    success_url = reverse_lazy(
        'entradaanalisis_list', kwargs={'estado': 'todos'}
    )
    title = "Ingresar Pedido"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Set estado
        self.object.estado = 'A'
        # Set etapa
        if not self.object.muestra_num_2 == '':
            self.object.etapa = 'COM'
        elif self.object.fecha_notif_familia is not None:
            self.object.etapa = 'NOT'
        elif self.object.notificar_trabsoc == 'SI':
            self.object.etapa = 'NTS'
        else:
            self.object.etapa = 'INI'
        # Set Timestampedmodel attrs
        self.object.created = datetime.datetime.now()
        self.object.created_user = self.request.user
        # Save object
        self.object.save()
        # Save many to many relationships
        if 'determinaciones' not in form.uneditablefields:
            form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class):
        form = super(EntradaAnalisisCreateView, self).get_form(form_class)
        user = self.request.user

        uneditablefields = set(form.fields)
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_neo'
        ):
            uneditablefields.discard('fecha')
            uneditablefields.discard('prioridad')
            uneditablefields.discard('sexo')
            uneditablefields.discard('apellido')
            uneditablefields.discard('nombre')
            uneditablefields.discard('fecha_nacimiento')
            uneditablefields.discard('apellido_madre')
            uneditablefields.discard('nombre_madre')
            uneditablefields.discard('doc_tipo_madre')
            uneditablefields.discard('doc_num_madre')
            uneditablefields.discard('domicilio')
            uneditablefields.discard('telefono')
            uneditablefields.discard('determinaciones')
            uneditablefields.discard('muestra_fecha_1')
            uneditablefields.discard('muestra_num_1')
            uneditablefields.discard('notificar_trabsoc')
            uneditablefields.discard('neonatologia_obs')
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_trabsoc'
        ):
            uneditablefields.discard('fecha_notif_familia')
            uneditablefields.discard('trabsoc_obs')
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_lab'
        ):
            uneditablefields.discard('muestra_fecha_2')
            uneditablefields.discard('muestra_num_2')
            uneditablefields.discard('muestra_texto_2')
            uneditablefields.discard('laboratorio_obs')

        for f in uneditablefields:
            form.helper[f].wrap(UneditableField)

        form.uneditablefields = uneditablefields

        return form

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.create_entrada_analisis',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisCreateView, self).dispatch(*args, **kwargs)


class EntradaAnalisisDeleteView(NeonatologiaAnalisisTopNavBar, TitleView,
                                DeleteView):
    model = EntradaAnalisis
    success_url = reverse_lazy(
        'entradaanalisis_list', kwargs={'estado': 'todos'}
    )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 'E'
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.delete_entrada_analisis',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisDeleteView, self).dispatch(*args, **kwargs)


@permission_required('neonatologia_analisis_app.restore_entrada_analisis')
def EntradaAnalisisRestore(request, pk):
    model = EntradaAnalisis
    success_url = reverse_lazy(
        'entradaanalisis_list', kwargs={'estado': 'todos'}
    )

    try:
        isinstance(int(pk), int)
    except:
        raise Http404("La página solicitada no existe")
    pk = int(pk)
    obj = get_object_or_404(model, id=pk)
    if not obj.estado == 'E':
        raise Http404("La página solicitada no existe")
    obj.estado = 'A'
    obj.save()
    return HttpResponseRedirect(success_url)


class EntradaAnalisisUpdateView(NeonatologiaAnalisisTopNavBar, TitleView,
                                UpdateView):
    model = EntradaAnalisis
    template_name = 'neonatologia_analisis_app/entradaanalisis_form.html'
    form_class = EntradaAnalisisForm
    success_url = reverse_lazy(
        'entradaanalisis_list', kwargs={'estado': 'todos'}
    )
    title = "Editar Entrada"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Set etapa
        if not self.object.muestra_num_2 == '':
            self.object.etapa = 'COM'
        elif self.object.fecha_notif_familia is not None:
            self.object.etapa = 'NOT'
        elif self.object.notificar_trabsoc == 'SI':
            self.object.etapa = 'NTS'
        else:
            self.object.etapa = 'INI'
        # Set Timestampedmodel attrs
        self.object.created = datetime.datetime.now()
        self.object.created_user = self.request.user
        # Save object
        self.object.save()
        # Save many to many relationships
        if 'determinaciones' not in form.uneditablefields:
            form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class):
        form = super(EntradaAnalisisUpdateView, self).get_form(form_class)
        user = self.request.user

        uneditablefields = set(form.fields)
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_neo'
        ):
            uneditablefields.discard('fecha')
            uneditablefields.discard('prioridad')
            uneditablefields.discard('sexo')
            uneditablefields.discard('apellido')
            uneditablefields.discard('nombre')
            uneditablefields.discard('fecha_nacimiento')
            uneditablefields.discard('apellido_madre')
            uneditablefields.discard('nombre_madre')
            uneditablefields.discard('doc_tipo_madre')
            uneditablefields.discard('doc_num_madre')
            uneditablefields.discard('domicilio')
            uneditablefields.discard('telefono')
            uneditablefields.discard('determinaciones')
            uneditablefields.discard('muestra_fecha_1')
            uneditablefields.discard('muestra_num_1')
            uneditablefields.discard('notificar_trabsoc')
            uneditablefields.discard('neonatologia_obs')
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_trabsoc'
        ):
            uneditablefields.discard('fecha_notif_familia')
            uneditablefields.discard('trabsoc_obs')
        if user.has_perm(
            'neonatologia_analisis_app.change_entrada_analisis_lab'
        ):
            uneditablefields.discard('muestra_fecha_2')
            uneditablefields.discard('muestra_num_2')
            uneditablefields.discard('muestra_texto_2')
            uneditablefields.discard('laboratorio_obs')

        for f in uneditablefields:
            form.helper[f].wrap(UneditableField)

        form.uneditablefields = uneditablefields

        return form

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.view_entrada_analisis',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisUpdateView, self).dispatch(*args, **kwargs)


@permission_required('neonatologia_analisis_app.view_entrada_analisis')
def export_to_excel(request, pk):
    model = EntradaAnalisis
    obj = get_object_or_404(model, id=pk)
    template_name = "neonatologia_analisis_app/entradaanalisis_csv.html"
    content = [
        {
            'title': 'Neonatología',
            'fields': (
                'fecha',
                'prioridad',
                'apellido',
                'nombre',
                'sexo',
                'fecha_nacimiento',
                'apellido_madre',
                'nombre_madre',
                'doc_tipo_madre',
                'doc_num_madre',
                'domicilio',
                'telefono',
                'determinaciones',
                'muestra_fecha_1',
                'muestra_num_1',
                'notificar_trabsoc',
                'neonatologia_obs',
            )
        },
        {
            'title': 'Trabajo social',
            'fields': (
                'fecha_notif_familia',
                'trabsoc_obs',
            )
        },
        {
            'title': 'Laboratorio',
            'fields': (
                'muestra_fecha_2',
                'muestra_num_2',
                'muestra_texto_2',
                'laboratorio_obs',
            )
        },
    ]
    values = []
    for block in content:
        value = (block['title'], '')
        values.append(value)
        values.append(('', ''))
        for field_name in block['fields']:
            field = model._meta.get_field(field_name)
            if isinstance(field, ManyToManyField):
                field_value = getattr(obj, field_name).values()
                if field.name == 'determinaciones':
                    field_value = map(lambda x: x['nombre'], field_value)
                value = (field.verbose_name, field_value)
            else:
                value = (field.verbose_name, obj._get_FIELD_display(field))
            values.append(value)
        values.append(('', ''))
        values.append(('', ''))
    response = render_to_response(template_name, {'values': values})

    #output file
    filename = "model.csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response


class EntradaAnalisisAdjuntoList(NeonatologiaAnalisisTopNavBar, TitleView,
                                 CreateView):
    model = EntradaAnalisisAdjunto
    parent_model = EntradaAnalisis
    title = "Listado de Adjuntos"
    template_name =\
        "neonatologia_analisis_app/entradaanalisisadjunto_list.html"
    form_class = EntradaAnalisisAdjuntoCreateForm

    def form_valid(self, form):
        if not self.request.user.has_perm(
            'neonatologia_analisis_app.create_entrada_analisis_adjunto'
        ):
            raise PermissionDenied()
        pk = self.kwargs.get('pk', None)
        try:
            isinstance(int(pk), int)
        except:
            raise Http404("La página solicitada no existe")
        pk = int(pk)
        parent_obj = get_object_or_404(self.parent_model, id=pk)
        self.object = form.save(commit=False)
        self.object.entrada_analisis = parent_obj
        self.object.created = datetime.datetime.now()
        self.object.created_user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_parent_obj(self):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Http404("La página solicitada no existe")
        parent_obj = get_object_or_404(self.parent_model, id=pk)
        return parent_obj

    def get_queryset(self):
        parent_obj = self.get_parent_obj()
        queryset = self.model.objects.filter(entrada_analisis=parent_obj)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntradaAnalisisAdjuntoList, self).\
            get_context_data(**kwargs)
        context['parent_obj'] = self.get_parent_obj()
        context['object_list'] = self.get_queryset()
        error_code = self.request.GET.get('e', None)
        if error_code == '1':
            error = {
                'class': 'alert-danger',
                'title': 'Error',
                'text': 'No se ha podido descargar el archivo.'
            }
            context['error'] = error
        elif error_code == '2':
            error = {
                'class': 'alert-danger',
                'title': 'Error',
                'text': 'El archivo supera el límite.'
            }
            context['error'] = error
        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk', None)
        try:
            isinstance(int(pk), int)
        except:
            raise Http404("La página solicitada no existe")
        pk = int(pk)
        success_url = reverse_lazy('entradaanalisisadjunto_list', args=[pk])
        return success_url

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.view_entrada_analisis_adjunto',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisAdjuntoList, self).\
            dispatch(*args, **kwargs)


class EntradaAnalisisAdjuntoDeleteView(
    NeonatologiaAnalisisTopNavBar, TitleView, DeleteView
):
    model = EntradaAnalisisAdjunto
    parent_model = EntradaAnalisis

    def get_context_data(self, **kwargs):
        context = super(EntradaAnalisisAdjuntoDeleteView, self).\
            get_context_data(**kwargs)
        self.object = self.get_object()
        self.parent_pk = self.object.entrada_analisis.id
        context['parent_pk'] = self.parent_pk
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.parent_pk = self.object.entrada_analisis.id
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs.get('pk', None)
        try:
            isinstance(int(pk), int)
        except:
            raise Http404("La página solicitada no existe")
        pk = int(pk)
        success_url = reverse_lazy(
            'entradaanalisisadjunto_list',
            args=[self.parent_pk]
        )
        return success_url

    @method_decorator(
        permission_required(
            'neonatologia_analisis_app.delete_entrada_analisis_adjunto',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(EntradaAnalisisAdjuntoDeleteView, self).\
            dispatch(*args, **kwargs)


@permission_required(
    'neonatologia_analisis_app.view_entrada_analisis_adjunto'
)
def EntradaAnalisisAdjuntoDownload(request, pk):
    model = EntradaAnalisisAdjunto

    try:
        isinstance(int(pk), int)
    except:
        raise Http404("La página solicitada no existe")
    pk = int(pk)
    obj = get_object_or_404(model, id=pk)
    try:
        fsock = open(obj.adjunto.path, 'r')
        name = str(obj.filename().encode("utf-8"))
        mimetype = mimetypes.guess_type(name, True)
        if mimetype[0] is None:
            mimetype_file = 'binary/octet-stream'
        else:
            mimetype_file = mimetype[0]
        response = HttpResponse(fsock, mimetype=mimetype_file)
        response['Content-Disposition'] =\
            "attachment; filename=\"%s\"" % obj.filename()
        return response
    except:
        parent_pk = obj.entrada_analisis.id
        redirect_url = reverse(
            'entradaanalisisadjunto_list',
            args=[parent_pk]
        ) + '?e=1'
        return HttpResponseRedirect(redirect_url)


def EntradaAnalisisExcelImport(request):

    if not request.user.is_superuser:
        raise PermissionDenied()

    csv_splitter = ","
    FILE_PATH = dirname(abspath(__file__))
    input_file_path = FILE_PATH + "/others/import.csv"

    # open input
    input_file = open(input_file_path, "r")

    # processing the input, omit header
    input_file.readline()

    # parse input
    for line in input_file:
        line = line.rstrip('\r\n')
        words = line.split(csv_splitter)
        # omitir columna de estado de migracion
        apellido = words[1]
        nombre = words[2]
        apellido_madre = words[3]
        nombre_madre = words[4]
        fecha_nacimiento = words[5]
        domicilio = words[6]
        telefono = words[7]
        # omitir determinaciones
        muestra_fecha_1 = words[9]
        muestra_num_1 = words[10]
        notificar_trabsoc = words[11]
        fecha_notif_familia = words[12]
        muestra_fecha_2 = words[13]
        muestra_num_2 = words[14]
        laboratorio_obs = words[15]
        trabsoc_obs = words[16]

        # checking
        if not apellido:
            continue
        if not nombre:
            continue
        if not apellido_madre:
            apellido_madre = '?'
        if not nombre_madre:
            nombre_madre = '?'
        if not fecha_nacimiento:
            fecha_nacimiento = datetime.date.today()
        else:
            if (re.match('^\d\d/\d\d/\d\d\d\d$', fecha_nacimiento)):
                f = fecha_nacimiento.split('/')
                day = f[0]
                month = f[1]
                year = f[2]
                fecha_nacimiento =\
                    datetime.date(int(year), int(month), int(day))
            else:
                fecha_nacimiento = datetime.date.today()
        if not muestra_fecha_1:
            muestra_fecha_1 = None
        else:
            if (re.match('^\d\d/\d\d/\d\d\d\d$', muestra_fecha_1)):
                f = muestra_fecha_1.split('/')
                day = f[0]
                month = f[1]
                year = f[2]
                muestra_fecha_1 =\
                    datetime.date(int(year), int(month), int(day))
            else:
                muestra_fecha_1 = None
        if notificar_trabsoc and\
                notificar_trabsoc in ['si', 'SI', 'sí', 'SÍ']:
            notificar_trabsoc = 'SI'
        else:
            notificar_trabsoc = 'NO'
        if not fecha_notif_familia:
            fecha_notif_familia = None
        else:
            if (re.match('^\d\d/\d\d/\d\d\d\d$', fecha_notif_familia)):
                f = fecha_notif_familia.split('/')
                day = f[0]
                month = f[1]
                year = f[2]
                fecha_notif_familia =\
                    datetime.date(int(year), int(month), int(day))
            else:
                fecha_notif_familia = None
        if not muestra_fecha_2:
            muestra_fecha_2 = None
        else:
            if (re.match('^\d\d/\d\d/\d\d\d\d$', muestra_fecha_2)):
                f = muestra_fecha_2.split('/')
                day = f[0]
                month = f[1]
                year = f[2]
                muestra_fecha_2 =\
                    datetime.date(int(year), int(month), int(day))
            else:
                muestra_fecha_2 = None

        fecha = fecha_nacimiento
        created = datetime.datetime.now()
        created_user = request.user
        doc_tipo_madre = 'DNI'
        doc_num_madre = 11111111

        try:
            obj = EntradaAnalisis(
                fecha=fecha,
                apellido=apellido,
                nombre=nombre,
                apellido_madre=apellido_madre,
                nombre_madre=nombre_madre,
                doc_tipo_madre=doc_tipo_madre,
                doc_num_madre=doc_num_madre,
                fecha_nacimiento=fecha_nacimiento,
                domicilio=domicilio,
                telefono=telefono,
                muestra_fecha_1=muestra_fecha_1,
                muestra_num_1=muestra_num_1,
                notificar_trabsoc=notificar_trabsoc,
                fecha_notif_familia=fecha_notif_familia,
                muestra_fecha_2=muestra_fecha_2,
                muestra_num_2=muestra_num_2,
                laboratorio_obs=laboratorio_obs,
                trabsoc_obs=trabsoc_obs,
                created=created,
                created_user=created_user
            )
            etapa = obj.get_current_etapa()
            obj.etapa = etapa
            obj.save()
        except:
            raise
    return HttpResponse("")
