from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import simplejson
from django.core import serializers

from planit.util.phone import format_number

class UserProfileManager(BaseUserManager):
    def create(self, phone, password):
        if not phone or not password:
            raise ValueError("Must have a phone number")

        user = self.model(
            phone=format_number(phone)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user




class UserProfile(AbstractBaseUser):
    phone = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'phone'

    objects = UserProfileManager()

    def __unicode__(self):
        return "%s" % (self.phone)

