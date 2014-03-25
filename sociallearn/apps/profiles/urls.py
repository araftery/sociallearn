from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
	url(r'^profile/(?P<username>\w+)/$', 'profile', name='profile'),
	url(r'^me/$', 'me', name='me'),
)