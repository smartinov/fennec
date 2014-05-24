from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/',include('fennec.apps.rest.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
