# -*- encoding: utf-8 -*-

import datetime
import os.path

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str  # , smart_unicode

from core.models import TimeStampedModel


class DeterminacionEstudioNeonatologia(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="descripción"
    )

    def __str__(self):
        return smart_str(self.nombre)


class EntradaAnalisis(TimeStampedModel):

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
    ETAPA_CHOICES = (
        ('INI', 'Iniciado'),
        ('NTS', 'Notif. Trab. Soc.'),
        ('NOT', 'Notificado'),
        ('COM', 'Completado'),
    )
    etapa = models.CharField(max_length=3,
                             choices=ETAPA_CHOICES,
                             default='INI')

    # Campos Neonatología
    fecha = models.DateField(default=datetime.date.today)
    PRIORIDAD_CHOICES = (
        ('U', 'Urgente'),
        ('N', 'Normal'),
    )
    prioridad = models.CharField(max_length=1,
                                 choices=PRIORIDAD_CHOICES,
                                 default='N')
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    apellido = models.CharField(
        max_length=50,
        verbose_name="apellido"
    )
    nombre = models.CharField(
        max_length=50,
        verbose_name="nombre"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        verbose_name="sexo"
    )
    fecha_nacimiento = models.DateField(
        verbose_name="fecha nacimiento"
    )
    apellido_madre = models.CharField(
        max_length=50,
        verbose_name="apellido madre"
    )
    nombre_madre = models.CharField(
        max_length=50,
        verbose_name="nombre madre"
    )
    TIPO_DOCS_CHOICES = (
        ('DNI', 'DNI'),
        ('LE', 'LE'),
        ('LC', 'LC'),
        ('CI', 'CI'),
    )
    doc_tipo_madre = models.CharField(
        max_length=3,
        choices=TIPO_DOCS_CHOICES,
        default='DNI',
        verbose_name="doc. tipo madre"
    )
    doc_num_madre = models.IntegerField(
        verbose_name="doc. número madre",
        validators=[validate_doc_num]
    )
    domicilio = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="domicilio"
    )
    telefono = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="teléfono"
    )
    determinaciones = models.ManyToManyField(
        DeterminacionEstudioNeonatologia,
        blank=True,
        verbose_name="determinaciones a repetir"
    )
    muestra_fecha_1 = models.DateField(
        null=True,
        blank=True,
        verbose_name="fecha de primera muestra"
    )
    muestra_num_1 = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="número de primera muestra"
    )

    SINO_CHOICES = (
        ('SI', 'Sí'),
        ('NO', 'No'),
    )
    notificar_trabsoc = models.CharField(
        max_length=2,
        choices=SINO_CHOICES,
        verbose_name="notificar Trabajo Social",
        default='SI',
    )
    neonatologia_obs = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="observaciones"
    )

    # Campos Trabajo Social
    fecha_notif_familia = models.DateField(
        null=True,
        blank=True,
        verbose_name="fecha notificación familia"
    )
    trabsoc_obs = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="observaciones"
    )

    # Campos Laboratorio
    muestra_num_2 = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="número de muestra repetición"
    )
    muestra_fecha_2 = models.DateField(
        null=True,
        blank=True,
        verbose_name="fecha de muestra repetición"
    )
    MUESTRA_TEXTO_CHOICES = (
        ('NOR', 'Normal'),
        ('ALT', 'Alterado'),
    )
    muestra_texto_2 = models.CharField(
        max_length=3,
        choices=MUESTRA_TEXTO_CHOICES,
        blank=True,
        verbose_name="resultado repetición",
    )
    laboratorio_obs = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="observaciones"
    )

    class Meta:
        permissions = (
            ("view_entrada_analisis", "Ver"),
            ("create_entrada_analisis", "Crear"),
            ("change_entrada_analisis_neo", "Modificar neo"),
            ("change_entrada_analisis_trabsoc", "Modificar trabsoc"),
            ("change_entrada_analisis_lab", "Modificar lab"),
            ("delete_entrada_analisis", "Borrar"),
            ("restore_entrada_analisis", "Restaurar")
        )

    def __str__(self):
        return self.fecha.strftime('%d/%m/%Y') +\
            ' ' + smart_str(self.apellido) + ' ' + smart_str(self.nombre)

    def fecha_format(self):
        return self.fecha.strftime('%d/%m/%Y')

    def ape_nom(self):
        return smart_str(self.apellido) + ' ' + smart_str(self.nombre)

    def is_analisis_retraso(self):
        if self.fecha_notif_familia is None:
            return False
        if self.muestra_fecha_2 is not None:
            return False
        dd = datetime.date.today() - self.fecha_notif_familia
        if dd > datetime.timedelta(hours=72):
            return True
        return False

    def get_current_etapa(self):
        # Set etapa
        if not self.muestra_num_2 == '':
            etapa = 'COM'
        elif self.fecha_notif_familia is not None:
            etapa = 'NOT'
        elif self.notificar_trabsoc == 'SI':
            etapa = 'NTS'
        else:
            etapa = 'INI'
        return etapa


def get_upload_path(instance, filename):
    return os.path.join(
        "1", "2", filename
    )


class EntradaAnalisisAdjunto(TimeStampedModel):
    entrada_analisis = models.ForeignKey(EntradaAnalisis, editable=False)

    def get_image_path(self, filename):
        return "neonatologia_analisis_app/entrada_analisis_adjunto/"\
            + str(self.entrada_analisis.id) + "/" + filename

    adjunto = models.FileField(upload_to=get_image_path, null=True)

    class Meta:
        permissions = (
            ("view_entrada_analisis_adjunto", "Ver"),
            ("create_entrada_analisis_adjunto", "Crear"),
            ("delete_entrada_analisis_adjunto", "Borrar")
        )

    def filename(self):
        return os.path.basename(self.adjunto.name)

    def get_file_size(self):
        return self.adjunto._get_size()

    def __str__(self):
        return smart_str(self.entrada_analisis) + ' - ' +\
            smart_str(self.filename())
