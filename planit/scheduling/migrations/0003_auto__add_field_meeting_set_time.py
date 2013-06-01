# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Meeting.set_time'
        db.add_column(u'scheduling_meeting', 'set_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Meeting.set_time'
        db.delete_column(u'scheduling_meeting', 'set_time')


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'newly_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '128'}),
            'phone_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'scheduling.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': u"orm['accounts.UserProfile']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'range_end': ('django.db.models.fields.DateTimeField', [], {}),
            'range_start': ('django.db.models.fields.DateTimeField', [], {}),
            'set_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['accounts.UserProfile']"})
        },
        u'scheduling.scheduleblock': {
            'Meta': {'object_name': 'ScheduleBlock'},
            'busy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"})
        },
        u'scheduling.suggestedtime': {
            'Meta': {'object_name': 'SuggestedTime'},
            'accepted': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'accepted'", 'symmetrical': 'False', 'to': u"orm['accounts.UserProfile']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'declined': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'declined'", 'symmetrical': 'False', 'to': u"orm['accounts.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scheduling.Meeting']"})
        }
    }

    complete_apps = ['scheduling']