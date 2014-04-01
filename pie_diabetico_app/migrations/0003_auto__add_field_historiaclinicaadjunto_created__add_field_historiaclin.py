# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HistoriaClinicaAdjunto.created'
        db.add_column(u'pie_diabetico_app_historiaclinicaadjunto', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 23, 0, 0)),
                      keep_default=False)

        # Adding field 'HistoriaClinicaAdjunto.created_user'
        db.add_column(u'pie_diabetico_app_historiaclinicaadjunto', 'created_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HistoriaClinicaAdjunto.created'
        db.delete_column(u'pie_diabetico_app_historiaclinicaadjunto', 'created')

        # Deleting field 'HistoriaClinicaAdjunto.created_user'
        db.delete_column(u'pie_diabetico_app_historiaclinicaadjunto', 'created_user_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pie_diabetico_app.historiaclinica': {
            'Meta': {'unique_together': "(('fecha', 'doc_num', 'doc_tipo'),)", 'object_name': 'HistoriaClinica'},
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'amputacion': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'angioplatia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'antecedentes_otros': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'antibiograma': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'antibiotico': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'bacterio_germen': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'biopsia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'bypass': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'color_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'color_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'control_glucemio': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'convive': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'cultivo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'curaciones': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'diabetes': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'directo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'dislipidemia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'doc_num': ('django.db.models.fields.IntegerField', [], {}),
            'doc_tipo': ('django.db.models.fields.CharField', [], {'default': "'DNI'", 'max_length': '3'}),
            'dolorosa_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'dolorosa_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dorsiflexion_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'dorsiflexion_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'edad': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'edad_diag_diabetes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'educacion': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'estado_soceco': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'estilo_vida': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'examen_pie': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'extension_1dedo_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'extension_1dedo_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'fuerza_muscular_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'fuerza_muscular_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'hiperqueratosis': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'historia_clinica': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hta': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'humedad_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'humedad_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'informe': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'intertrigo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'laboratorio': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'macrovascular': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'maniobra_abanico_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'maniobra_abanico_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'micologico': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'nefropatia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'neuropatia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'onicomicosis': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'peso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pie_der_almohadilla': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_der_ampollas': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_der_callosidades': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_der_dedos': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_der_fisuras': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_der_forma': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_der_infeccion': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_der_ulcera': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_izq_almohadilla': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_izq_ampollas': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_izq_callosidades': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_izq_dedos': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_izq_fisuras': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_izq_forma': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pie_izq_infeccion': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'pie_izq_ulcera': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'piel_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'piel_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_pedio_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_pedio_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_popliteo_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_popliteo_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_tibial_post_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'pulso_tibial_post_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'reflejo_aquilano_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'reflejo_aquilano_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'reflejo_rotuliano_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'reflejo_rotuliano_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'relleno_capilar_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'relleno_capilar_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'retinopatia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'tabaquismo': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'tactil_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'tactil_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'talla': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'termica_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'termica_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'tratamiento': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'ulceras': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'ulceras_desc': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'ulceras_previas': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'unas_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'unas_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'vasculopatia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'vellos_der': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'vellos_izq': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'vibratoria_der': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'vibratoria_izq': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'vision_dism': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'pie_diabetico_app.historiaclinicaadjunto': {
            'Meta': {'object_name': 'HistoriaClinicaAdjunto'},
            'adjunto': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'historia_clinica': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pie_diabetico_app.HistoriaClinica']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pie_diabetico_app']
