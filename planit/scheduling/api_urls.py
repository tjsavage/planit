from django.conf.urls import patterns, include, url


urlpatterns = patterns('planit.scheduling.api_views',
    url(r'schedule/(?P<user_id>\d+)/$', 'schedule'),
    url(r'suggestions/$', 'suggestions'),
)
