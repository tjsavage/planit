from datetime import time, timedelta

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from planit.accounts.models import UserProfile

class ScheduleBlock(models.Model):
    user = models.ForeignKey(UserProfile)
    day = models.CharField(max_length=30)
    start = models.TimeField()
    end = models.TimeField()
    busy = models.BooleanField(default=False)

    def to_json(self):
        return { 'day': '%s' % self.day, 
                'start': '%s' % time.strftime(self.start, settings.TIME_FORMAT), 
                'end': '%s' % time.strftime(self.end, settings.TIME_FORMAT), 
                'status': '%s' % str(self.busy).lower()}


def create_schedule(sender, instance, created, **kwargs):
    if created:
        for day in settings.DAYS:
            time = settings.START_TIME
            interval = settings.INTERVAL
            while time < settings.END_TIME:
                ScheduleBlock.objects.get_or_create(user=instance,
                    day=day,
                    start=time,
                    end=time+settings.INTERVAL,
                    busy=False)
                time += settings.INTERVAL


post_save.connect(create_schedule, sender=UserProfile)