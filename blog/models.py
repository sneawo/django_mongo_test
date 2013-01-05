from datetime import datetime
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse

class Tag(Document):
	title = StringField(max_length=200, required=True)

	def __unicode__(self):
		return self.title

	def posts_count(self):
		return len(Post.objects(tags=self.id))

	def posts_avg_length(self):
		return Post.objects(tags=self.id).average('text_length')

class Post(Document):
	user = ReferenceField(User, reverse_delete_rule=CASCADE)
	title = StringField(max_length=200, required=True)
	text = StringField(required=True)
	text_length = IntField()
	date_modified = DateTimeField(default=datetime.now)
	is_published = BooleanField()
	tags = ListField(ReferenceField(Tag))

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.text_length = len(self.text)
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post-detail', args=[self.id])

	def get_edit_url(self):
		return reverse('post-update', args=[self.id])

	def get_delete_url(self):
		return reverse('post-delete', args=[self.id])		