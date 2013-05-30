import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson

from planit.scheduling.models import Meeting
from planit.accounts.models import UserProfile, invite_user, invite_to_meeting

import logging
logger = logging.getLogger(__name__)

def home(request):
    pass

@login_required
def schedule(request):
    user = request.user

    return render_to_response("scheduling/schedule.html", {}, 
        context_instance=RequestContext(request))

@login_required
def create_meeting(request):
    if request.method == 'POST':
        data = simplejson.loads(request.body)

        name = data["name"]
        start = datetime.datetime.strptime(data["start"], "%d-%m-%Y")
        end = datetime.datetime.strptime(data["end"], "%d-%m-%Y")
        duration = int(data["duration"])

        meeting = Meeting.objects.create(name=name, 
                                        range_start=start, 
                                        range_end=end,
                                        duration=duration,
                                        creator=request.user)
        for invitee in data["invitees"]:
            u, created = UserProfile.objects.match_or_create(phone=invitee["phone"], name=invitee["name"])
            if created:
                invite_user(u, invitor=request.user, next="/scheduling/meeting/%d/" % meeting.pk)
            else:
                invite_to_meeting(u, meeting, invitor=request.user)


        return HttpResponse(simplejson.dumps(meeting.to_json()));

    return render_to_response("scheduling/create_meeting.html", {},
        context_instance=RequestContext(request))
