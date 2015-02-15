from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib import auth


def sign_out(request):
    auth.logout(request)
    next = reverse('auth.sign-in')
    if request.GET and request.GET.get("next"):
        next = request.GET.get("next")

    return redirect(next)


def sign_in(request):
    state = "Please sign in below..."
    username = password = next = ''
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next')
        if next is None:
            next = '/'

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next)
            else:
                error = True
                state = "Your account is not active, please contact the site administrator."
        else:
            error = True
            state = "Username or password does not exist."
    if request.GET:
        next = request.GET.get('error') if request.GET.get('error') is not None else '/app/dashboard'

    return render_to_response('auth/sign-in.html',
                              {
                                  'state': state,
                                  'username': username,
                                  'error': error,
                                  'next': next
                              },
                              RequestContext(request))