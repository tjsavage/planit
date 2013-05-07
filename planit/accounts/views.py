from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

from planit.accounts.models import UserProfile
from planit.util.phone import format_number

def register(request):
    if request.method == 'GET':
        return render_to_response('accounts/register.html', {},
            context_instance=RequestContext(request))
    elif request.method == 'POST':
        try:
            phone = format_number(request.POST.get("phone", None))
        except ValueError:
            return HttpResponse("Invalid phone")

        password = request.POST.get("password", None)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)

        if UserProfile.objects.filter(phone=phone).count():
            return HttpResponse("already created")

        user = UserProfile.objects.create(phone, password)
        if not user:
            return HttpResponse("error")

        user.name = name
        user.email = email

        user.save()

        user = auth.authenticate(phone=phone, password=password)

        auth.login(request, user)
        return HttpResponseRedirect('/accounts/')

def login(request):
    if request.method == 'POST':
        try:
            phone = format_number(request.POST['phone'])
        except ValueError:
            return HttpResponse("invalid phone")
        password = request.POST['password']

        user = auth.authenticate(phone=phone, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/accounts/')
        else:
            return HttpResponse("invalid login")

    else:
        return render_to_response("accounts/login.html", {},
            context_instance=RequestContext(request))

@login_required
def index(request):
    return HttpResponse(request.user.name)