from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moocs_with_friends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('core.urls', namespace="core")),
    url(r'^profile/', include('profiles.urls', namespace="profiles")),
    url(r'^courses/', include('courses.urls', namespace="courses")),
)