from datetime import time

def increment_time(t, minutes):
    m = t.minute
    h = t.hour

    m += minutes
    h += m / 60
    m = m % 60

    h = h % 24

    return time(hour=h, minute=m)