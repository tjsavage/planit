from datetime import time, datetime, timedelta

from planit.scheduling.models import ScheduleBlock
from planit.util.time import increment_time

def is_available(user, start, duration):
    if start.minute != 0 and start.minute != 30:
        raise ValueError("Only configured to work in 30 minute intervals")
    if duration % 30 != 0:
        raise ValueError("Only configured to work in 30 minute intervals")

    free_block_start = time(hour=start.hour, minute=start.minute)
    free_contiguous_time = 0
    day = start.strftime("%A")
    while free_contiguous_time < duration:
        block = ScheduleBlock.objects.filter(user=user, start=free_block_start, day=day)[0]
        if block.busy:
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
        attendees = []
        for user in users:
            if is_available(user, potential_start, duration):
                attendees.append(user)
        result.append((potential_start, attendees))
        potential_start += td_duration

    result = sorted(result, key=lambda t: len(t[1]), reverse=True)
    return result