from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from planit.accounts.models import UserProfile
from planit.scheduling.models import ScheduleBlock

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def schedule(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)

    if request.method == 'GET':
        blocks_json = [block.to_json() for block in ScheduleBlock.objects.filter(user=user)]
        
        blocks_json = sorted_by_day(blocks_json)

        return HttpResponse(simplejson.dumps(blocks_json))

    elif request.method == 'POST':
        logger.debug(request.raw_post_data)
        blocks = simplejson.loads(request.raw_post_data)

        for block in blocks:
            schedule_block, created = ScheduleBlock.objects.get_or_create(user=user,
                                                                day=block["day"],
                                                                start=datetime.strptime(block["start"], settings.TIME_FORMAT),
                                                                end=datetime.strptime(block["end"], settings.TIME_FORMAT))
            schedule_block.busy = True if block["busy"] == "true" else False
            schedule_block.save()

        blocks_json = [block.to_json() for block in ScheduleBlock.objects.filter(user=user)]

        blocks_json = sorted_by_day(blocks_json)

        return HttpResponse(simplejson.dumps(blocks_json))

def sorted_by_day(blocks):
    return sorted(blocks, key=lambda b: settings.DAYS.index(b["day"]))