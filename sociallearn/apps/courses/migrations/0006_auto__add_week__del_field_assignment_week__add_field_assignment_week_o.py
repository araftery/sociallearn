# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Week'
        db.create_table(u'courses_week', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'courses', ['Week'])

        # Adding M2M table for field assignments on 'Week'
        m2m_table_name = db.shorten_name(u'courses_week_assignments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('week', models.ForeignKey(orm[u'courses.week'], null=False)),
            ('assignment', models.ForeignKey(orm[u'courses.assignment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['week_id', 'assignment_id'])

        # Deleting field 'Assignment.week'
        db.delete_column(u'courses_assignment', 'week')

        # Adding field 'Assignment.week_old'
        db.add_column(u'courses_assignment', 'week_old',
                      self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2),
                      keep_default=False)

        # Adding field 'Course.unit_name'
        db.add_column(u'courses_course', 'unit_name',
                      self.gf('django.db.models.fields.CharField')(default='week', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Week'
        db.delete_table(u'courses_week')

        # Removing M2M table for field assignments on 'Week'
        db.delete_table(db.shorten_name(u'courses_week_assignments'))

        # Adding field 'Assignment.week'
        db.add_column(u'courses_assignment', 'week',
                      self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2),
                      keep_default=False)

        # Deleting field 'Assignment.week_old'
        db.delete_column(u'courses_assignment', 'week_old')

        # Deleting field 'Course.unit_name'
        db.delete_column(u'courses_course', 'unit_name')


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
        u'courses.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'child'", 'unique': 'True', 'null': 'True', 'to': u"orm['courses.Assignment']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '750'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'week_old': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'courses.assignmentcompletion': {
            'Meta': {'object_name': 'AssignmentCompletion'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Assignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Student']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'courses.assignmentstart': {
            'Meta': {'object_name': 'AssignmentStart'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Assignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Student']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
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
        u'courses.week': {
            'Meta': {'object_name': 'Week'},
            'assignments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Assignment']", 'symmetrical': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'profiles.student': {
            'Meta': {'object_name': 'Student'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['courses']