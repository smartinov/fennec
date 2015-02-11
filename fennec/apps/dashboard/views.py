from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def dashboard(request):
    return render_to_response('dashboard/dashboard/main.html', RequestContext(request))

@login_required
def template_popup_notifications(request):
    return render_to_response('dashboard/template/notifications.popover.html', RequestContext(request))

