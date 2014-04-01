# -*- coding: utf-8 -*-

import datetime
import os.path

from django.db import models
from django.core.exceptions import ValidationError

from core.models import TimeStampedModel


class HistoriaClinica(TimeStampedModel):

    # Validators
    def validate_doc_num(value):
        if len(str(value)) < 7:
            raise ValidationError('Debe tener al menos 7 dígitos.')

    def validate_edad(value):
        if len(str(value)) > 3:
            raise ValidationError('Debe tener menos de 4 dígitos.')

    # Meta Datos
    ESTADO_CHOICES = (
        ('A', 'Activo'),
        ('E', 'Eliminado'),
    )
    estado = models.CharField(max_length=1,
                              choices=ESTADO_CHOICES,
                              default='A')
    # Datos personales
    fecha = models.DateField(default=datetime.date.today)
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    sexo = models.CharField(max_length=1,
                            choices=SEXO_CHOICES,
                            blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField(null=True, validators=[validate_edad])
    historia_clinica = models.IntegerField(null=True, blank=True)
    TIPO_DOCS_CHOICES = (
        ('DNI', 'DNI'),
        ('LE', 'LE'),
        ('LC', 'LC'),
        ('CI', 'CI'),
    )
    doc_tipo = models.CharField(max_length=3,
                                choices=TIPO_DOCS_CHOICES,
                                default='DNI',
                                verbose_name="doc. tipo")
    doc_num = models.IntegerField(
        verbose_name="doc. número",
        validators=[validate_doc_num]
    )
    domicilio = models.CharField(max_length=100, blank=True)

    # Social
    EDUCACION_CHOICES = (
        ('ANA', 'Analfabeto'),
        ('PRI', 'Primaria'),
        ('SEC', 'Secundaria'),
        ('TER', 'Terciaria'),
        ('UNI', 'Universitaria'),
    )
    educacion = models.CharField(max_length=3,
                                 choices=EDUCACION_CHOICES,
                                 blank=True,
                                 verbose_name="educación")
    ESTADO_SOCECO_CHOICES = (
        ('BAJ', 'Bajo'),
        ('MED', 'Medio'),
        ('ALT', 'Alto'),
    )
    estado_soceco = models.CharField(max_length=3,
                                     choices=ESTADO_SOCECO_CHOICES,
                                     blank=True,
                                     verbose_name="estado socio-económico")
    CONVIVE_CHOICES = (
        ('SOL', 'Solo'),
        ('CON', 'Cónyuge'),
        ('FAM', 'Familia'),
        ('OTR', 'Otro'),
    )
    convive = models.CharField(max_length=3,
                               choices=CONVIVE_CHOICES,
                               blank=True)

    # Examen físico
    peso = models.IntegerField(blank=True, null=True)
    talla = models.IntegerField(blank=True, null=True)
    imc = models.IntegerField(blank=True, null=True, verbose_name="IMC")
    DIABETES_CHOICES = (
        ('1', 'I'),
        ('2', 'II'),
        ('2IR', 'II I.R.'),
        ('GES', 'Gestacional'),
    )
    diabetes = models.CharField(max_length=3,
                                choices=DIABETES_CHOICES,
                                blank=True,
                                verbose_name="diabetes tipo")
    edad_diag_diabetes = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="edad diagnóstico diabetes"
    )
    CONTROL_GLUCEMIO_CHOICES = (
        ('MAL', 'Malo'),
        ('REG', 'Regular'),
        ('ACE', 'Aceptable'),
        ('BUE', 'Bueno'),
    )
    control_glucemio = models.CharField(max_length=3,
                                        choices=CONTROL_GLUCEMIO_CHOICES,
                                        blank=True)
    ESTILO_VIDA_CHOICES = (
        ('NAD', 'Nada'),
        ('DIE', 'Dieta solo'),
        ('EJE', 'Ejercicio solo'),
        ('DYE', 'Dieta y ejercicio'),
    )
    estilo_vida = models.CharField(max_length=3,
                                   choices=ESTILO_VIDA_CHOICES,
                                   blank=True,
                                   verbose_name="estilo de vida")

    # Antecedentes personales
    SINO_CHOICES = (
        ('SI', 'Sí'),
        ('NO', 'No'),
    )
    TABAQUISMO_CHOICES = (
        ('SI', 'Sí'),
        ('NO', 'No'),
        ('EX', 'Ex'),
    )
    tabaquismo = models.CharField(max_length=2,
                                  choices=TABAQUISMO_CHOICES,
                                  blank=True)
    ALCOHOL_CHOICES = (
        ('SI', 'Sí'),
        ('NO', 'No'),
        ('EX', 'Ex'),
    )
    alcohol = models.CharField(max_length=2,
                               choices=ALCOHOL_CHOICES,
                               blank=True)
    hta = models.CharField(max_length=2,
                           choices=SINO_CHOICES,
                           blank=True)
    retinopatia = models.CharField(max_length=2,
                                   choices=SINO_CHOICES,
                                   blank=True,
                                   verbose_name="retinopatía")
    nefropatia = models.CharField(max_length=2,
                                  choices=SINO_CHOICES,
                                  blank=True,
                                  verbose_name="nefropatía")
    dislipidemia = models.CharField(max_length=2,
                                    choices=SINO_CHOICES,
                                    blank=True)
    vision_dism = models.CharField(max_length=2,
                                   choices=SINO_CHOICES,
                                   blank=True,
                                   verbose_name="disminución de visión")
    angioplatia = models.CharField(max_length=2,
                                   choices=SINO_CHOICES,
                                   blank=True,
                                   verbose_name="angioplatía")
    bypass = models.CharField(max_length=2,
                              choices=SINO_CHOICES,
                              blank=True)
    ulceras_previas = models.CharField(max_length=2,
                                       choices=SINO_CHOICES,
                                       blank=True,
                                       verbose_name="úlceras previas")
    macrovascular = models.CharField(max_length=2,
                                     choices=SINO_CHOICES,
                                     blank=True,
                                     verbose_name="enfermedad macrovascular")
    amputacion = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="amputación"
    )
    antecedentes_otros = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="otros antecedentes"
    )

    # Examen de pie
    examen_pie = models.CharField(max_length=2,
                                  choices=SINO_CHOICES,
                                  blank=True,
                                  verbose_name="examen de pie (último año)")
    neuropatia = models.CharField(max_length=2,
                                  choices=SINO_CHOICES,
                                  blank=True,
                                  verbose_name="síntoma de neuropatía")
    vasculopatia = models.CharField(max_length=2,
                                    choices=SINO_CHOICES,
                                    blank=True,
                                    verbose_name="síntoma de vasculopatía")
    # Apariencia de pie
    PIE_FORMA_CHOICES = (
        ('NOR', 'Normal'),
        ('DEF', 'Deformado'),
    )
    pie_der_forma = models.CharField(max_length=3,
                                     choices=PIE_FORMA_CHOICES,
                                     blank=True,
                                     verbose_name="forma")
    ALMOHADILLA_CHOICES = (
        ('CON', 'Conservada'),
        ('ALT', 'Alterada'),
    )
    pie_der_almohadilla = models.CharField(max_length=3,
                                           choices=ALMOHADILLA_CHOICES,
                                           blank=True,
                                           verbose_name="almohadilla plantar")
    pie_der_callosidades = models.CharField(max_length=2,
                                            choices=SINO_CHOICES,
                                            blank=True,
                                            verbose_name="callosidades")
    pie_der_fisuras = models.CharField(max_length=2,
                                       choices=SINO_CHOICES,
                                       blank=True,
                                       verbose_name="fisuras")
    pie_der_infeccion = models.CharField(max_length=2,
                                         choices=SINO_CHOICES,
                                         blank=True,
                                         verbose_name="infección")
    pie_der_ulcera = models.CharField(max_length=2,
                                      choices=SINO_CHOICES,
                                      blank=True,
                                      verbose_name="úlcera")
    pie_der_ampollas = models.CharField(max_length=2,
                                        choices=SINO_CHOICES,
                                        blank=True,
                                        verbose_name="ampollas")
    DEDOS_CHOICES = (
        ('NOR', 'Normales'),
        ('MAR', 'Martillo'),
        ('ACA', 'Acabalgados'),
        ('RIG', 'Garra rígida'),
        ('FLA', 'Garra flácida'),
    )
    pie_der_dedos = models.CharField(max_length=3,
                                     choices=DEDOS_CHOICES,
                                     blank=True,
                                     verbose_name="dedos")
    pie_izq_forma = models.CharField(max_length=3,
                                     choices=PIE_FORMA_CHOICES,
                                     blank=True,
                                     verbose_name="forma")
    pie_izq_almohadilla = models.CharField(max_length=3,
                                           choices=ALMOHADILLA_CHOICES,
                                           blank=True,
                                           verbose_name="almohadilla plantar")
    pie_izq_callosidades = models.CharField(max_length=2,
                                            choices=SINO_CHOICES,
                                            blank=True,
                                            verbose_name="callosidades")
    pie_izq_fisuras = models.CharField(max_length=2,
                                       choices=SINO_CHOICES,
                                       blank=True,
                                       verbose_name="fisuras")
    pie_izq_infeccion = models.CharField(max_length=2,
                                         choices=SINO_CHOICES,
                                         blank=True,
                                         verbose_name="infección")
    pie_izq_ulcera = models.CharField(max_length=2,
                                      choices=SINO_CHOICES,
                                      blank=True,
                                      verbose_name="úlcera")
    pie_izq_ampollas = models.CharField(max_length=2,
                                        choices=SINO_CHOICES,
                                        blank=True,
                                        verbose_name="ampollas")
    pie_izq_dedos = models.CharField(max_length=3,
                                     choices=DEDOS_CHOICES,
                                     blank=True,
                                     verbose_name="dedos")

    # Neuropatía motora
    MASMENOS_CHOICES = (
        ('MAS', 'Más'),
        ('MEN', 'Menos'),
    )
    POSNEG_CHOICES = (
        ('POS', 'Positivo'),
        ('NEG', 'Negativo'),
    )
    maniobra_abanico_der = models.CharField(max_length=3,
                                            choices=POSNEG_CHOICES,
                                            blank=True,
                                            verbose_name="maniobra abanico")
    extension_1dedo_der = models.CharField(max_length=3,
                                           choices=POSNEG_CHOICES,
                                           blank=True,
                                           verbose_name="extensión 1º dedo")
    dorsiflexion_der = models.CharField(max_length=3,
                                        choices=POSNEG_CHOICES,
                                        blank=True,
                                        verbose_name="dorsiflexión de pie")
    maniobra_abanico_izq = models.CharField(
        max_length=3,
        choices=POSNEG_CHOICES,
        blank=True,
        verbose_name="maniobra abanico"
    )
    extension_1dedo_izq = models.CharField(max_length=3,
                                           choices=POSNEG_CHOICES,
                                           blank=True,
                                           verbose_name="extensión 1º dedo")
    dorsiflexion_izq = models.CharField(max_length=3,
                                        choices=POSNEG_CHOICES,
                                        blank=True,
                                        verbose_name="dorsiflexión de pie")

    # Neuropatía sensitiva
    TERMICA_CHOICES = (
        ('NOR', 'Normal'),
        ('ALT', 'Alterada'),
    )
    termica_der = models.CharField(max_length=3,
                                   choices=TERMICA_CHOICES,
                                   blank=True,
                                   verbose_name="térmica")
    PREAUS_CHOICES = (
        ('PRE', 'Presente'),
        ('AUS', 'Ausente'),
    )
    dolorosa_der = models.CharField(max_length=3,
                                    choices=PREAUS_CHOICES,
                                    blank=True,
                                    verbose_name="dolorosa")
    VIBRATORIA_CHOICES = (
        ('NOR', 'Normal (<15º)'),
        ('DIS', 'Disminuida (15º-20º)'),
        ('AUS', 'Ausente (>20º)'),
    )
    vibratoria_der = models.CharField(max_length=3,
                                      choices=VIBRATORIA_CHOICES,
                                      blank=True,
                                      verbose_name="vibratoria")
    TACTIL_CHOICES = (
        ('NOR', 'Normal (>3)'),
        ('DIS', 'Disminuida (1-2)'),
        ('AUS', 'Ausente (No percibe)'),
    )
    tactil_der = models.CharField(max_length=3,
                                  choices=TACTIL_CHOICES,
                                  blank=True,
                                  verbose_name="táctil (monofilamento)")
    REFLEJO_ROTULIANO_CHOICES = (
        ('PRE', 'Presente'),
        ('PCR', 'Presente con refuerzos'),
        ('AUS', 'Ausente'),
    )
    reflejo_rotuliano_der = models.CharField(
        max_length=3,
        choices=REFLEJO_ROTULIANO_CHOICES,
        blank=True,
        verbose_name="reflejo rotuliano"
    )
    FUERZA_MUSCULAR_CHOICES = (
        ('MAS', 'Más'),
        ('ALT', 'Alterada'),
    )
    fuerza_muscular_der = models.CharField(
        max_length=3,
        choices=FUERZA_MUSCULAR_CHOICES,
        blank=True,
        verbose_name="fuerza muscular"
    )
    reflejo_aquilano_der = models.CharField(
        max_length=3,
        choices=PREAUS_CHOICES,
        blank=True,
        verbose_name="reflejo aquilano"
    )
    termica_izq = models.CharField(max_length=3,
                                   choices=TERMICA_CHOICES,
                                   blank=True,
                                   verbose_name="térmica")
    dolorosa_izq = models.CharField(max_length=3,
                                    choices=PREAUS_CHOICES,
                                    blank=True,
                                    verbose_name="dolorosa")
    vibratoria_izq = models.CharField(max_length=3,
                                      choices=VIBRATORIA_CHOICES,
                                      blank=True,
                                      verbose_name="vibratoria")
    tactil_izq = models.CharField(max_length=3,
                                  choices=TACTIL_CHOICES,
                                  blank=True,
                                  verbose_name="táctil (monofilamento)")
    reflejo_rotuliano_izq = models.CharField(
        max_length=3,
        choices=REFLEJO_ROTULIANO_CHOICES,
        blank=True,
        verbose_name="reflejo rotuliano"
    )
    fuerza_muscular_izq = models.CharField(
        max_length=3,
        choices=FUERZA_MUSCULAR_CHOICES,
        blank=True,
        verbose_name="fuerza muscular"
    )
    reflejo_aquilano_izq = models.CharField(
        max_length=3,
        choices=PREAUS_CHOICES,
        blank=True,
        verbose_name="reflejo aquilano"
    )

    # Flujo periférico
    PIEL_CHOICES = (
        ('NOR', 'Normal'),
        ('ATR', 'Atrófica'),
        ('REL', 'Reluciente'),
    )
    piel_der = models.CharField(max_length=3,
                                choices=PIEL_CHOICES,
                                blank=True,
                                verbose_name="piel")
    COLOR_CHOICES = (
        ('NOR', 'Normal'),
        ('PAL', 'Pálido'),
        ('ERI', 'Eritrocianosis'),
    )
    color_der = models.CharField(max_length=3,
                                 choices=COLOR_CHOICES,
                                 blank=True,
                                 verbose_name="color")
    vellos_der = models.CharField(max_length=2,
                                  choices=SINO_CHOICES,
                                  blank=True,
                                  verbose_name="vellos (en dedos)")
    HUMEDAD_CHOICES = (
        ('NOR', 'Normal'),
        ('SEC', 'Seco'),
    )
    humedad_der = models.CharField(max_length=3,
                                   choices=HUMEDAD_CHOICES,
                                   blank=True,
                                   verbose_name="humedad")
    RELLENO_CAPILAR_CHOICES = (
        ('NOR', 'Normal (<2´´)'),
        ('ALT', 'Alterado (<4´´)'),
    )
    relleno_capilar_der = models.CharField(max_length=3,
                                           choices=RELLENO_CAPILAR_CHOICES,
                                           blank=True,
                                           verbose_name="relleno capilar")
    pulso_pedio_der = models.CharField(max_length=3,
                                       choices=PREAUS_CHOICES,
                                       blank=True,
                                       verbose_name="pulso pedio")
    pulso_tibial_post_der = models.CharField(
        max_length=3,
        choices=PREAUS_CHOICES,
        blank=True,
        verbose_name="pulso tibial posterior"
    )
    pulso_popliteo_der = models.CharField(max_length=3,
                                          choices=PREAUS_CHOICES,
                                          blank=True,
                                          verbose_name="pulso popiteo")
    UNAS_CHOICES = (
        ('NOR', 'Normal'),
        ('ALT', 'Alterada'),
    )
    unas_der = models.CharField(max_length=3,
                                choices=UNAS_CHOICES,
                                blank=True,
                                verbose_name="uñas")
    piel_izq = models.CharField(max_length=3,
                                choices=PIEL_CHOICES,
                                blank=True,
                                verbose_name="piel")
    color_izq = models.CharField(max_length=3,
                                 choices=COLOR_CHOICES,
                                 blank=True,
                                 verbose_name="color")
    vellos_izq = models.CharField(max_length=2,
                                  choices=SINO_CHOICES,
                                  blank=True,
                                  verbose_name="vellos (en dedos)")
    humedad_izq = models.CharField(max_length=3,
                                   choices=HUMEDAD_CHOICES,
                                   blank=True,
                                   verbose_name="humedad")
    relleno_capilar_izq = models.CharField(max_length=3,
                                           choices=RELLENO_CAPILAR_CHOICES,
                                           blank=True,
                                           verbose_name="relleno capilar")
    pulso_pedio_izq = models.CharField(max_length=3,
                                       choices=PREAUS_CHOICES,
                                       blank=True,
                                       verbose_name="pulso pedio")
    pulso_tibial_post_izq = models.CharField(
        max_length=3,
        choices=PREAUS_CHOICES,
        blank=True,
        verbose_name="pulso tibial posterior"
    )
    pulso_popliteo_izq = models.CharField(max_length=3,
                                          choices=PREAUS_CHOICES,
                                          blank=True,
                                          verbose_name="pulso popliteo")
    unas_izq = models.CharField(max_length=3,
                                choices=UNAS_CHOICES,
                                blank=True,
                                verbose_name="uñas")

    # Examen dermatológico
    hiperqueratosis = models.CharField(max_length=500, blank=True)
    intertrigo = models.CharField(max_length=500, blank=True)
    onicomicosis = models.CharField(max_length=500, blank=True)
    bacterio_germen = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="examen bacteriológico germen"
    )
    micologico = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="micológico"
    )
    directo = models.CharField(max_length=500, blank=True)
    cultivo = models.CharField(max_length=500, blank=True)
    antibiograma = models.CharField(max_length=500, blank=True)
    biopsia = models.CharField(max_length=2,
                               choices=SINO_CHOICES,
                               blank=True)
    derm_observaciones = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="observaciones"
    )

    # Úlceras
    ULCERAS_CHOICES = (
        ('G0', 'Grado 0'),
        ('G1', 'Grado 1'),
        ('G2', 'Grado 2'),
        ('G3', 'Grado 3'),
        ('G4', 'Grado 4'),
        ('G5', 'Grado 5'),
    )
    ulceras = models.CharField(max_length=2,
                               choices=ULCERAS_CHOICES,
                               blank=True,
                               verbose_name="úlceras")
    ulceras_desc = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="descripción"
    )

    # Informe
    informe = models.CharField(max_length=500, blank=True)
    laboratorio = models.CharField(max_length=500, blank=True)
    tratamiento = models.CharField(max_length=500, blank=True)
    antibiotico = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="antibiótico"
    )
    curaciones = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = ("fecha", "doc_num", "doc_tipo")
        permissions = (
            ("view_historia_clinica", "Ver"),
            ("create_historia_clinica", "Crear"),
            ("change_historia_clinica", "Modificar"),
            ("delete_historia_clinica", "Borrar"),
            ("restore_historia_clinica", "Restaurar")
        )

    def __str__(self):
        return self.fecha.strftime('%d/%m/%Y') +\
            ' ' + self.doc_tipo + ' ' + str(self.doc_num)

    def fecha_format(self):
        return self.fecha.strftime('%d/%m/%Y')

    def doc_str(self):
        return str(self.doc_tipo) + ' ' + str(self.doc_num)

    def ape_nom(self):
        return str(self.apellido) + ' ' + str(self.nombre)


def get_upload_path(instance, filename):
    return os.path.join(
        "1", "2", filename)


class HistoriaClinicaAdjunto(TimeStampedModel):
    historia_clinica = models.ForeignKey(HistoriaClinica, editable=False)

    class Meta:
        permissions = (
            ("view_historia_clinica_adjunto", "Ver"),
            ("create_historia_clinica_adjunto", "Crear"),
            ("delete_historia_clinica_adjunto", "Borrar"),
        )

    def get_image_path(self, filename):
        return "pie_diabetico_app/historia_clinica_adjunto/"\
            + str(self.historia_clinica.id) + "/" + filename

    adjunto = models.FileField(upload_to=get_image_path, null=True)

    def filename(self):
        return os.path.basename(self.adjunto.name)

    def get_file_size(self):
        return self.adjunto._get_size()

    def __str__(self):
        return str(self.historia_clinica) + ' - ' + str(self.filename())
