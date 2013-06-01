from django.conf.urls import patterns, include, url


urlpatterns = patterns('planit.scheduling.api_views',
    url(r'schedule/(?P<user_id>\d+)/$', 'schedule'),
    url(r'suggestions/$', 'suggestions'),
    url(r'meeting/(?P<meeting_id>\d+)/$', 'meeting'),
    url(r'meeting/(?P<meeting_id>\d+)/availability/$', 'meeting_availabilities'),
    url(r'meeting/(?P<meeting_id>\d+)/availability/(?P<suggested_time_id>\d+)/$', 'meeting_availability'),
)
