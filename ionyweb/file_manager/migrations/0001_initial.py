# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Directory'
        db.create_table('file_manager_directory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['file_manager.Directory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('file_manager', ['Directory'])

        # Adding model 'FileManager'
        db.create_table('file_manager_filemanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='filemanager', null=True, blank=True, to=orm['file_manager.Directory'])),
        ))
        db.send_create_signal('file_manager', ['FileManager'])

        # Adding model 'File'
        db.create_table('file_manager_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dir', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['file_manager.Directory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_creation', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_modification', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('file_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('file_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('file_manager', ['File'])

        # Adding model 'Image'
        db.create_table('file_manager_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_manager', ['Image'])

        # Adding model 'Document'
        db.create_table('file_manager_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_manager', ['Document'])

        # Adding model 'Audio'
        db.create_table('file_manager_audio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_manager', ['Audio'])

        # Adding model 'Archive'
        db.create_table('file_manager_archive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_manager', ['Archive'])

        # Adding model 'Other'
        db.create_table('file_manager_other', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_manager', ['Other'])

    def backwards(self, orm):
        # Deleting model 'Directory'
        db.delete_table('file_manager_directory')

        # Deleting model 'FileManager'
        db.delete_table('file_manager_filemanager')

        # Deleting model 'File'
        db.delete_table('file_manager_file')

        # Deleting model 'Image'
        db.delete_table('file_manager_image')

        # Deleting model 'Document'
        db.delete_table('file_manager_document')

        # Deleting model 'Audio'
        db.delete_table('file_manager_audio')

        # Deleting model 'Archive'
        db.delete_table('file_manager_archive')

        # Deleting model 'Other'
        db.delete_table('file_manager_other')

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'file_manager.archive': {
            'Meta': {'object_name': 'Archive'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'file_manager.audio': {
            'Meta': {'object_name': 'Audio'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'file_manager.directory': {
            'Meta': {'object_name': 'Directory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['file_manager.Directory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'file_manager.document': {
            'Meta': {'object_name': 'Document'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'file_manager.file': {
            'Meta': {'object_name': 'File'},
            'date_creation': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dir': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['file_manager.Directory']"}),
            'file_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'file_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'file_manager.filemanager': {
            'Meta': {'object_name': 'FileManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'filemanager'", 'null': 'True', 'blank': 'True', 'to': "orm['file_manager.Directory']"})
        },
        'file_manager.image': {
            'Meta': {'object_name': 'Image'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'file_manager.other': {
            'Meta': {'object_name': 'Other'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['file_manager']