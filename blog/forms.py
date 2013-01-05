from bson import ObjectId
from django import forms
from models import *

class PostForm(forms.Form):
	title = forms.CharField(max_length=255)
	text = forms.CharField(widget=forms.widgets.Textarea())
	is_published = forms.BooleanField(required=False)
	tags = forms.MultipleChoiceField(
		widget=forms.widgets.CheckboxSelectMultiple(), 
		required=False)

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['tags'].choices = [(tag.id, tag.title) for tag in Tag.objects]
		if self.instance:
			self.fields['title'].initial = self.instance.title
			self.fields['text'].initial = self.instance.text
			self.fields['is_published'].initial = self.instance.is_published		
			self.fields['tags'].initial = [tag.id for tag in self.instance.tags]


	def save(self, commit=True):
		post = self.instance if self.instance else Post()
		post.title = self.cleaned_data['title']
		post.text = self.cleaned_data['text']
		post.is_published = self.cleaned_data['is_published']
		post.tags = Tag.objects(id__in=self.cleaned_data['tags'])
		if commit:
			post.save()

		return post