from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^sign-in/$', 'fennec.apps.auth.views.sign_in'),
)
