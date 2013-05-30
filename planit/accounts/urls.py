from django.conf.urls import patterns, include, url

urlpatterns = patterns('planit.accounts.views',
    # Examples:
    url(r'register/$', 'register'),
    url(r'login/$', 'login'),
    url(r'invite/$', 'invite'),
    url(r'verified/$', 'verified'),
    url(r'newly_created/$', 'newly_created'),
    url(r'$', 'index'),
)
