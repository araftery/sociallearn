from django.shortcuts import render, redirect
import urllib, hashlib

# Create your views here.

def profile(request):

	return render(request, 'profiles/profile.html', { })

def me(request):
	size = 200
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(request.user.email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d': 'http://www.arayaclean.com/images/default-avatar.png', 's':str(size)})
	return render(request, 'profiles/me.html', { 'gravatar_url': gravatar_url })