from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
import urllib, hashlib
from django.utils import timezone
from django.contrib import auth
from django.http import Http404
import core.utils
import profiles.models
import courses.models
import social.models
import profiles.utils
import operator

@login_required
def hub(request):
	active_courses = request.user.student.active_courses
	for course in active_courses:
		people_in_course = []
		points_earned = profiles.utils.get_points_in_course(student=request.user.student, course=course)
		people_in_course.append({'person': request.user.student, 'name': request.user.student.name, 'points': points_earned})
		friends_taking_course = request.user.student.friends.filter(courses=course)
		for friend in friends_taking_course:
			people_in_course.append({ 'person': friend, 'name': friend.name, 'points': profiles.utils.get_points_in_course(student=friend, course=course )})
		people_in_course.sort(key=lambda x: (x['points'], x['name']), reverse=True)
		course.leaderboard = people_in_course


	# overall leaderboard
	friends_plus_self = list(request.user.student.friends.all())
	friends_plus_self.append(request.user.student)
	friends_plus_self.sort(key=lambda x: x.points, reverse=True)


	recent_items = courses.models.AssignmentCompletion.objects.filter(student__in=request.user.student.friends.all()).order_by('-time')[:10]


	return render(request, 'social/hub.html', { 'active_courses': active_courses, 'recent_items': recent_items, 'friends_plus_self': friends_plus_self })


@login_required
@core.utils.json_response
def send_friend_request(request, id):
	try:
		target = profiles.models.Student.objects.get(id=id)
	except profiles.models.Student.DoesNotExist:
		raise Http404()

	requester = request.user.student

	if requester == target:
		return { 'result': 'failure' }

	now = timezone.now()

	friend_request = None
	if not social.models.FriendRequest.objects.filter(requester=requester, target=target):
		friend_request = social.models.FriendRequest(requester=requester, target=target, time_requested=now)
		friend_request.save()

	if friend_request:
		return { 'result': 'success' }
	else:
		return { 'result': 'failure' }


@core.utils.json_response
@login_required
def friend_request_response(request, response, id):
	try:
		friend_request = social.models.FriendRequest.objects.get(id=id)
		if friend_request.target != request.user.student or friend_request.accepted is not None:
			return {'status': 'failure'}
	except social.models.FriendRequest.DoesNotExist:
		return {'status': 'failure'}

	if response == 'accept':
		accepted = True
	elif response == 'reject':
		accepted = False
	else:
		return {'status': 'failure'}

	friend_request.accepted = accepted
	friend_request.save()

	return {'status':'success'}
