from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_authenticated():
        return render_to_response('web/dashboard.html')
    else:
        return redirect('/auth/sign-in?continueTo=%s' % request.path)
