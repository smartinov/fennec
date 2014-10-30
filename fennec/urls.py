from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url="/app/dashboard")),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('fennec.services.urls'), name="api"),
    url(r'^auth/', include('fennec.authentication.urls')),
    url(r'^app/', include('fennec.dashboard.urls')),
    url(r'^api/authentication/', include('rest_framework.urls', namespace='rest_framework')),
)
