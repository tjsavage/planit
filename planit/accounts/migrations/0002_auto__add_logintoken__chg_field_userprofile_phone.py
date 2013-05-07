# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoginToken'
        db.create_table(u'accounts_logintoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('next_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['LoginToken'])


        # Changing field 'UserProfile.phone'
        db.alter_column(u'accounts_userprofile', 'phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(unique=True, max_length=128))

    def backwards(self, orm):
        # Deleting model 'LoginToken'
        db.delete_table(u'accounts_logintoken')


        # Changing field 'UserProfile.phone'
        db.alter_column(u'accounts_userprofile', 'phone', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))

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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '128'}),
            'phone_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['accounts']