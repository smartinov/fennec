from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'^diagram', 'fennec.apps.diagram.views.diagram'),
)
