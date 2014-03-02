import django.utils.timezone, datetime
import courses.models

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

def get_login_streak(student):
	"""
	Gets the current login streak in days for a given student.
	"""
	now = django.utils.timezone.now()
	visit = student.visit_set.filter(time__day=now.day)
	streak = 0
	while visit:
		streak += 1
		time = now - datetime.timedelta(streak)
		visit = student.visit_set.filter(time__day=time.day)
	return streak

def get_completion_streak(student):
	"""
	Gets the current completion streak in days for a given student.
	"""
	now = django.utils.timezone.now()
	completion = student.assignmentcompletion_set.filter(time__day=now.day)
	streak = 0
	while completion:
		streak += 1
		time = now - datetime.timedelta(streak)
		completion = student.assignmentcompletion_set.filter(time__day=time.day)
	return streak