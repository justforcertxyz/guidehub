from django.test import TestCase, Client
from unittest import skip
from django.conf import settings
from .models import Blog


class BlogModelTest(TestCase):
    def test_Blog_model_exists(self):
        blog_count = Blog.objects.count()

        self.assertEqual(blog_count, 0)

    def test___str__(self):
        title = "Test Blog"
        slug = "test_blog"
        blog = Blog.objects.create(title=title, slug=slug)

        self.assertEqual(str(blog), blog.title)
