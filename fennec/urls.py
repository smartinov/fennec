from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin
admin.autodiscover()

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^$',RedirectView.as_view(url="/app/dashboard")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/',include('fennec.apps.rest.urls')),
    url(r'^auth/',include('fennec.apps.auth.urls')),
    url(r'^app/',include('fennec.apps.web.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
