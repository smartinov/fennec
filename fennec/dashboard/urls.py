from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'^dashboard', 'fennec.dashboard.views.dashboard'),
    (r'^template/notifications.popover', 'fennec.dashboard.views.template_popup_notifications')
)
