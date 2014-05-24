from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'^dashboard', 'fennec.apps.web.views.dashboard'),
)
