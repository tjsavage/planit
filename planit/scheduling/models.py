from django.db import models

from planit.accounts.models import UserProfile

class ScheduleBlock(models.Model):
    DAYS = (
        ('Su', 'Sunday'),
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('Sa', 'Saturday')
    )

    user = models.ForeignKey(UserProfile)
    day = models.CharField(max_length=2, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
