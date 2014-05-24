from django.shortcuts import render

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext

def sign_in(request):
    state = "Please sign in below..."
    username = password = ''
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Sign in successful!"
            else:
                error = True
                state = "Your account is not active, please contact the site administrator."
        else:
            error = True
            state = "Username or password does not exist."

    return render_to_response('auth/sign-in.html',{'state':state, 'username': username, 'error':error},RequestContext(request))