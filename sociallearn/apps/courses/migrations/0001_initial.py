# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Instructor'
        db.create_table(u'courses_instructor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'courses', ['Instructor'])

        # Adding model 'Course'
        db.create_table(u'courses_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2000)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'courses', ['Course'])

        # Adding M2M table for field instructors on 'Course'
        m2m_table_name = db.shorten_name(u'courses_course_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False)),
            ('instructor', models.ForeignKey(orm[u'courses.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'instructor_id'])


    def backwards(self, orm):
        # Deleting model 'Instructor'
        db.delete_table(u'courses_instructor')

        # Deleting model 'Course'
        db.delete_table(u'courses_course')

        # Removing M2M table for field instructors on 'Course'
        db.delete_table(db.shorten_name(u'courses_course_instructors'))


    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Instructor']", 'symmetrical': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000'})
        },
        u'courses.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['courses']