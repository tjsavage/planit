import hashlib, random, string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import simplejson
from django.core import serializers
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

import logging
logger = logging.getLogger(__name__)

class UserProfileManager(BaseUserManager):
    def create(self, phone, password):
        if not phone or not password:
            raise ValueError("Must have a phone number")

        user = self.model(
            phone=to_python(phone)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    phone = PhoneNumberField(unique=True)
    phone_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'phone'

    objects = UserProfileManager()

    def __unicode__(self):
        return "%s" % (self.phone)

class LoginToken(models.Model):
    phone = PhoneNumberField()
    token = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    next_url = models.CharField(max_length=255, blank=True, null=True)

class VerificationToken(models.Model):
    user = models.ForeignKey('UserProfile')
    token = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

def generate_verification_token(user):
    sha = hashlib.sha1()
    sha.update(settings.SECRET_KEY)
    sha.update(str(user.phone))
    sha.update(randomword(20))

    token = sha.hexdigest()

    verification_token = VerificationToken.objects.create(token=token,
                                                        user=user)

    return verification_token

def generate_login_token(phone, next=""):
    sha = hashlib.sha1()
    sha.update(settings.SECRET_KEY)
    sha.update(str(to_python(phone)))
    sha.update(randomword(20))

    token = sha.hexdigest()

    login_token = LoginToken.objects.create(token=token, 
                                            phone=phone,
                                            next_url=next)

    return login_token

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

