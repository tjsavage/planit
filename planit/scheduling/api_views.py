from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from planit.accounts.models import UserProfile
from planit.scheduling.models import ScheduleBlock, Meeting, SuggestedTime
from planit.scheduling import tasks

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
            schedule_block.busy = block["busy"]
            schedule_block.save()

        blocks_json = [block.to_json() for block in ScheduleBlock.objects.filter(user=user)]

        blocks_json = sorted_by_day(blocks_json)

        return HttpResponse(simplejson.dumps(blocks_json))

def suggestions(request):
    """
    GET request with parameters:
    users -> comma-separated list of user user_ids
    start -> date formatted in ISO format: YYYY-MM-DDTHH:MM:SS
    end -> date formatted in ISO format
    duration -> minute duration of meeting
    """
    if request.method == 'GET':
        user_ids = request.GET['users'].split(",")
        users = [get_object_or_404(UserProfile, pk=user_id) for user_id in user_ids]
        start = datetime.strptime(request.GET['start'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(request.GET['end'], "%Y-%m-%dT%H:%M:%S")
        duration = int(request.GET['duration'])

        suggestions = tasks.best_starts(users, start, end, duration)

        results = []
        for suggestion in suggestions:
            d = {}
            d["start"] = suggestion[0].strftime("%Y-%m-%dT%H:%M:%S")
            d["duration"] = duration
            d["available"] = [u.to_json() for u in suggestion[1]]
            results.append(d)

        return HttpResponse(simplejson.dumps(results))

def meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=int(meeting_id))

    #if not request.user in meeting.users.all():
    #    return HttpResponse("You don't belong here")

    return HttpResponse(simplejson.dumps(meeting.to_json()))

def meeting_availabilities(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=int(meeting_id))

    return HttpResponse(simplejson.dumps(meeting.to_json()["suggestedTimes"]))

@login_required
def meeting_availability(request, meeting_id, suggested_time_id):
    meeting = get_object_or_404(Meeting, pk=int(meeting_id))
    suggested_time = get_object_or_404(SuggestedTime, pk=int(suggested_time_id))

    if not request.user in meeting.users.all():
        return HttpResponse("You don't belong here")

    if suggested_time.meeting != meeting:
        return HttpResponse("Your meeting and time don't match")

    if request.method == 'POST':
        if request.user in suggested_time.declined.all():
            suggested_time.declined.remove(request.user)
        if request.user not in suggested_time.accepted.all():
            suggested_time.accepted.add(request.user)
    elif request.method == 'DELETE':
        if request.user not in suggested_time.declined.all():
            suggested_time.declined.add(request.user)
        if request.user in suggested_time.accepted.all():
            suggested_time.accepted.remove(request.user)
    elif request.method == 'GET':
        if request.user in suggested_time.declined.all():
            return HttpResponse('{"status":"declined"}');
        elif request.user in suggested_time.accepted.all():
            return HttpResponse('{"status":"accepted"}');
        else:
            return HttpResponse('{"status":""}');

    suggested_time.save()
    return HttpResponse("200")



def sorted_by_day(blocks):
    return sorted(blocks, key=lambda b: settings.DAYS.index(b["day"]))