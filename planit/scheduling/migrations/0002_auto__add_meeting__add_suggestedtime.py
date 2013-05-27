# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table(u'scheduling_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('range_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('range_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['accounts.UserProfile'])),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'scheduling', ['Meeting'])

        # Adding M2M table for field users on 'Meeting'
        db.create_table(u'scheduling_meeting_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'scheduling.meeting'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False))
        ))
        db.create_unique(u'scheduling_meeting_users', ['meeting_id', 'userprofile_id'])

        # Adding model 'SuggestedTime'
        db.create_table(u'scheduling_suggestedtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduling.Meeting'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'scheduling', ['SuggestedTime'])

        # Adding M2M table for field accepted on 'SuggestedTime'
        db.create_table(u'scheduling_suggestedtime_accepted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('suggestedtime', models.ForeignKey(orm[u'scheduling.suggestedtime'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False))
        ))
        db.create_unique(u'scheduling_suggestedtime_accepted', ['suggestedtime_id', 'userprofile_id'])

        # Adding M2M table for field declined on 'SuggestedTime'
        db.create_table(u'scheduling_suggestedtime_declined', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('suggestedtime', models.ForeignKey(orm[u'scheduling.suggestedtime'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False))
        ))
        db.create_unique(u'scheduling_suggestedtime_declined', ['suggestedtime_id', 'userprofile_id'])


    def backwards(self, orm):
        # Deleting model 'Meeting'
        db.delete_table(u'scheduling_meeting')

        # Removing M2M table for field users on 'Meeting'
        db.delete_table('scheduling_meeting_users')

        # Deleting model 'SuggestedTime'
        db.delete_table(u'scheduling_suggestedtime')

        # Removing M2M table for field accepted on 'SuggestedTime'
        db.delete_table('scheduling_suggestedtime_accepted')

        # Removing M2M table for field declined on 'SuggestedTime'
        db.delete_table('scheduling_suggestedtime_declined')


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
        u'scheduling.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': u"orm['accounts.UserProfile']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'range_end': ('django.db.models.fields.DateTimeField', [], {}),
            'range_start': ('django.db.models.fields.DateTimeField', [], {}),
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