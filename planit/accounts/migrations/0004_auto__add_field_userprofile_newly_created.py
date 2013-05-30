# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.newly_created'
        db.add_column(u'accounts_userprofile', 'newly_created',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.newly_created'
        db.delete_column(u'accounts_userprofile', 'newly_created')


    models = {
        u'accounts.logintoken': {
            'Meta': {'object_name': 'LoginToken'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
        u'accounts.verificationtoken': {
            'Meta': {'object_name': 'VerificationToken'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.UserProfile']"})
        }
    }

    complete_apps = ['accounts']