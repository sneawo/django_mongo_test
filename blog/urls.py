from django.conf.urls import patterns, url
from views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, TagListView

urlpatterns = patterns('',
	url(r'^tags/$', TagListView.as_view(), name='tag-list'),
	url(r'^add/$', PostCreateView.as_view(), name='post-create'),
	url(r'^(?P<pk>[\w\d]+)/$', PostDetailView.as_view(), name='post-detail'),
	url(r'^(?P<pk>[\w\d]+)/edit/$', PostUpdateView.as_view(), name='post-update'),
	url(r'^(?P<pk>[\w\d]+)/delete/$', PostDeleteView.as_view(), name='post-delete'),
)
