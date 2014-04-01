# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import filesizeformat

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div,\
    Field, Button, Row
from crispy_forms.bootstrap import Tab, TabHolder

from core.forms import FormWithUneditableMixin

from .models import EntradaAnalisis, EntradaAnalisisAdjunto


class EntradaAnalisisForm(FormWithUneditableMixin, forms.ModelForm):
    class Meta:
        model = EntradaAnalisis
        widgets = {
            'neonatologia_obs': forms.Textarea(attrs={'rows': 4}),
            'trabsoc_obs': forms.Textarea(attrs={'rows': 4}),
            'laboratorio_obs': forms.Textarea(attrs={'rows': 4}),
            'determinaciones': forms.SelectMultiple(attrs={'size': '8'}),
        }
        fields = (
            # Neonatología
            'fecha',
            'prioridad',
            'sexo',
            'apellido',
            'nombre',
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
            'neonatologia_obs',
            'notificar_trabsoc',
            # Trabajo social
            'fecha_notif_familia',
            'trabsoc_obs',
            # Laboratorio
            'muestra_num_2',
            'muestra_fecha_2',
            'muestra_texto_2',
            'laboratorio_obs'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Neonatología',
                    Row(
                        Div('fecha', css_class='col-sm-6'),
                        Div('prioridad', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('apellido', css_class='col-sm-6'),
                        Div('nombre', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('sexo', css_class='col-sm-6'),
                        Div('fecha_nacimiento', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('apellido_madre', css_class='col-sm-6'),
                        Div('nombre_madre', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('doc_tipo_madre', css_class='col-sm-6'),
                        Div('doc_num_madre', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('domicilio', css_class='col-sm-6'),
                        Div('telefono', css_class='col-sm-6'),
                    ),
                    Row(
                        Div(
                            'determinaciones',
                            css_class='col-sm-6',
                        ),
                        Div(
                            'muestra_fecha_1',
                            'muestra_num_1',
                            css_class='col-sm-6',
                        ),
                    ),
                    Row(
                        Div(
                            'notificar_trabsoc',
                            css_class='col-sm-6',
                        ),
                        Div(
                            'neonatologia_obs',
                            css_class='col-sm-6',
                        ),
                    ),
                ),
                Tab(
                    'Trabajo Social',
                    Row(
                        Div('fecha_notif_familia', css_class='col-sm-6'),
                        Div('trabsoc_obs', css_class='col-sm-6'),
                    ),
                ),
                Tab(
                    'Laboratorio',
                    Row(
                        Div('muestra_num_2', css_class='col-sm-6'),
                        Div('muestra_fecha_2', css_class='col-sm-6'),
                    ),
                    Row(
                        Div('muestra_texto_2', css_class='col-sm-6'),
                        Div('laboratorio_obs', css_class='col-sm-6'),
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Aceptar', css_class='btn-primary'),
                Button(
                    'cancel', 'Cancelar', css_class='btn-default',
                    onclick='window.location.href="{}"'.format(
                        reverse_lazy(
                            'entradaanalisis_list',
                            kwargs={'estado': 'todos'}
                        )
                    )
                )
            )
        )
        super(EntradaAnalisisForm, self).__init__(*args, **kwargs)


class EntradaAnalisisFechaIrForm(forms.Form):

    fechaIr = forms.CharField(
        max_length=254,
        required=True,
    )
    fechaIr.error_messages['required'] = ''
    fechaIr.error_messages['invalid'] = ''

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('fechaIr'),
                Submit('submitIr', 'Ir', css_class='btn-primary'),
            ),
        )
        super(EntradaAnalisisFechaIrForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(EntradaAnalisisFechaIrForm, self).is_valid()

    def clean(self):
        cleaned_data = super(EntradaAnalisisFechaIrForm, self).clean()
        fechaIr = cleaned_data.get("fechaIr", None)
        if fechaIr:
            if not (re.match('^\d\d/\d\d\d\d$', fechaIr)):
                self._errors["fechaIr"] = self.error_class([""])
                del cleaned_data["fechaIr"]
        return cleaned_data


class EntradaAnalisisBuscarForm(forms.Form):

    stringBuscar = forms.CharField(
        max_length=254,
        required=True,
    )
    stringBuscar.error_messages['required'] = ''
    stringBuscar.error_messages['invalid'] = ''

    campoBuscar = forms.TypedChoiceField(
        choices=(
            ('id', 'ID'),
            ('fecha', 'Fecha'),
            ('apellido', 'Apellido'),
            ('nombre', 'Nombre'),
            ('fecha_nacimiento', 'Fecha nac.'),
            ('apellido_madre', 'Madre Ape.'),
            ('nombre_madre', 'Madre Nom.'),
            ('determinaciones', 'Det. a rep.'),
            ('muestra_fecha_1', 'Fecha 1º muestra'),
            ('notificar_trabsoc', 'Notif. Trab. Soc.'),
            ('fecha_notif_familia', 'Fecha notif. flia.'),
            ('muestra_fecha_2', 'Fecha muestra rep.')
        ),
        widget=forms.Select,
        initial='0',
        required=True,
    )
    campoBuscar.error_messages['required'] = ''
    campoBuscar.error_messages['invalid_choice'] = ''

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('stringBuscar'),
                Field('campoBuscar'),
                Submit('submitBuscar', 'Filtrar', css_class='btn-primary'),
                Submit('submitBuscar', 'Reiniciar', css_class='btn-default'),
            ),
        )
        super(EntradaAnalisisBuscarForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(EntradaAnalisisBuscarForm, self).is_valid()

    def clean(self):
        cleaned_data = super(EntradaAnalisisBuscarForm, self).clean()
        stringBuscar = cleaned_data.get("stringBuscar", None)
        campoBuscar = cleaned_data.get("campoBuscar", None)
        if stringBuscar and campoBuscar:
            if campoBuscar == 'id':
                try:
                    isinstance(int(stringBuscar), int)
                except:
                    self._errors["stringBuscar"] = self.error_class([""])
                    del cleaned_data["stringBuscar"]
            elif campoBuscar in [
                'fecha', 'fecha_nacimiento', 'muestra_fecha_1',
                'muestra_fecha_2', 'fecha_notif_familia'
            ]:
                if not (re.match('^\d\d/\d\d/\d\d\d\d$', stringBuscar)):
                    self._errors["stringBuscar"] = self.error_class([""])
                    del cleaned_data["stringBuscar"]
            elif campoBuscar in [
                'apellido', 'nombre', 'apellido_madre',
                'nombre_madre', 'notificar_trabsoc', 'determinaciones'
            ]:
                pass
        return cleaned_data


class EntradaAnalisisAdjuntoCreateForm(forms.ModelForm):

    MAX_ADJUNTO_SIZE = 1024 * 1024 * 10  # Tamaño máximo permitido en bytes

    class Meta:
        model = EntradaAnalisisAdjunto
        widgets = {}
        fields = (
            'adjunto',
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Fieldset(
                '',
                'adjunto',
                css_class="text-left"
            ),
            ButtonHolder(
                Submit('submit', 'Agregar', css_class='btn-primary'),
            )
        )
        super(EntradaAnalisisAdjuntoCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EntradaAnalisisAdjuntoCreateForm, self).clean()
        adjunto = cleaned_data.get("adjunto", None)
        if adjunto:
            adjunto_size = adjunto._get_size()
            if adjunto_size > self.MAX_ADJUNTO_SIZE:
                self._errors["adjunto"] = self.error_class(
                    [
                        "El archivo supera el tamaño máximo de " +
                        str(filesizeformat(self.MAX_ADJUNTO_SIZE)) + "."
                    ]
                )
                del cleaned_data["adjunto"]
        return cleaned_data
