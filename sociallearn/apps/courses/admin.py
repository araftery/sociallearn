from django.contrib import admin
from courses.models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Week)