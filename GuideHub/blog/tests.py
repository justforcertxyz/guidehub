from django.test import TestCase, Client
from unittest import skip
from django.conf import settings
from .models import Blog
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.urls import reverse


class BlogModelTest(TestCase):
    def setUp(self):
        self.html_file_name = "test.html"

    def tearDown(self):
        file = f"{
            settings.BASE_DIR}/blog/templates/blog/entries/{self.html_file_name}"
        os.system(f"test -f {file} && rm {file}")

    def test_Blog_model_exists(self):
        blog_count = Blog.objects.count()

        self.assertEqual(blog_count, 0)

    def test___str__(self):
        title = "Test Blog"
        slug = "test_blog"
        blog = Blog.objects.create(title=title, slug=slug)

        self.assertEqual(str(blog), blog.title)

    def test_template_path(self):
        html_file = SimpleUploadedFile(name=self.html_file_name,
                                       content=b"<h1>This is some HTML</h1><p>Here is some pragraph</p>",
                                       content_type="text/html"
                                       )

        blog = Blog.objects.create(title="Some Title",
                                   slug="some_slug",
                                   html_file=html_file,
                                   )

        self.assertEqual(blog.template_path(),
                         f"blog/entries/{self.html_file_name}")


class IndexPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('blog:index')

    def test_index_page_returns_correct_response(self):
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_returns_corrent_content(self):
        response = self.client.get(self.index_url)
        self.assertContains(response, "<title>Blog")
