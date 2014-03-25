from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^logout/$', 'core.views.logout', name="logout"),
    url(r'^register/$', 'core.views.register',name="register"),
    url(r'^$', 'core.views.home', name="home"),
    url(r'^dashboard/$', 'core.views.dashboard', name="dashboard"),
)