from django.db import models
from django.contrib import auth
from django.utils import timezone

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(auth.models.User)
	phone = models.CharField(max_length=25, null=True, blank=True)
	sex = models.CharField(max_length=1, choices=[('M', 'male'), ('F', 'female')])
	courses = models.ManyToManyField('courses.Course')
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

	def __unicode__(self):
		return '{}'.format(self.name)



