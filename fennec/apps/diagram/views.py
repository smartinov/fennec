from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def diagram(request):
    return render_to_response('diagram/diagram/main.html', RequestContext(request))



