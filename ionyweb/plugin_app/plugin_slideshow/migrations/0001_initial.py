# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plugin_Slideshow'
        db.create_table('plugin_slideshow_plugin_slideshow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fx', self.gf('django.db.models.fields.CharField')(default='FA', max_length=3)),
            ('speed', self.gf('django.db.models.fields.IntegerField')(default=1000, null=True, blank=True)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=4000, null=True, blank=True)),
            ('pause', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('random', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pager', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pager_thumbs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('width_image', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('height_image', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('plugin_slideshow', ['Plugin_Slideshow'])

        # Adding model 'Slide'
        db.create_table('plugin_slideshow_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='slides', to=orm['plugin_slideshow.Plugin_Slideshow'])),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('plugin_slideshow', ['Slide'])

    def backwards(self, orm):
        # Deleting model 'Plugin_Slideshow'
        db.delete_table('plugin_slideshow_plugin_slideshow')

        # Deleting model 'Slide'
        db.delete_table('plugin_slideshow_slide')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'file_manager.filemanager': {
            'Meta': {'object_name': 'FileManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'filemanager'", 'null': 'True', 'blank': 'True', 'to': "orm['file_manager.Directory']"})
        },
        'page.page': {
            'Meta': {'object_name': 'Page'},
            'app_page_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'app_page_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'default_template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_diplayed_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modif': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'menu_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['page.Page']"}),
            'placeholder_slug': ('django.db.models.fields.SlugField', [], {'default': "'content-placeholder-1'", 'max_length': '50'}),
            'plugin_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['website.WebSite']"})
        },
        'plugin.pluginrelation': {
            'Meta': {'ordering': "['plugin_order']", 'object_name': 'PluginRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'display_on_new_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'plugins'", 'symmetrical': 'False', 'to': "orm['page.Page']"}),
            'placeholder_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'plugin_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'plugin_slideshow.plugin_slideshow': {
            'Meta': {'object_name': 'Plugin_Slideshow'},
            'fx': ('django.db.models.fields.CharField', [], {'default': "'FA'", 'max_length': '3'}),
            'height_image': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pager_thumbs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pause': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'random': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'default': '1000', 'null': 'True', 'blank': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '4000', 'null': 'True', 'blank': 'True'}),
            'width_image': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'plugin_slideshow.slide': {
            'Meta': {'object_name': 'Slide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slides'", 'to': "orm['plugin_slideshow.Plugin_Slideshow']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'website.website': {
            'Meta': {'object_name': 'WebSite'},
            'analytics_key': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'default_layout': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'default_template': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'website_set'", 'unique': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['sites.Site']"}),
            'files_library': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'website'", 'null': 'True', 'to': "orm['file_manager.FileManager']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_maintenance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'main_menu_levels': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'ndds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'website'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['website.WebSiteOwner']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'website.websiteowner': {
            'Meta': {'object_name': 'WebSiteOwner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'websites_owned'", 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'websites_owned'", 'to': "orm['website.WebSite']"})
        }
    }

    complete_apps = ['plugin_slideshow']