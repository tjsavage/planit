import re

def format_number(input):
    phone_re = re.compile(r'\+?1?(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', re.VERBOSE)
    groups = phone_re.search(input).groups()
    return "+1 (%s) %s-%s" % (groups[0], groups[1], groups[2])