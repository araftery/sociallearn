from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import auth
from django.http import Http404
import profiles.models
import core.forms
import courses.models, courses.utils, core.utils

@login_required
def home(request):
	return redirect('core:dashboard')

def logout(request):
    """Logs out user"""
    auth.logout(request)
    return redirect('core:home')

def register(request):
	if request.user.is_authenticated():
		return redirect('core:home')

	if request.method == 'POST':
		form = core.forms.RegisterForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			auth.models.User.objects.create_user(username=data.get('username'), email=data.get('email'), first_name=data.get('first_name'), last_name=data.get('last_name'), password=data.get('password'))
			user = auth.models.User.objects.get(username=data.get('username'))
			student = profiles.models.Student(phone=data.get('phone'), sex=data.get('sex'), user=user)
			student.save()

			return redirect('core:home')
	else:
		form = core.forms.RegisterForm()

	return render(request, 'registration/register.html', { 'form': form })

def dashboard(request):

	active_courses = request.user.student.active_courses
	for course in active_courses:
		course.percentage_completed = courses.utils.percentage_completed(course=course, student=request.user.student)

	# overall leaderboard
	friends_plus_self = list(request.user.student.friends.all())
	friends_plus_self.append(request.user.student)
	friends_plus_self = core.utils.rank_descending(friends_plus_self, key=lambda x: x.points)


	recent_items = courses.models.AssignmentCompletion.objects.filter(student__in=request.user.student.friends.all()).order_by('-time')[:10]


	return render(request, 'core/dashboard.html', { 'courses': active_courses, 'recent_items': recent_items, 'friends_plus_self': friends_plus_self })















	return render(request, 'courses/dashboard.html', {'courses': student_courses})


