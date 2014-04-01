# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import filesizeformat

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div,\
    Field, Row, Button, HTML
from crispy_forms.bootstrap import Tab, TabHolder

from core.forms import FormWithUneditableMixin

from .models import HistoriaClinica, HistoriaClinicaAdjunto
from .extras.constants import ulceras_modal_html


class HistoriaClinicaForm(FormWithUneditableMixin, forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        widgets = {
            'amputacion': forms.Textarea(attrs={'rows': 2}),
            'antecedentes_otros': forms.Textarea(attrs={'rows': 2}),
            'derm_observaciones': forms.Textarea(attrs={'rows': 2}),
            'ulceras_desc': forms.Textarea(attrs={'rows': 4}),
            'informe': forms.Textarea(attrs={'rows': 4}),
            'laboratorio': forms.Textarea(attrs={'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'rows': 2}),
            'antibiotico': forms.Textarea(attrs={'rows': 2}),
            'curaciones': forms.Textarea(attrs={'rows': 2}),
        }
        fields = (
            # Datos personales
            'fecha',
            'sexo',
            'nombre',
            'apellido',
            'edad',
            'historia_clinica',
            'doc_tipo',
            'doc_num',
            'domicilio',
            'educacion',
            'estado_soceco',
            'convive',
            # Examen físico
            'peso',
            'talla',
            'imc',
            'diabetes',
            'edad_diag_diabetes',
            'control_glucemio',
            'estilo_vida',
            # Antecedentes personales
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
            'antecedentes_otros',
            # Examen de pie
            'examen_pie',
            'neuropatia',
            'vasculopatia',
            # Apariencia de pie
            'pie_der_forma',
            'pie_der_almohadilla',
            'pie_der_callosidades',
            'pie_der_fisuras',
            'pie_der_infeccion',
            'pie_der_ulcera',
            'pie_der_ampollas',
            'pie_der_dedos',
            'pie_izq_forma',
            'pie_izq_almohadilla',
            'pie_izq_callosidades',
            'pie_izq_fisuras',
            'pie_izq_infeccion',
            'pie_izq_ulcera',
            'pie_izq_ampollas',
            'pie_izq_dedos',
            # Neuropatía motora
            'maniobra_abanico_der',
            'extension_1dedo_der',
            'dorsiflexion_der',
            'maniobra_abanico_izq',
            'extension_1dedo_izq',
            'dorsiflexion_izq',
            # Neuropatía sensitiva
            'termica_der',
            'dolorosa_der',
            'vibratoria_der',
            'tactil_der',
            'reflejo_rotuliano_der',
            'fuerza_muscular_der',
            'reflejo_aquilano_der',
            'termica_izq',
            'dolorosa_izq',
            'vibratoria_izq',
            'tactil_izq',
            'reflejo_rotuliano_izq',
            'fuerza_muscular_izq',
            'reflejo_aquilano_izq',
            # Flujo periférico
            'piel_der',
            'color_der',
            'vellos_der',
            'humedad_der',
            'relleno_capilar_der',
            'pulso_pedio_der',
            'pulso_tibial_post_der',
            'pulso_popliteo_der',
            'unas_der',
            'piel_izq',
            'color_izq',
            'vellos_izq',
            'humedad_izq',
            'relleno_capilar_izq',
            'pulso_pedio_izq',
            'pulso_tibial_post_izq',
            'pulso_popliteo_izq',
            'unas_izq',
            # Examen dermatológico
            'hiperqueratosis',
            'intertrigo',
            'onicomicosis',
            'bacterio_germen',
            'micologico',
            'directo',
            'cultivo',
            'antibiograma',
            'biopsia',
            'derm_observaciones',
            # Úlceras
            'ulceras',
            'ulceras_desc',
            # Informe
            'informe',
            'laboratorio',
            'tratamiento',
            'antibiotico',
            'curaciones'
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
                    'Personal',
                    Fieldset(
                        '',
                        'fecha',
                        'sexo',
                        'nombre',
                        'apellido',
                        'edad',
                        'historia_clinica',
                        Row(
                            Div(
                                'doc_tipo',
                                css_class="col-sm-3 col-sm-offset-3"
                            ),
                            Div('doc_num', css_class="col-sm-6")
                        ),
                        'domicilio',
                    ),
                ),
                Tab(
                    'Social',
                    Fieldset(
                        '',
                        'educacion',
                        'estado_soceco',
                        'convive',
                    ),
                ),
                Tab(
                    'Examen físico',
                    Fieldset(
                        '',
                        'peso',
                        'talla',
                        'imc',
                        'diabetes',
                        'edad_diag_diabetes',
                        'control_glucemio',
                        'estilo_vida',
                    ),
                ),
                Tab(
                    'Antecedentes',
                    Fieldset(
                        '',
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
                        'antecedentes_otros',
                    ),
                ),
                Tab(
                    'Examen pie',
                    Fieldset(
                        '',
                        'examen_pie',
                        'neuropatia',
                        'vasculopatia',
                    ),
                ),
                Tab(
                    'Apariencia pie',
                    Fieldset(
                        'Pie derecho',
                        'pie_der_forma',
                        'pie_der_almohadilla',
                        'pie_der_callosidades',
                        'pie_der_fisuras',
                        'pie_der_infeccion',
                        'pie_der_ulcera',
                        'pie_der_ampollas',
                        'pie_der_dedos',
                        css_class="col-sm-6",
                    ),
                    Fieldset(
                        'Pie izquierdo',
                        'pie_izq_forma',
                        'pie_izq_almohadilla',
                        'pie_izq_callosidades',
                        'pie_izq_fisuras',
                        'pie_izq_infeccion',
                        'pie_izq_ulcera',
                        'pie_izq_ampollas',
                        'pie_izq_dedos',
                        css_class="col-sm-6",
                    ),
                ),
                Tab(
                    'Neuropatía motora',
                    Fieldset(
                        'Pie derecho',
                        'maniobra_abanico_der',
                        'extension_1dedo_der',
                        'dorsiflexion_der',
                        css_class="col-sm-6",
                    ),
                    Fieldset(
                        'Pie izquierdo',
                        'maniobra_abanico_izq',
                        'extension_1dedo_izq',
                        'dorsiflexion_izq',
                        css_class="col-sm-6",
                    ),
                ),
                Tab(
                    'Neuropatía sensitiva',
                    Fieldset(
                        'Pie derecho',
                        'termica_der',
                        'dolorosa_der',
                        'vibratoria_der',
                        'tactil_der',
                        'reflejo_rotuliano_der',
                        'fuerza_muscular_der',
                        'reflejo_aquilano_der',
                        css_class="col-sm-6",
                    ),
                    Fieldset(
                        'Pie izquierdo',
                        'termica_izq',
                        'dolorosa_izq',
                        'vibratoria_izq',
                        'tactil_izq',
                        'reflejo_rotuliano_izq',
                        'fuerza_muscular_izq',
                        'reflejo_aquilano_izq',
                        css_class="col-sm-6",
                    ),
                ),
                Tab(
                    'Flujo periférico',
                    Fieldset(
                        'Pie derecho',
                        'piel_der',
                        'color_der',
                        'vellos_der',
                        'humedad_der',
                        'relleno_capilar_der',
                        'pulso_pedio_der',
                        'pulso_tibial_post_der',
                        'pulso_popliteo_der',
                        'unas_der',
                        css_class="col-sm-6",
                    ),
                    Fieldset(
                        'Pie izquierdo',
                        'piel_izq',
                        'color_izq',
                        'vellos_izq',
                        'humedad_izq',
                        'relleno_capilar_izq',
                        'pulso_pedio_izq',
                        'pulso_tibial_post_izq',
                        'pulso_popliteo_izq',
                        'unas_izq',
                        css_class="col-sm-6",
                    ),
                ),
                Tab(
                    'Dermatológico',
                    Fieldset(
                        '',
                        'hiperqueratosis',
                        'intertrigo',
                        'onicomicosis',
                        'bacterio_germen',
                        'micologico',
                        'directo',
                        'cultivo',
                        'antibiograma',
                        'biopsia',
                        'derm_observaciones',
                    ),
                ),
                Tab(
                    'Úlceras',
                    Fieldset(
                        '',
                        Row(
                            Div(
                                'ulceras',
                                css_class="col-sm-9 col-sm-offset-1"
                            ),
                            Div(
                                HTML(
                                    ulceras_modal_html
                                ), css_class="col-sm-2"
                            )
                        ),
                        'ulceras_desc',
                    ),
                ),
                Tab(
                    'Informe',
                    Fieldset(
                        '',
                        'informe',
                        'laboratorio',
                        'tratamiento',
                        'antibiotico',
                        'curaciones'
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Aceptar', css_class='btn-primary'),
                Button(
                    'cancel', 'Cancelar', css_class='btn-default',
                    onclick='window.location.href="{}"'.format(
                        reverse_lazy(
                            'historiaclinica_list',
                            kwargs={
                                'estado': 'activos',
                            }
                        )
                    )
                )
            )
        )
        super(HistoriaClinicaForm, self).__init__(*args, **kwargs)


class HistoriaClinicaBuscarForm(forms.Form):

    stringBuscar = forms.CharField(
        max_length=254,
        required=True,
    )
    stringBuscar.error_messages['required'] = ''
    stringBuscar.error_messages['invalid'] = ''

    campoBuscar = forms.TypedChoiceField(
        choices=(
            ('id', 'ID'), ('fecha', 'Fecha'), ('doc_num', 'Doc. Num.'),
            ('nombre', 'Nombre'), ('apellido', 'Apellido')
        ),
        widget=forms.Select,
        initial='0',
        required=True,
    )
    campoBuscar.error_messages['required'] = ''
    campoBuscar.error_messages['invalid'] = ''

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
                css_class="text-right",
            )
        )
        super(HistoriaClinicaBuscarForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(HistoriaClinicaBuscarForm, self).is_valid()

    def clean(self):
        cleaned_data = super(HistoriaClinicaBuscarForm, self).clean()
        stringBuscar = cleaned_data.get("stringBuscar", None)
        campoBuscar = cleaned_data.get("campoBuscar", None)
        if stringBuscar and campoBuscar:
            if campoBuscar in ['id', 'doc_num']:
                try:
                    isinstance(int(stringBuscar), int)
                except:
                    self._errors["stringBuscar"] = self.error_class([""])
                    del cleaned_data["stringBuscar"]
            if campoBuscar == 'fecha':
                if not (re.match('^\d\d/\d\d/\d\d\d\d$', stringBuscar)):
                    self._errors["stringBuscar"] = self.error_class([""])
                    del cleaned_data["stringBuscar"]
            if campoBuscar in ['nombre', 'apellido']:
                pass
        return cleaned_data


class HistoriaClinicaAdjuntoCreateForm(forms.ModelForm):

    MAX_ADJUNTO_SIZE = 1024 * 1024 * 10  # Tamaño máximo permitido en bytes

    class Meta:
        model = HistoriaClinicaAdjunto
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
        super(HistoriaClinicaAdjuntoCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(HistoriaClinicaAdjuntoCreateForm, self).clean()
        adjunto = cleaned_data.get("adjunto", None)
        if adjunto:
            adjunto_size = adjunto._get_size()
            if adjunto_size > self.MAX_ADJUNTO_SIZE:
                self._errors["adjunto"] = self.error_class(
                    ["El archivo supera el tamaño máximo de " +
                     str(filesizeformat(self.MAX_ADJUNTO_SIZE)) + "."]
                )
                del cleaned_data["adjunto"]
        return cleaned_data
