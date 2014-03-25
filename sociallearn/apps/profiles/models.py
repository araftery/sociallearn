from django.db import models
from django.contrib import auth
from django.utils import timezone
from courses.models import AssignmentCompletion
from django.db.models import Sum
import profiles.utils
import urllib, hashlib

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(auth.models.User)
	phone = models.CharField(max_length=25, null=True, blank=True)
	sex = models.CharField(max_length=1, choices=[('M', 'male'), ('F', 'female')])
	courses = models.ManyToManyField('courses.Course', blank=True)
	friends = models.ManyToManyField('self', blank=True)
	# add avatar

	@property
	def name(self):
	    return '{} {}'.format(self.user.first_name, self.user.last_name)

	@property
	def active_courses(self):
		"""
		Returns QuerySet of active courses
		"""

		now = timezone.now()
		return self.courses.filter(start_date__lte=now, end_date__gte=now).order_by('title')

	@property
	def points(self):
		result = AssignmentCompletion.objects.filter(student=self).aggregate(Sum('assignment__points'))

		# note: this could break if there were more than one element in this dict
		points = result.itervalues().next()
		if points is not None:
			return points
		else:
			return 0

	@property
	def level(self):
	    return profiles.utils.get_level(self.points)

	@property
	def login_streak(self):
	    return profiles.utils.get_login_streak(self)

	@property
	def completion_streak(self):
	    return profiles.utils.get_completion_streak(self)

	def gravatar_url(self, size=200):

		size = 200
		gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
		gravatar_url += urllib.urlencode({'d': 'http://www.arayaclean.com/images/default-avatar.png', 's':str(size)})
		return gravatar_url

	def recent_activity(self, max=10):
		return self.assignmentcompletion_set.order_by('-time')[:max]
	

	def __unicode__(self):
		return '{}'.format(self.name)

class Visit(models.Model):
	time = models.DateTimeField()
	student = models.ForeignKey(Student)

	def __unicode__(self):
		return 'Visit by {} at {}'.format(self.student.name, self.time.strftime('%m/%d/%y %I:%M %p'))
		