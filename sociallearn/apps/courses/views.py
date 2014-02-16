from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils import timezone
import courses.utils
import core.utils
import courses.models
import courses.forms

@login_required
def add_course(request):
	now = timezone.now()
	form = courses.forms.CoursesForm(request.user)
	if request.POST:
		form = courses.forms.CoursesForm(request.user, request.POST)
		if form.is_valid():
			course = form.cleaned_data.get('course')
			return redirect('courses:add_course_input_progress', id=course.id)
	
	return render(request, 'courses/add_course.html', { 'form': form })

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

	course_assignments_roots = course.assignment_set.filter(parent=None).order_by('week')
	weeks = []
	week_in = None
	for root in course_assignments_roots:
		assignments = []
		for assignment in courses.utils.assignment_tree(root):
			if assignment.assignmentcompletion_set.filter(student=request.user.student):
				assignment.done = True
			else:
				assignment.done = False
			assignments.append(assignment)


		week = {'num': root.week, 'assignments': assignments}
		weeks.append(week)

	print weeks

	if request.method == 'POST':
		request.user.student.courses.add(course)
		
		for week in weeks:
			for assignment in week['assignments']:
				status = request.POST.get('assignment{}'.format(assignment.id), False)
				if status:
					assignment_completion = courses.models.AssignmentCompletion(assignment=assignment, student=request.user.student, time=time)
					assignment_completion.save()
		
		return redirect('courses:dashboard')


	return render(request, 'courses/add_course_input_progress.html', { 'course': course, 'courses': courses, 'weeks': weeks })

@login_required
def dashboard(request):
	"""
	Courses dashboard
	"""

	# get courses and first course
	student_courses = request.user.student.active_courses
	course = student_courses.first()
	if course is not None:
		course_assignments_roots = course.assignment_set.filter(parent=None).order_by('week')
		weeks = []
		week_in = None
		for root in course_assignments_roots:
			assignments = []
			for assignment in courses.utils.assignment_tree(root):
				if assignment.assignmentcompletion_set.filter(student=request.user.student):
					assignment.done = True
				else:
					assignment.done = False
				assignments.append(assignment)

			# get week completed percentage
			week_assignments = courses.models.Assignment.objects.filter(week=root.week, course=course)
			week_assignment_completions = courses.models.AssignmentCompletion.objects.filter(assignment__course=course, assignment__week=root.week, student=request.user.student)
			if week_assignments:
				percentage = int(float(len(week_assignment_completions)/float(len(week_assignments))) * 100)
			else:
				percentage = 0

			if week_in is None and percentage != 100:
				week_in = root.week

			week = {'num': root.week, 'assignments': assignments, 'percentage': percentage}
			weeks.append(week)
		
		return render(request, 'courses/dashboard.html', { 'course': course, 'courses': courses, 'weeks': weeks, 'week_in': week_in})
	else:
		return render(request, 'courses/dashboard.html')

@login_required
@core.utils.json_response
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
	week_assignments = courses.models.Assignment.objects.filter(week=assignment.week, course=assignment.course)
	week_assignment_completions = courses.models.AssignmentCompletion.objects.filter(assignment__course=assignment.course, assignment__week=assignment.week, student=request.user.student)
	if week_assignments:
		percentage = int(float(len(week_assignment_completions)/float(len(week_assignments))) * 100)
	else:
		percentage = 0

	return {'week': assignment.week, 'course': assignment.course.id, 'percentage': percentage}


@login_required
@core.utils.json_response
def assignment_incomplete(request, id):
	try:
		id = int(id)
		assignment = courses.models.Assignment.objects.get(id=id)
	except:
		return {'error': 'Sorry, an error occurred.'}

	courses.models.AssignmentCompletion.objects.filter(assignment=assignment, student=request.user.student).delete()

	# get week completed percentage
	week_assignments = courses.models.Assignment.objects.filter(week=assignment.week, course=assignment.course)
	week_assignment_completions = courses.models.AssignmentCompletion.objects.filter(assignment__course=assignment.course, assignment__week=assignment.week, student=request.user.student)

	if week_assignments:
		percentage = int(float(len(week_assignment_completions)/float(len(week_assignments))) * 100)
	else:
		percentage = 0

	return {'week': assignment.week, 'course': assignment.course.id, 'percentage': percentage}



