from django.conf.urls import patterns, url

urlpatterns = patterns('courses.views',
    url(r'^dashboard/$', 'dashboard', name="dashboard"),
)