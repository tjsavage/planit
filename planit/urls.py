from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'planit.scheduling.views.home', name='home'),
    url(r'^accounts/', include('planit.accounts.urls')),
    url(r'^t/$', 'planit.accounts.views.token_login'),
    url(r'^v/$', 'planit.accounts.views.verify'),
    url(r'^api/', include('planit.scheduling.api_urls')),
    url(r'^scheduling/', include('planit.scheduling.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
