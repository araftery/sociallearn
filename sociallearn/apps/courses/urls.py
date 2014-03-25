from django.conf.urls import patterns, url

urlpatterns = patterns('courses.views',
    url(r'^course/(?P<course_id>\d+)/$', 'course', name="course"),
    url(r'^dashboard/$', 'dashboard', name="dashboard"),
    url(r'^assignment_complete/(?P<id>\d+)/$', 'assignment_complete', name="assignment_complete"),
    url(r'^assignment_complete/$', 'assignment_complete', name="assignment_complete_noargs"),
    url(r'^add_course/$', 'add_course', name="add_course"),
    url(r'^level_progress/$', 'level_progress', name="level_progress"),
    #url(r'^add_course/(?P<id>\d+)/$', 'add_course_input_progress', name="add_course_input_progress"),
    url(r'^assignment_completions_data/(?P<username>\w+)/(?P<last_three>\w+)/$', 'assignment_completions_data', name="assignment_completions_data_nomonth"),
    url(r'^assignment_completions_data/(?P<username>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<last_three>\w+)$', 'assignment_completions_data', name="assignment_completions_data"),
    url(r'^assignment_completions_data/$', 'assignment_completions_data', name="assignment_completions_data_noargs"),

)