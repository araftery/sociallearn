from django import forms
import courses.models
from django.utils import timezone

class CoursesForm(forms.Form):
	course = forms.ModelChoiceField(queryset=courses.models.Course.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).order_by('title'), required=True)

	def __init__(self, user, *args, **kwargs):
		super(CoursesForm, self).__init__(*args, **kwargs)
		self.fields['course'].queryset = courses.models.Course.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).exclude(id__in=user.student.courses.all()).order_by('title')