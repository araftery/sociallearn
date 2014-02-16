from django.conf.urls import patterns, url

urlpatterns = patterns('courses.views',
    url(r'^dashboard/$', 'dashboard', name="dashboard"),
    url(r'^assignment_complete/(?P<id>\d+)/$', 'assignment_complete', name="assignment_complete"),
    url(r'^assignment_complete/$', 'assignment_complete', name="assignment_complete_noargs"),
    url(r'^assignment_incomplete/(?P<id>\d+)/$', 'assignment_incomplete', name="assignment_incomplete"),
    url(r'^assignment_incomplete/$', 'assignment_incomplete', name="assignment_incomplete_noargs"),
    url(r'^add_course/$', 'add_course', name="add_course"),
    url(r'^add_course/(?P<id>\d+)/$', 'add_course_input_progress', name="add_course_input_progress"),
)