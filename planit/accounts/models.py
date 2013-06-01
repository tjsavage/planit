import hashlib, random, string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import simplejson
from django.core import serializers
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

from planit.accounts.sms import send_verification, send_message

import logging
logger = logging.getLogger(__name__)

class UserProfileManager(BaseUserManager):
    def create(self, phone, password=None, name=None):
        if not phone:
            raise ValueError("Must have a phone number")


        user = self.model(
            phone=phone
        )

        if not password:
            password = "nopassword"
            user.newly_created = True

        user.set_password(password)
        user.name = name
        user.save(using=self._db)
        return user

    def match_or_create(self, name=None, phone=None):
        phone = to_python(phone)

        user = self.match(name, phone)
        created = False
        if not user:
            created = True
            user = UserProfile.objects.create(phone,
                                            name=name)
            user.set_password("nopassword")
            user.newly_created = True
            user.save(using=self._db)
        return user, created

    def match(self, name, phone):
        phone = to_python(phone)

        phone_matches = UserProfile.objects.filter(phone=phone)
        if phone_matches.count():
            return phone_matches[0]

        return None

class UserProfile(AbstractBaseUser):
    phone = PhoneNumberField(unique=True)
    phone_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    newly_created = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserProfileManager()

    def __unicode__(self):
        return "%s" % (self.phone)

    def to_json(self):
        result = {}
        result["phone"] = str(self.phone)
        result["name"] = self.name
        result["email"] = self.email
        return result

class LoginToken(models.Model):
    phone = PhoneNumberField()
    token = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    next_url = models.CharField(max_length=255, blank=True, null=True)

class VerificationToken(models.Model):
    user = models.ForeignKey('UserProfile')
    token = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)


def invite_user(user, invitor=None, next=None):
    if not user.newly_created:
        raise Error

    token = generate_login_token(user.phone, next=next)

    if invitor:
        body = "You were invited by %s to schedule a meeting. Schedule at http://gogroup.us/t/?token=%s" % (invitor.name, token.token)
    else:
        body = "You were invited to GoGroup! Get started at http://gogroup.us/t/?token=%s" % (token.token)
    send_message(user.phone, body)

def invite_to_meeting(user, meeting, invitor=None):
    token = generate_login_token(user.phone, next="/scheduling/meeting/%d/" % meeting.pk)

    if invitor:
        body = "You were invited by %s to schedule a meeting. Schedule at http://gogroup.us/t/?token=%s" % (invitor.name, token.token)
    else:
        body = "You were invited to schedule a meeting with goGroup! Get started at http://gogroup.us/t/?token=%s" % (token.token)
    send_message(user.phone, body)





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

