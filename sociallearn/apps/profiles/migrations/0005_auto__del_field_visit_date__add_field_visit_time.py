# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Visit.date'
        db.delete_column(u'profiles_visit', 'date')

        # Adding field 'Visit.time'
        db.add_column(u'profiles_visit', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 2, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Visit.date'
        raise RuntimeError("Cannot reverse this migration. 'Visit.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Visit.date'
        db.add_column(u'profiles_visit', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)

        # Deleting field 'Visit.time'
        db.delete_column(u'profiles_visit', 'time')


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
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Instructor']", 'symmetrical': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'unit_name': ('django.db.models.fields.CharField', [], {'default': "'week'", 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000'})
        },
        u'courses.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.student': {
            'Meta': {'object_name': 'Student'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'profiles.visit': {
            'Meta': {'object_name': 'Visit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Student']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['profiles']