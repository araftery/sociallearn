from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils import timezone
import courses.utils
from core.utils import json_response
import courses.models
import courses.forms
import courses.utils
import json
import profiles.utils
import calendar
from itertools import chain
import datetime
import pytz

@login_required
def add_course(request):
	now = timezone.now()
	form = courses.forms.CoursesForm(request.user)
	if request.POST:
		form = courses.forms.CoursesForm(request.user, request.POST)
		if form.is_valid():
			course = form.cleaned_data.get('course')
			request.user.student.courses.add(course)
			return redirect('courses:course', course_id=course.id)
	
	return render(request, 'courses/add_course.html', { 'form': form })
'''
@login_required
def add_course_input_progress(request, id):
	"""
	Add course step 2: input progress to date
	"""

	try:
		course = courses.models.Course.objects.get(id=id)
		
		# make sure the student isn't already taking the course
		if course in request.user.student.courses.all():
			raise Http404()

	except DoesNotExist:
		Http404()

	time = timezone.now()

	root_week = course.week_set.filter(parent=None).first()
	weeks = courses.utils.get_tree(root_week)
	week_in = None

	weeks_with_assignments = []

	for week in weeks:
		assignments = []
		root = week.assignment_set.filter(parent=None).first()
		for assignment in courses.utils.get_tree(root):
			if assignment.assignmentcompletion_set.filter(student=request.user.student):
				assignment.done = True
			else:
				assignment.done = False
			assignments.append(assignment)

		weeks_with_assignments.append({'num': week.number, 'assignments': assignments})


	if request.method == 'POST':
		request.user.student.courses.add(course)
		
		for week in weeks:
			for assignment in week['assignments']:
				status = request.POST.get('assignment{}'.format(assignment.id), False)
				if status:
					assignment_completion = courses.models.AssignmentCompletion(assignment=assignment, student=request.user.student, time=time)
					assignment_completion.save()
		
		return redirect('courses:dashboard')


	return render(request, 'courses/add_course_input_progress.html', { 'course': course, 'courses': courses, 'weeks': weeks_with_assignments })
'''

@login_required
def course(request, course_id):
	"""
	Course page
	"""

	# get course. NOTE: this allows only active courses to be viewed
	student_courses = request.user.student.active_courses
	try:
		course = student_courses.get(id=course_id)
	except:
		return Http404()
	
	root_week = course.week_set.filter(parent=None).first()
	weeks = courses.utils.get_tree(root_week)
	week_in = None

	weeks_with_assignments = []

	for week in weeks:
		assignments = []
		root = week.assignment_set.filter(parent=None).first()
		if root:
			for assignment in courses.utils.get_tree(root):
				if assignment.assignmentcompletion_set.filter(student=request.user.student):
					assignment.done = True
				else:
					assignment.done = False
				assignments.append(assignment)


		# get week completed percentage
		week_assignments = courses.models.Assignment.objects.filter(week=week, course=course, required=True)
		week_assignment_completions = courses.models.AssignmentCompletion.objects.filter(assignment__course=course, assignment__week=week, assignment__required=True, student=request.user.student)
		if week_assignments:
			percentage = int(float(len(week_assignment_completions)/float(len(week_assignments))) * 100)
		else:
			percentage = 0

		if week_in is None and percentage != 100:
			week_in = week.number

		weeks_with_assignments.append({'num': week.number, 'assignments': assignments, 'percentage': percentage, 'description': week.description})

	for week in weeks_with_assignments:
		if (week_in == week['num'] or week['percentage']) and week['percentage'] != 100:
			week['show_progress_bar'] = True
		else:
			week['show_progress_bar'] = False
	# also, get a flat (1d) dict of assignment ids -> assignment info
	assignments = {}
	for week in weeks_with_assignments:
		for assignment in week['assignments']:
			assignments[assignment.id] = {
				'title': assignment.title,
			}
	# convert the assignments dict to json
	assignments_json = json.dumps(assignments)
	
	return render(request, 'courses/course.html', { 'course': course, 'courses': student_courses, 'weeks': weeks_with_assignments, 'week_in': week_in, 'assignments_json': assignments_json})


@login_required
def dashboard(request):
	"""
	Courses dashboard page
	"""

	student_courses = request.user.student.active_courses
	for course in student_courses:
		course.percentage_completed = courses.utils.percentage_completed(course=course, student=request.user.student)

	return render(request, 'courses/dashboard.html', {'courses': student_courses})

@login_required
from core.utils import json_response
def assignment_complete(request, id):
	try:
		id = int(id)
		assignment = courses.models.Assignment.objects.get(id=id)
	except:
		return {'error': 'Sorry, an error occurred.'}

	time = timezone.now()
	if not courses.models.AssignmentCompletion.objects.filter(assignment=assignment, student=request.user.student):
		assignment_completion = courses.models.AssignmentCompletion(assignment=assignment, student=request.user.student, time=time)
		assignment_completion.save()

	# get week completed percentage
	week_assignments = courses.models.Assignment.objects.filter(week=assignment.week, course=assignment.course, required=True)
	week_assignment_completions = courses.models.AssignmentCompletion.objects.filter(assignment__course=assignment.course, assignment__week=assignment.week, assignment__required=True, student=request.user.student)
	if week_assignments:
		percentage = int(float(len(week_assignment_completions)/float(len(week_assignments))) * 100)
	else:
		percentage = 0

	return {'week': assignment.week.number, 'course': assignment.course.id, 'percentage': percentage, 'points': assignment.points }



@login_required
from core.utils import json_response
def level_progress(request):
	points = request.user.student.points
	level = request.user.student.level
	level_progress = int(((float(points) - profiles.utils.get_points(level)) / profiles.utils.get_points(level + 1)) * 100)

	return { 'level_progress': level_progress, 'user_level': request.user.student.level }


@login_required
from core.utils import json_response
def assignment_completions_data(request, month=None, year=None):
	if (month is None or year is None):
		now = timezone.now()
		month = now.month
		year = now.year

	try:
		month = int(month)
		year = int(year)
	except:
		return Http404()

	cal = calendar.Calendar()

	month_dates = [i for i in chain.from_iterable(cal.monthdatescalendar(year,month)) if i.month == month]
	
	data = {}

	for date in month_dates:
		num_completions = courses.models.AssignmentCompletion.objects.filter(student=request.user.student, time__year=date.year, time__month=date.month, time__day=date.day).count()
		
		date = datetime.datetime.combine(date, datetime.datetime.min.time())

		if num_completions != 0:
			data[calendar.timegm(date.replace(tzinfo=pytz.timezone('EST')).utctimetuple())] = num_completions

	return data




