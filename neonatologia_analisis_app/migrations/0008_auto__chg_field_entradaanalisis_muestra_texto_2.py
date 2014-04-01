# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'EntradaAnalisis.muestra_texto_2'
        db.alter_column(u'neonatologia_analisis_app_entradaanalisis', 'muestra_texto_2', self.gf('django.db.models.fields.CharField')(max_length=3))

    def backwards(self, orm):

        # Changing field 'EntradaAnalisis.muestra_texto_2'
        db.alter_column(u'neonatologia_analisis_app_entradaanalisis', 'muestra_texto_2', self.gf('django.db.models.fields.CharField')(max_length=50))

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'neonatologia_analisis_app.determinacionestudioneonatologia': {
            'Meta': {'object_name': 'DeterminacionEstudioNeonatologia'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'neonatologia_analisis_app.entradaanalisis': {
            'Meta': {'object_name': 'EntradaAnalisis'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'apellido_madre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'determinaciones': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['neonatologia_analisis_app.DeterminacionEstudioNeonatologia']", 'symmetrical': 'False', 'blank': 'True'}),
            'doc_num_madre': ('django.db.models.fields.IntegerField', [], {}),
            'doc_tipo_madre': ('django.db.models.fields.CharField', [], {'default': "'DNI'", 'max_length': '3'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'etapa': ('django.db.models.fields.CharField', [], {'default': "'INI'", 'max_length': '3'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {}),
            'fecha_notif_familia': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laboratorio_obs': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'muestra_fecha_1': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'muestra_fecha_2': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'muestra_num_1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'muestra_num_2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'muestra_texto_2': ('django.db.models.fields.CharField', [], {'default': "'NOR'", 'max_length': '3', 'blank': 'True'}),
            'neonatologia_obs': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombre_madre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notificar_trabsoc': ('django.db.models.fields.CharField', [], {'default': "'SI'", 'max_length': '2'}),
            'prioridad': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'trabsoc_obs': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'neonatologia_analisis_app.entradaanalisisadjunto': {
            'Meta': {'object_name': 'EntradaAnalisisAdjunto'},
            'adjunto': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entrada_analisis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['neonatologia_analisis_app.EntradaAnalisis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['neonatologia_analisis_app']