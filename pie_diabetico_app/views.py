# -*- coding: utf-8 -*-

import datetime
import re
import mimetypes

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from crispy_forms.bootstrap import UneditableField

from core.views import PaginationOverflowMixin, SessionMixin

from .models import HistoriaClinica, HistoriaClinicaAdjunto
from .forms import HistoriaClinicaForm, HistoriaClinicaBuscarForm,\
    HistoriaClinicaAdjuntoCreateForm


class PieDiabeticoTopNavBar(object):
    def get_context_data(self, **kwargs):
        context = super(PieDiabeticoTopNavBar, self).get_context_data(**kwargs)
        context["active"] = "pie_diabetico_index"
        return context


class TitleView(object):
    title = ""

    def get_context_data(self, **kwargs):
        context = super(TitleView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context


class IndexView(PieDiabeticoTopNavBar, TemplateView):
    template_name = "pie_diabetico_app/index.html"


class HistoriaClinicaListView(
    SessionMixin, PaginationOverflowMixin,
    PieDiabeticoTopNavBar, TitleView, ListView
):
    model = HistoriaClinica
    paginate_by = 10
    title = "Listado de Fichas"
    form_class = HistoriaClinicaBuscarForm

    session_prefix = "HistoriaClinicaListView_"

    def post(self, request, *args, **kwargs):
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
        return super(HistoriaClinicaListView, self).get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        return super(HistoriaClinicaListView, self).get(request, args, kwargs)

    def get_queryset(self):

        # Filtro estado
        filtroEstado = self.kwargs['estado'] or None
        if filtroEstado == 'deleted':
            qs = self.model.objects.filter(estado='E')
        else:
            qs = self.model.objects.filter(estado='A')

        # Filtro por campo
        stringBuscar = self.get_session('stringBuscar')
        campoBuscar = self.get_session('campoBuscar')
        dict = {
            'stringBuscar': stringBuscar or '',
            'campoBuscar': campoBuscar or '',
        }
        qdict = QueryDict('')
        qdict = qdict.copy()
        qdict.update(dict)
        form = self.form_class(qdict)

        if form.is_valid():

            if True:

                if stringBuscar and campoBuscar:

                    if campoBuscar == 'id':
                        try:
                            isinstance(int(stringBuscar), int)
                            filter_dict = {campoBuscar: stringBuscar}
                            qs = qs.filter(**filter_dict)
                        except:
                            pass

                    elif campoBuscar == 'fecha':
                        if (re.match('^\d\d/\d\d/\d\d\d\d$', stringBuscar)):
                            fecha_split = stringBuscar.split('/')
                            f_dia = int(fecha_split[0])
                            f_mes = int(fecha_split[1])
                            f_ano = int(fecha_split[2])
                            fecha = datetime.date(f_ano, f_mes, f_dia)
                            filter_dict = {campoBuscar: fecha}
                            qs = qs.filter(**filter_dict)

                    elif campoBuscar == 'doc_num':
                        try:
                            isinstance(int(stringBuscar), int)
                            filter_dict =\
                                {campoBuscar + '__contains': stringBuscar}
                            qs = self.model.objects.filter(**filter_dict)
                        except:
                            pass

                    elif campoBuscar == 'nombre':
                        filter_dict = {
                            campoBuscar + '__contains': stringBuscar
                        }
                        qs = qs.filter(**filter_dict)

                    elif campoBuscar == 'apellido':
                        filter_dict = {
                            campoBuscar + '__contains': stringBuscar
                        }
                        qs = qs.filter(**filter_dict)

                else:
                    pass

        return qs

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaListView, self).\
            get_context_data(**kwargs)

        stringBuscar = self.get_session('stringBuscar')
        campoBuscar = self.get_session('campoBuscar')
        submitBuscar = self.get_session('submitBuscar')

        if self.request.method == 'POST':
            if submitBuscar == 'Filtrar':
                dict = {
                    'stringBuscar': stringBuscar or '',
                    'campoBuscar': campoBuscar or '',
                }
                qdict = QueryDict('')
                qdict = qdict.copy()
                qdict.update(dict)
                form = self.form_class(qdict)
                context['form'] = form
            else:
                form = self.form_class(initial={
                    'stringBuscar': stringBuscar or '',
                    'campoBuscar': campoBuscar or '',
                })
                context['form'] = form

        if self.request.method == 'GET':
            if submitBuscar == 'Filtrar':
                dict = {
                    'stringBuscar': stringBuscar or '',
                    'campoBuscar': campoBuscar or '',
                }
                qdict = QueryDict('')
                qdict = qdict.copy()
                qdict.update(dict)
                form = self.form_class(qdict)
                context['form'] = form
            else:
                form = self.form_class(initial={
                    'stringBuscar': stringBuscar or '',
                    'campoBuscar': campoBuscar or '',
                })
                context['form'] = form

        # Botón Ver Eliminados/Activos
        btn_estado = {}
        filtroEstado = self.kwargs['estado'] or None
        if filtroEstado == 'deleted':
            btn_estado['class'] = 'btn-success'
            btn_estado['text'] = 'Ver Activos'
            btn_estado['url'] = 'historiaclinica_list'
            btn_estado['url_args'] = 'activos'
        else:
            btn_estado['class'] = 'btn-danger'
            btn_estado['text'] = 'Ver Eliminados'
            btn_estado['url'] = 'historiaclinica_list'
            btn_estado['url_args'] = 'deleted'
        context['btn_estado'] = btn_estado
        return context

    @method_decorator(
        permission_required(
            'pie_diabetico_app.view_historia_clinica',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaListView, self).dispatch(*args, **kwargs)


class HistoriaClinicaCreateView(PieDiabeticoTopNavBar, TitleView, CreateView):
    model = HistoriaClinica
    template_name = 'pie_diabetico_app/historiaclinica_form.html'
    form_class = HistoriaClinicaForm
    success_url = reverse_lazy(
        'historiaclinica_list', kwargs={'estado': 'activos'}
    )
    title = "Ingresar Ficha"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.estado = 'A'
        self.object.created = datetime.datetime.now()
        self.object.created_user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(
        permission_required(
            'pie_diabetico_app.create_historia_clinica',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaCreateView, self).dispatch(*args, **kwargs)


class HistoriaClinicaDeleteView(PieDiabeticoTopNavBar, TitleView, DeleteView):
    model = HistoriaClinica
    success_url = reverse_lazy(
        'historiaclinica_list', kwargs={'estado': 'activos'}
    )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 'E'
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(
        permission_required(
            'pie_diabetico_app.delete_historia_clinica',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaDeleteView, self).dispatch(*args, **kwargs)


@permission_required('pie_diabetico_app.restore_historia_clinica')
def HistoriaClinicaRestore(request, pk):
    model = HistoriaClinica
    success_url = reverse_lazy(
        'historiaclinica_list', kwargs={'estado': 'activos'}
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


class HistoriaClinicaUpdateView(PieDiabeticoTopNavBar, TitleView, UpdateView):
    model = HistoriaClinica
    template_name = 'pie_diabetico_app/historiaclinica_form.html'
    form_class = HistoriaClinicaForm
    success_url = reverse_lazy(
        'historiaclinica_list', kwargs={'estado': 'activos'}
    )
    title = "Editar Ficha"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created = datetime.datetime.now()
        self.object.created_user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class):
        form = super(HistoriaClinicaUpdateView, self).get_form(form_class)
        user = self.request.user

        uneditablefields = set(form.fields)
        if user.has_perm(
            'pie_diabetico_app.change_historia_clinica'
        ):
            uneditablefields = set()

        for f in uneditablefields:
            form.helper[f].wrap(UneditableField)

        form.uneditablefields = uneditablefields

        return form

    @method_decorator(
        permission_required(
            'pie_diabetico_app.view_historia_clinica',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaUpdateView, self).dispatch(*args, **kwargs)


@permission_required('pie_diabetico_app.view_historia_clinica')
def export_to_excel(request, pk):
    model = HistoriaClinica
    obj = get_object_or_404(model, id=pk)
    template_name = "pie_diabetico_app/historiaclinica_csv.html"
    content = [
        {
            'title': 'Datos personales',
            'fields': (
                'fecha',
                'sexo',
                'nombre',
                'apellido',
                'edad',
                'sexo',
                'nombre',
                'apellido',
                'edad',
                'historia_clinica',
                'doc_tipo',
                'doc_num',
                'domicilio'
            )
        },
        {
            'title': 'Social',
            'fields': (
                'educacion',
                'estado_soceco',
                'convive'
            )
        },
        {
            'title': 'Examen físico',
            'fields': (
                'peso',
                'talla',
                'imc',
                'diabetes',
                'edad_diag_diabetes',
                'control_glucemio',
                'estilo_vida'
            )
        },
        {
            'title': 'Antecedentes personales',
            'fields': (
                'tabaquismo',
                'alcohol',
                'hta',
                'retinopatia',
                'nefropatia',
                'dislipidemia',
                'vision_dism',
                'angioplatia',
                'bypass',
                'ulceras_previas',
                'macrovascular',
                'amputacion',
                'antecedentes_otros'
            )
        },
        {
            'title': 'Examen de pie',
            'fields': (
                'examen_pie',
                'neuropatia',
                'vasculopatia'
            )
        },
        {
            'title': 'Apariencia de pie derecho',
            'fields': (
                'pie_der_forma',
                'pie_der_almohadilla',
                'pie_der_callosidades',
                'pie_der_fisuras',
                'pie_der_infeccion',
                'pie_der_ulcera',
                'pie_der_ampollas',
                'pie_der_dedos',
            )
        },
        {
            'title': 'Apariencia de pie izquierdo',
            'fields': (
                'pie_izq_forma',
                'pie_izq_almohadilla',
                'pie_izq_callosidades',
                'pie_izq_fisuras',
                'pie_izq_infeccion',
                'pie_izq_ulcera',
                'pie_izq_ampollas',
                'pie_izq_dedos'
            )
        },
        {
            'title': 'Neuropatía motora pie derecho',
            'fields': (
                'maniobra_abanico_der',
                'extension_1dedo_der',
                'dorsiflexion_der'
            )
        },
        {
            'title': 'Neuropatía motora pie izquierdo',
            'fields': (
                'maniobra_abanico_izq',
                'extension_1dedo_izq',
                'dorsiflexion_izq'
            )
        },
        {
            'title': 'Neuropatía sensitiva pie derecho',
            'fields': (
                'termica_der',
                'dolorosa_der',
                'vibratoria_der',
                'tactil_der',
                'reflejo_rotuliano_der',
                'fuerza_muscular_der',
                'reflejo_aquilano_der'
            )
        },
        {
            'title': 'Neuropatía sensitiva pie izquierdo',
            'fields': (
                'termica_izq',
                'dolorosa_izq',
                'vibratoria_izq',
                'tactil_izq',
                'reflejo_rotuliano_izq',
                'fuerza_muscular_izq',
                'reflejo_aquilano_izq'
            )
        },
        {
            'title': 'Flujo periférico pie derecho',
            'fields': (
                'piel_der',
                'color_der',
                'vellos_der',
                'humedad_der',
                'relleno_capilar_der',
                'pulso_pedio_der',
                'pulso_tibial_post_der',
                'pulso_popliteo_der',
                'unas_der'
            )
        },
        {
            'title': 'Flujo periférico pie izquierdo',
            'fields': (
                'piel_izq',
                'color_izq',
                'vellos_izq',
                'humedad_izq',
                'relleno_capilar_izq',
                'pulso_pedio_izq',
                'pulso_tibial_post_izq',
                'pulso_popliteo_izq',
                'unas_izq',
            )
        },
        {
            'title': 'Examen dermatológico',
            'fields': (
                'hiperqueratosis',
                'intertrigo',
                'onicomicosis',
                'bacterio_germen',
                'micologico',
                'directo',
                'cultivo',
                'antibiograma',
                'biopsia',
            )
        },
        {
            'title': 'Úlceras',
            'fields': (
                'ulceras',
                'ulceras_desc',
            )
        },
        {
            'title': 'Informe',
            'fields': (
                'informe',
                'laboratorio',
                'tratamiento',
                'antibiotico',
                'curaciones'
            )
        }
    ]
    values = []
    for block in content:
        value = (block['title'], '')
        values.append(value)
        values.append(('', ''))
        for field_name in block['fields']:
            field = model._meta.get_field(field_name)
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


class HistoriaClinicaAdjuntoList(PieDiabeticoTopNavBar, TitleView, CreateView):
    model = HistoriaClinicaAdjunto
    parent_model = HistoriaClinica
    title = "Listado de Adjuntos"
    template_name = "pie_diabetico_app/historiaclinicaadjunto_list.html"
    form_class = HistoriaClinicaAdjuntoCreateForm

    def form_valid(self, form):
        if not self.request.user.has_perm(
            'pie_diabetico_app.create_historia_clinica_adjunto'
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
        self.object.historia_clinica = parent_obj
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
        queryset = self.model.objects.filter(historia_clinica=parent_obj)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaAdjuntoList, self).\
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
        success_url = reverse_lazy('historiaclinicaadjunto_list', args=[pk])
        return success_url

    @method_decorator(
        permission_required(
            'pie_diabetico_app.view_historia_clinica_adjunto',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaAdjuntoList, self).\
            dispatch(*args, **kwargs)


class HistoriaClinicaAdjuntoDeleteView(
    PieDiabeticoTopNavBar, TitleView, DeleteView
):
    model = HistoriaClinicaAdjunto
    parent_model = HistoriaClinica

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaAdjuntoDeleteView, self).\
            get_context_data(**kwargs)
        self.object = self.get_object()
        self.parent_pk = self.object.historia_clinica.id
        context['parent_pk'] = self.parent_pk
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.parent_pk = self.object.historia_clinica.id
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
            'historiaclinicaadjunto_list',
            args=[self.parent_pk]
        )
        return success_url

    @method_decorator(
        permission_required(
            'pie_diabetico_app.delete_historia_clinica_adjunto',
            raise_exception=True
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(HistoriaClinicaAdjuntoDeleteView, self).\
            dispatch(*args, **kwargs)


@permission_required(
    'pie_diabetico_app.view_historia_clinica_adjunto'
)
def HistoriaClinicaAdjuntoDownload(request, pk):
    model = HistoriaClinicaAdjunto

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
        parent_pk = obj.historia_clinica.id
        redirect_url = reverse(
            'historiaclinicaadjunto_list',
            args=[parent_pk]
        ) + '?e=1'
        return HttpResponseRedirect(redirect_url)
