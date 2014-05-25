from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render_to_response('web/dashboard.html')
