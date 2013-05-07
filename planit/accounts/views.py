from django.shortcuts import render_to_response
from django.template import RequestContext

def register(request):
    if request.method == 'GET':
        return render_to_response('accounts/register.html', {},
            context_instance=RequestContext(request))