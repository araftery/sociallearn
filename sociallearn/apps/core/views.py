from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import auth

@login_required
def home(request):
	return redirect('courses:dashboard')


def logout(request):
    """Logs out user"""
    auth.logout(request)
    return redirect('core:home')