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
                'busy': self.busy}

class Meeting(models.Model):
    name = models.CharField(max_length=255)
    range_start = models.DateTimeField()
    range_end = models.DateTimeField()
    creator = models.ForeignKey(UserProfile, related_name="creator")
    users = models.ManyToManyField(UserProfile, related_name="users")
    set_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField()

    def to_json(self):
        return { 'pk': '%s' % self.pk,
                'name': '%s' % self.name,
                'suggestedTimes': [s.to_json() for s in SuggestedTime.objects.filter(meeting=self)]}

class SuggestedTime(models.Model):
    meeting = models.ForeignKey('Meeting')
    datetime = models.DateTimeField()
    accepted = models.ManyToManyField(UserProfile, related_name="accepted")
    declined = models.ManyToManyField(UserProfile, related_name="declined")

    def to_json(self):
        return {'pk': '%s' % self.pk,
                'date': '%s' % self.datetime.strftime(settings.DATE_FORMAT),
                'time': '%s' % self.datetime.strftime(settings.TIME_FORMAT),
                'start': '%s' % self.datetime.strftime(settings.TIME_FORMAT),
                'end': '%s' % (self.datetime + timedelta(minutes=self.meeting.duration)).strftime(settings.TIME_FORMAT),
                'accepted': [u.to_json() for u in self.accepted.all()],
                'declined': [u.to_json() for u in self.declined.all()]}

def create_schedule(user, default_busy=None):
    for day in settings.DAYS:
        time = settings.START_TIME
        interval = settings.INTERVAL
        while time < settings.END_TIME:
            block, created = ScheduleBlock.objects.get_or_create(user=user,
                day=day,
                start=time,
                end=time+settings.INTERVAL)
            if "default_busy" is not None:
                block.busy = default_busy
                block.save()
            time += settings.INTERVAL

def create_schedule_signal(sender, instance, created, **kwargs):
    if created:
        create_schedule(instance, default_busy=False)


post_save.connect(create_schedule_signal, sender=UserProfile)