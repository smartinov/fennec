from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^sign-in/$', 'fennec.apps.auth.views.sign_in'),
    url(r'^sign-out/$','fennec.apps.auth.views.sign_out',name="auth.sign-out"),
)
