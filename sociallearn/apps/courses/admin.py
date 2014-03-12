from django.contrib import admin
from courses.models import *
from django import forms

# Register your models here.

class AssignmentForm(forms.ModelForm):

	class Meta:
		model = Assignment

	def clean(self):
		week = self.cleaned_data.get('week')
		parent = self.cleaned_data.get('parent')
		if not week and parent:
			self.cleaned_data['week'] = parent.week

		return self.cleaned_data

	def __init__(self, *args, **kwargs):
		super(AssignmentForm, self).__init__(*args, **kwargs) 
		self.fields['parent'].queryset = Assignment.objects.all().order_by('-id')



class AssignmentAdmin(admin.ModelAdmin):
	form = AssignmentForm

admin.site.register(Course)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Week)
admin.site.register(Instructor)
admin.site.register(AssignmentCompletion)