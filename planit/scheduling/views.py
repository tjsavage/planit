from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    pass

@login_required
def schedule(request):
    user = request.user

    return render_to_response("scheduling/schedule.html", {}, 
        context_instance=RequestContext(request))

def create_meeting(request):

    return render_to_response("scheduling/create_meeting.html", {},
        context_instance=RequestContext(request))
