from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

from planit.accounts.models import UserProfile, LoginToken, VerificationToken, generate_login_token
from phonenumber_field.phonenumber import to_python

from planit.accounts.sms import send_verification


def register(request):
    if request.method == 'GET':
        phone = request.GET.get("phone", "")
        next_url = request.GET.get("next", "")
        return render_to_response('accounts/register.html', {
                "phone": phone,
                "next": next_url
            },
            context_instance=RequestContext(request))
    elif request.method == 'POST':
        try:
            phone = request.POST.get("phone", None)
        except ValueError:
            return HttpResponse("Invalid phone")

        password = request.POST.get("password", None)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        next = request.POST.get("next", None)

        if UserProfile.objects.filter(phone=phone).count():
            return HttpResponse("already created")
        user = UserProfile.objects.create(phone, password)
        if not user:
            return HttpResponse("error")

        user.name = name
        user.email = email

        user.save()

        #send_verification(user)

        user = auth.authenticate(phone=user.phone, password=password)

        auth.login(request, user)
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/accounts/")

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
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

def token_login(request):
    if request.method == 'GET':
        token = request.GET['token']

        try:
            login_token = LoginToken.objects.get(token=token)
        except LoginToken.DoesNotExist:
            return HttpResponse("invalid token")

        try:
            user = UserProfile.objects.get(phone=login_token.phone)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect("/accounts/register/?phone=%s&next=%s" % (login_token.phone, login_token.next_url))

def verify(request):
    if request.method == 'GET':
        token = request.GET["token"]

        try:
            verification_token = VerificationToken.objects.get(token=token)
        except VerificationToken.DoesNotExist:
            return HttpResponse("invalid token")

        user = verification_token.user
        user.phone_verified = True
        user.save()

        return HttpResponseRedirect("/accounts/verified/")

def verified(request):
    return HttpResponse("Verified!")



def invite(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        login_token = generate_login_token(phone, next="/junk/")

        return HttpResponse("http://localhost:8000/t/?token=%s" % login_token.token)

    else:
        return render_to_response("accounts/invite.html", {},
            context_instance=RequestContext(request))


@login_required
def index(request):
    return render_to_response("accounts/dashboard.html", {},
        context_instance=RequestContext(request))