from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'^dashboard', 'fennec.apps.dashboard.views.dashboard'),
    (r'^template/notifications.popover', 'fennec.apps.dashboard.views.template_popup_notifications')
)
