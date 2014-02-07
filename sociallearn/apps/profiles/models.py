from django.db import models
from django.contrib import auth
from django.utils import timezone

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(auth.models.User)
	courses = models.ManyToManyField('courses.Course')

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

	def __unicode__(self):
		return '{}'.format(self.name)



