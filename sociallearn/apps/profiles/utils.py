import django.utils.timezone, datetime
import courses.models
from django.db.models import Sum

def get_level(points):
	"""
	Converts points to a level, using the formula level = sqrt(points/220)
	"""
	return int((points/220.0) ** .5)

def get_points(level):
	"""
	Converts level to points, using the formula points = (level^2 * 220)
	"""
	return int((level ** 2) * 220)

def get_points_in_course(student, course):
	"""
	Gets the points earned by a user in a particular course
	"""
	points_result = courses.models.AssignmentCompletion.objects.filter(assignment__course=course, student=student).aggregate(Sum('assignment__points'))

	# note: this could break if there were more than one element in this dict
	total_points = points_result.itervalues().next()
	if total_points is None:
		total_points = 0

	return int(total_points)

def get_login_streak(student):
	"""
	Gets the current login streak in days for a given student.
	"""
	yesterday = django.utils.timezone.now() - datetime.timedelta(1)
	visit = student.visit_set.filter(time__day=yesterday.day)
	streak = 0
	while visit:
		streak += 1
		time = yesterday - datetime.timedelta(streak)
		visit = student.visit_set.filter(time__day=time.day)
	
	# add 1 if you've visited today
	now = django.utils.timezone.now()
	if student.visit_set.filter(time__day=now.day):
		streak += 1

	return streak

def get_completion_streak(student):
	"""
	Gets the current completion streak in days for a given student.
	"""
	yesterday = django.utils.timezone.now() - datetime.timedelta(1)
	completion = student.assignmentcompletion_set.filter(time__day=yesterday.day)
	streak = 0
	while completion:
		streak += 1
		time = yesterday - datetime.timedelta(streak)
		completion = student.assignmentcompletion_set.filter(time__day=time.day)
	
	# add 1 if you've completed an assignment today
	now = django.utils.timezone.now()
	if student.assignmentcompletion_set.filter(time__day=now.day):
		streak += 1
	
	return streak