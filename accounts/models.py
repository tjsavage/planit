from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=12, null=True, blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        new_user_profile = UserProfile(user=instance)
        new_user_profile.save()

post_save.connect(create_user_profile, sender=User)