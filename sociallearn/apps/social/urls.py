from django.conf.urls import patterns, url

urlpatterns = patterns('social.views',
	url(r'^send_friend_request/$', 'send_friend_request', name='send_friend_request_noargs'),
	url(r'^send_friend_request/(?P<id>\d+)/$', 'send_friend_request', name='send_friend_request'),
	url(r'^friend_request_response/$', 'friend_request_response', name='friend_request_response_noargs'),
	url(r'^friend_request_response/(?P<id>\d+)/(?P<response>\w+)/$', 'friend_request_response', name='friend_request_response'),
	url(r'^hub/$', 'hub', name='hub'),
)