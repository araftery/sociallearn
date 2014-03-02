from django.db import models
from django.utils import timezone

class Instructor(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

	@property
	def name(self):
	    return '{} {}'.format(self.first_name, self.last_name)


class Course(models.Model):
	title = models.CharField(max_length=500)
	start_date = models.DateField()
	end_date = models.DateField()
	length = models.IntegerField(max_length=2) # length in weeks
	instructors = models.ManyToManyField(Instructor)
	url = models.URLField(max_length=2000)

	# name for sub-units (by default, 'week')
	unit_name = models.CharField(max_length=200, default='week')

	providers = (
		('EDX', 'edX'),
		)
	provider = models.CharField(max_length=3, choices=providers)

	@property
	def is_active(self):
		now = timezone.now()
		if self.start_date <= now <= self.end_date:
			return True
		else:
			return False

	def __unicode__(self):
		return self.title

class Assignment(models.Model):
	title = models.CharField(max_length=750)
	parent = models.OneToOneField('self', null=True, blank=True, related_name='child')
	week = models.ForeignKey('courses.Week', null=True, blank=True)
	url = models.URLField(max_length=2000)
	course = models.ForeignKey(Course)
	points = models.IntegerField(max_length=5)
	required = models.BooleanField(default=True)

	def __unicode__(self):
		return '{}, Week {}: {}'.format(self.course.title, self.week.number, self.title)

class AssignmentStart(models.Model):
	assignment = models.ForeignKey(Assignment)
	student = models.ForeignKey('profiles.Student')
	time = models.DateTimeField()

class AssignmentCompletion(models.Model):
	# right now, not storing the point value associated with it
	# this is fine (because it's contained in Assignment), but could cause issues
	# if the point values change after an assignment has been completed
	assignment = models.ForeignKey(Assignment)
	student = models.ForeignKey('profiles.Student')
	time = models.DateTimeField()

class Week(models.Model):
	number = models.IntegerField(max_length=2)
	course = models.ForeignKey('courses.Course')
	parent = models.OneToOneField('self', null=True, blank=True, related_name='child')

	# *brief* description, limited to 60 characters
	description = models.CharField(max_length=60, null=True, blank=True)

	def __unicode__(self):
		return '{}: {} {}'.format(self.course.title, self.course.unit_name.capitalize(), self.number)

