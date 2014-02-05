from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

@login_required
def dashboard(request):
	# get courses and first course
	courses = request.user.student.active_courses
	course = courses.first()

	return render(request, 'courses/dashboard.html', { 'course': course, 'courses': courses})