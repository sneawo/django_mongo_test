from django.conf.urls import patterns, include, url
from django.conf import settings
from blog.views import PostListView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='post-list'),
    url(r'^post/', include('blog.urls'))
)

if settings.DEBUG:
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()

	urlpatterns += patterns('',
			url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
				'document_root': settings.MEDIA_ROOT,
			}),
	   )
