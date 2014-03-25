from django import forms
from django.utils import timezone
from django.contrib import auth
import django.core.exceptions as exceptions

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	email = forms.CharField(max_length=1000)
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=50)
	password_confirm = forms.CharField(max_length=50)
	phone = forms.CharField(max_length=25, required=False)
	sex = forms.CharField(max_length=1)


	def clean_email(self):
		email = self.cleaned_data.get('email')
		user = auth.models.User.objects.filter(email=email)

		if user:
			raise exceptions.ValidationError('A user with this email address already exists.', code='invalid')
		
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		user = auth.models.User.objects.filter(username=username)

		if user:
			raise exceptions.ValidationError('A user with this username already exists.', code='invalid')
		
		return username



	def clean(self):
		password = self.cleaned_data.get('password')
		password_confirm = self.cleaned_data.get('password_confirm')

		if password != password_confirm:
			raise exceptions.ValidationError('The password and confirm fields must match.', code='invalid')

		return self.cleaned_data