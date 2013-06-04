from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.conf import settings

from planit.accounts.models import UserProfile, LoginToken, VerificationToken, generate_login_token
from phonenumber_field.phonenumber import to_python

from planit.accounts.sms import send_verification, send_message


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
            return render_to_response('accounts/register.html', {
                "error": "Invalid phone number"
            }, context_instance=RequestContext(request))

        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)

        if password != password2:
            return render_to_response('accounts/register.html', {
                "error": "Passwords don't match"
            }, context_instance=RequestContext(request))
            
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        next = request.POST.get("next", None)

        if UserProfile.objects.filter(phone=phone).count():
            user = UserProfile.objects.get(phone=phone)
            user.newly_created = True
            user.set_password("nopassword")
            user.save()

            token = generate_login_token(user.phone, next="/accounts/")
            send_message(user.phone, "Hey from GoGroup! You can log in to reset your password here: http://%s/t/?token=%s" % (settings.BASE_URL, token.token))

            return render_to_response('accounts/register.html', {
                    "error": "An account with that phone number has already been created. We've texted you a link to login."
                }, context_instance=RequestContext(request))
        user = UserProfile.objects.create(phone, password=password, name=name)
        if not user:
            return HttpResponse("error")

        user.name = name
        user.email = email
        user.set_password(password)

        user.save()
        #send_verification(user)

        #user = auth.authenticate(phone=user.phone, password=password)
        
        user.backend = 'django.contrib.auth.backends.ModelBackend'
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
            return render_to_response("accounts/login.html", 
                {"error": "Sorry, incorrect phone number or password"},
            context_instance=RequestContext(request))

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
            if user.newly_created:
                user = auth.authenticate(phone=user.phone, password="nopassword")
                auth.login(request, user)
                return HttpResponseRedirect("/accounts/newly_created/?next=%s" % login_token.next_url)
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
                if login_token.next_url:
                    return HttpResponseRedirect("%s" % login_token.next_url)
                else:
                    return HttpResponseRedirect("/accounts/")
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect("/accounts/register/?phone=%s&next=%s" % (login_token.phone, login_token.next_url))

@login_required
def newly_created(request):
    if request.method == 'POST':
        password = request.POST["password"]
        name = request.POST["name"]
        user = request.user
        user.name = name
        user.newly_created = False
        user.set_password(password)
        user.save()

        return HttpResponseRedirect("%s" % request.POST.get("next", "/"))

    return render_to_response("accounts/newly_created.html", 
                            {"name": request.user.name,
                            "next": request.GET.get("next")},
                            context_instance=RequestContext(request))



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

        return HttpResponse("%s/t/?token=%s" % (request.get_host(), login_token.token))

    else:
        return render_to_response("accounts/invite.html", {},
            context_instance=RequestContext(request))


@login_required
def index(request):
    return render_to_response("accounts/dashboard.html", {},
        context_instance=RequestContext(request))