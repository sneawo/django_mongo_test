from django.core.urlresolvers import reverse
from django_mongo_test.tests import MongoTestCase
from django.test.client import Client
from models import *

class BlogTest(MongoTestCase):

    def setUp(self):
        super(BlogTest, self).setUp()
        self.user = User(username='test1').save()
        self.tag = Tag(title='Test1').save()
        self.client = Client()

class PostModelTest(BlogTest):

    def test_text_length(self):
        post = Post(user=self.user, title='test', text='123', tags=[self.tag]).save()

        self.assertEqual(post.text_length, 3)

class PostListViewTest(BlogTest):

    def test_get(self):
        Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()
        Post(user=self.user, title='test', text='123', is_published=True).save()
        Post(user=self.user, title='test', text='123', tags=[self.tag]).save()

        response = self.client.get(reverse('post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 2)

    def test_filtered_get(self):
        Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()
        Post(user=self.user, title='test', text='123', is_published=True).save()
        Post(user=self.user, title='test', text='123', tags=[self.tag]).save()

        response = self.client.get(reverse('post-list') + '?tag=' + str(self.tag.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 1)


class PostCreateViewTest(BlogTest):

    def test_get(self):
        response = self.client.get(reverse('post-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_post(self):
        data = {
            'title': 'test',
            'text': 'test',
            'is_published': True,
            'tags': [self.tag.id]
        }

        response = self.client.post(reverse('post-create'), data, follow=True)

        self.assertEqual(response.status_code, 200)

        post = Post.objects.order_by('-created_date').first()
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.text, data['text'])        
        self.assertEqual(post.is_published, data['is_published'])
        self.assertEqual([tag.id for tag in post.tags], data['tags'])

class PostDetailViewTest(BlogTest):

    def test_get(self):
        post = Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()

        response = self.client.get(reverse('post-detail', args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)        

class PostUpdateViewTest(BlogTest):

    def test_get(self):
        post = Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()
        response = self.client.get(reverse('post-update', args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_post(self):
        post = Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()
        data = {
            'title': 'test1',
            'text': 'test2',
            'is_published': False,
            'tags': [self.tag.id]
        }

        response = self.client.post(reverse('post-update', args=[post.id]), data, follow=True)

        self.assertEqual(response.status_code, 200)

        post = Post.objects(id=post.id).first()
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.text, data['text'])        
        self.assertEqual(post.is_published, data['is_published'])
        self.assertEqual([tag.id for tag in post.tags], data['tags'])

class PostDeleteViewTest(BlogTest):

    def test_delete(self):
        post = Post(user=self.user, title='test', text='123', tags=[self.tag], is_published=True).save()
        self.assertEqual(Post.objects(id=post.id).count(), 1)

        response = self.client.get(reverse('post-delete', args=[post.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects(id=post.id).count(), 0)

class TagListViewTest(BlogTest):

    def test_get(self):
        Post(user=self.user, title='test', text='123', tags=[self.tag]).save()
        Post(user=self.user, title='test', text='12345', tags=[self.tag]).save()
        response = self.client.get(reverse('tag-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tag_list']), 1)
        self.assertTrue('count: 2' in response.content)
        self.assertTrue('length: 4' in response.content)
