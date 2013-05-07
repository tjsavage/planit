import re

import logging

logger = logging.getLogger(__name__)

def format_number(input):
    logger.debug(input)
    phone_re = re.compile(r'\+?1?(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$', re.VERBOSE)
    search = phone_re.search(input)
    if not search:
        raise ValueError("Invalid input")
    groups = search.groups()
    return "+1 (%s) %s-%s" % (groups[0], groups[1], groups[2])