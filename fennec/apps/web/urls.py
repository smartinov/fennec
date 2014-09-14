from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'^dashboard', 'fennec.apps.web.views.dashboard'),
    (r'^template/notifications.popover', 'fennec.apps.web.views.template_popup_notifications')
)
