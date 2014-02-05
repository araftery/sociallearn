from django.db import models

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
	providers = (
		('EDX', 'edX'),
		)
	provider = models.CharField(max_length=3, choices=providers)

	def __unicode__(self):
		return self.title


class Assignment(models.Model):
	title = models.CharField(max_length=750)
	parent = models.OneToOneField('self', null=True, blank=True, related_name='child')
	url = models.URLField(max_length=2000)
	course = models.ForeignKey(Course)
	week = models.IntegerField(max_length=2)

	def __unicode__(self):
		return '{}, Week {}: {}'.format(self.course.title, self.week, self.title)

class AssignmentStart(models.Model):
	assignment = models.ForeignKey(Assignment)
	student = models.ForeignKey('profiles.Student')
	time = models.DateTimeField()

class AssignmentCompletion(models.Model):
	assignment = models.ForeignKey(Assignment)
	student = models.ForeignKey('profiles.Student')
	time = models.DateTimeField()
