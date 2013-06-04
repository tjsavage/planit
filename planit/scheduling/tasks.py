from datetime import time, datetime, timedelta

from django.conf import settings

from planit.scheduling.models import ScheduleBlock, SuggestedTime, Meeting
from planit.util.time import increment_time
from planit.accounts.sms import send_message

def is_available(user, start, duration):
    if start.minute != 0 and start.minute != 30:
        raise ValueError("Only configured to work in 30 minute intervals")
    if duration % 30 != 0:
        raise ValueError("Only configured to work in 30 minute intervals")

    free_block_start = time(hour=start.hour, minute=start.minute)
    free_contiguous_time = 0
    day = start.strftime("%A")
    while free_contiguous_time < duration:
        blocks = ScheduleBlock.objects.filter(user=user, start=free_block_start, day=day)
        if blocks.count() > 0:
            block = blocks[0]
            if block.busy:
                return False
        else:
            return False
        free_contiguous_time += 30
        free_block_start = increment_time(start, free_contiguous_time)

    return True

def best_starts(users, range_start, range_end, duration):
    """
    Return a list of potential start times, in order of the most people that can make it.
    Returns a list of tuples in the form of [(datetime.datetime, [users who can make it])]
    """
    result = []

    potential_start = range_start
    td_duration = timedelta(minutes=duration)
    while potential_start < range_end:
        if potential_start.hour < settings.START_TIME.hour:
            potential_start += settings.INTERVAL
            continue
        attendees = []
        for user in users:
            if is_available(user, potential_start, duration):
                attendees.append(user)
        result.append((potential_start, attendees))
        potential_start += settings.INTERVAL

    result = sorted(result, key=lambda t: len(t[1]), reverse=True)
    return result

def generate_suggested_times(meeting):
        starts = best_starts(meeting.users.all(), meeting.range_start, meeting.range_end, meeting.duration)
        for start in starts[:20]:
            SuggestedTime.objects.create(meeting=meeting,
                                        datetime=start[0])
        return True

def send_out_set_time(meeting):
    for user in meeting.users.all():
        send_message(user.phone, "Hello from GoGroup! Your meeting %s has been set for %s" % (meeting.name, meeting.set_time.formatted()))
