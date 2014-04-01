# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntradaAnalisis'
        db.create_table(u'neonatologia_analisis_app_entradaanalisis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('estado', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido_madre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nombre_madre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')(null=True)),
            ('domicilio', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('determinacion', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('muestra_fecha_1', self.gf('django.db.models.fields.DateField')(null=True)),
            ('muestra_num_1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('notificar_trabsoc', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('neonatologia_obs', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('fecha_notif_familia', self.gf('django.db.models.fields.DateField')(null=True)),
            ('trabsoc_obs', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('muestra_fecha_2', self.gf('django.db.models.fields.DateField')(null=True)),
            ('muestra_num_2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('muestra_texto_2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('laboratorio_obs', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'neonatologia_analisis_app', ['EntradaAnalisis'])

        # Adding unique constraint on 'EntradaAnalisis', fields ['fecha', 'apellido', 'nombre']
        db.create_unique(u'neonatologia_analisis_app_entradaanalisis', ['fecha', 'apellido', 'nombre'])

        # Adding model 'EntradaAnalisisAdjunto'
        db.create_table(u'neonatologia_analisis_app_entradaanalisisadjunto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('entrada_analisis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['neonatologia_analisis_app.EntradaAnalisis'])),
            ('adjunto', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'neonatologia_analisis_app', ['EntradaAnalisisAdjunto'])


    def backwards(self, orm):
        # Removing unique constraint on 'EntradaAnalisis', fields ['fecha', 'apellido', 'nombre']
        db.delete_unique(u'neonatologia_analisis_app_entradaanalisis', ['fecha', 'apellido', 'nombre'])

        # Deleting model 'EntradaAnalisis'
        db.delete_table(u'neonatologia_analisis_app_entradaanalisis')

        # Deleting model 'EntradaAnalisisAdjunto'
        db.delete_table(u'neonatologia_analisis_app_entradaanalisisadjunto')


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
        u'neonatologia_analisis_app.entradaanalisis': {
            'Meta': {'unique_together': "(('fecha', 'apellido', 'nombre'),)", 'object_name': 'EntradaAnalisis'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'apellido_madre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'determinacion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_notif_familia': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laboratorio_obs': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'muestra_fecha_1': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'muestra_fecha_2': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'muestra_num_1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'muestra_num_2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'muestra_texto_2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'neonatologia_obs': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nombre_madre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notificar_trabsoc': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
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