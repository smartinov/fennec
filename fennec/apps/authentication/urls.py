from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^sign-in/$', 'fennec.apps.authentication.views.sign_in', name="auth.sign-in"),
    url(r'^sign-out/$', 'fennec.apps.authentication.views.sign_out',name="auth.sign-out"),
)
