# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScheduleBlock'
        db.create_table(u'scheduling_scheduleblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('busy', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'scheduling', ['ScheduleBlock'])


    def backwards(self, orm):
        # Deleting model 'ScheduleBlock'
        db.delete_table(u'scheduling_scheduleblock')


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '128'}),
            'phone_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'scheduling.scheduleblock': {
            'Meta': {'object_name': 'ScheduleBlock'},
            'busy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"})
        }
    }

    complete_apps = ['scheduling']