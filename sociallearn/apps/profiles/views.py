from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils import timezone
from django.contrib import auth
from django.http import Http404
import profiles.utils, profiles.models
import core.utils
import courses.utils
from dateutil.relativedelta import relativedelta

# Create your views here.

@login_required
def profile(request, username):
	try:
		user = auth.models.User.objects.get(username=username)
		student = user.student
	except auth.models.User.DoesNotExist:
		raise Http404()

	next_level = user.student.level + 1
	points_to_next_level = profiles.utils.get_points(next_level) - user.student.points

	if request.user.student.friends.filter(id=student.id):
		friends_status = 'friend'
	elif request.user.student.friendrequests_out.filter(target=student, accepted=None):
		friends_status = 'requested_out'
	elif request.user.student.friendrequests_in.filter(requester=student, accepted=None):
		friends_status = 'requested_in'
	else:
		friends_status = None

	activity = student.recent_activity()
	active_courses = student.active_courses
	for course in active_courses:
		course.percentage_completed = courses.utils.percentage_completed(course, student)

	friends = student.friends.all().order_by('user__last_name', 'user__first_name')


	heatmap_start = timezone.now() - relativedelta(months=3)

	return render(request, 'profiles/profile.html', { 'heatmap_start': heatmap_start, 'student': student, 'friends': friends, 'courses':active_courses, 'next_level': next_level, 'activity': activity, 'points_to_next_level': points_to_next_level, 'friends_status': friends_status })

@login_required
def me(request):
	size = 200
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(request.user.email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d': 'http://www.arayaclean.com/images/default-avatar.png', 's':str(size)})
	return render(request, 'profiles/me.html', { 'gravatar_url': gravatar_url })