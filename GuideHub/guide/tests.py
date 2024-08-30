from django.test import TestCase, Client
from .models import Guide
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from django.utils import timezone
from django.urls import reverse
from unittest import skip
from payment.models import Order

User = get_user_model()


def create_guide(title, slug="some_slug", description="description", price=5, pages=1, author="", guide_pdf="", tags="", language="deutsch"):
    if author == "":
        author = User.objects.create_user(username="Name", password="Foo")

    if guide_pdf == "":
        guide_pdf = SimpleUploadedFile(
            name="test_guide.pdf", content=b'Tes guide', content_type="text/pdf")
    return Guide.create_guide(title=title, slug=slug,
                              description=description, current_price=price, pages=pages,
                              author=author,
                              guide_pdf=guide_pdf,
                              tags=tags,
                              )


def delete_file(file_name):
    file = f"{
        settings.GUIDE_PDF_ROOT}/{file_name}"
    os.system(f"test -f {file} && rm {file}")


class GuideModelTest(TestCase):
    def setUp(self):
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="application/pdf")
        delete_file(self.pdf_file_name)

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_guide_model_exists(self):
        guide_count = Guide.objects.count()

        self.assertEqual(guide_count, 0)

    def test_create_guide(self):
        title = "This is a Guide"
        slug = "this_is_a_guide"
        description = "Here is some text. Lorem Ipsum and os on!"
        pages = 5
        price = 4.50
        author = User.objects.create_user(
            username="Author Name", password="Foo")
        tags = 'Test, Apfel'
        language = "english"
        su1 = User.objects.create_superuser(username="su1", password="Foo")
        su2 = User.objects.create_superuser(username="su2", password="Foo")
        user = User.objects.create_user(username="Normal User", password="Foo")
        guide = Guide.create_guide(title=title, slug=slug, description=description,
                                   pages=pages, current_price=price, author=author,
                                   guide_pdf=self.pdf, tags=tags, language=language)

        guide_count = Guide.objects.count()
        self.assertTrue(isinstance(guide, Guide))
        self.assertEqual(guide_count, 1)
        self.assertEqual(guide, Guide.objects.first())

        self.assertEqual(guide.title, title)
        self.assertEqual(guide.slug, slug)
        self.assertEqual(guide.description, description)
        self.assertEqual(guide.current_price, price)
        self.assertTrue(f'{price}' in guide.price_history[0])
        self.assertEqual(guide.author, author)
        self.assertEqual(guide.guide_pdf.size, self.pdf.size)
        self.assertEqual(guide.guide_pdf.name, self.pdf.name)
        self.assertNotEqual(guide.guide_pdf.size, 0)
        self.assertEqual(guide.tags, tags)
        self.assertEqual(guide.language, language)

        self.assertEqual(guide.owned_by.get_queryset().count(), 3)
        self.assertTrue(guide.is_owned(su2))
        self.assertTrue(guide.is_owned(author))
        self.assertFalse(guide.is_owned(user))

    def test___str__(self):
        title = "Some Title"
        guide = create_guide(title=title, guide_pdf=self.pdf)
        self.assertEqual(str(guide), title)

    def test_add_owner(self):
        guide = create_guide(title="Some Title", guide_pdf=self.pdf)
        username = "User"
        user = User.objects.create_user(username=username, password="Foo")
        self.assertEqual(guide.owned_by.get_queryset().count(), 1)
        guide.add_owner(user)
        self.assertEqual(guide.owned_by.get_queryset().count(), 2)

    def test_is_owned(self):
        guide = create_guide(title="Some Title", guide_pdf=self.pdf)

        username = "User"
        user = User.objects.create_user(username=username, password="Foo")

        self.assertFalse(guide.is_owned(user))

        guide.add_owner(user)

        self.assertTrue(guide.is_owned(user))

    def test_set_price(self):
        author = User.objects.create_user(username="Name", password="Foo")
        price = 4.5
        guide = create_guide(title="Some Title", author=author,
                             guide_pdf=self.pdf, price=price)

        self.assertTrue(f'{price}' in guide.price_history[0])

        new_price = 1.25
        guide.set_price(new_price=new_price, commit=False)
        self.assertEqual(len(guide.price_history), 2)
        self.assertTrue(f'{price}' in guide.price_history[0])
        self.assertTrue(f'{new_price}' in guide.price_history[1])

        guide = Guide.objects.first()
        self.assertEqual(len(guide.price_history), 1)
        self.assertTrue(f'{price}' in guide.price_history[0])
        self.assertFalse(f'{new_price}' in guide.price_history[0])
        guide.delete()

        self.tearDown()

        guide = create_guide(title="Some Title", author=author,
                             guide_pdf=self.pdf, price=price)
        guide.set_price(new_price=new_price, commit=True)
        guide = Guide.objects.first()
        self.assertEqual(len(guide.price_history), 2)
        self.assertTrue(f'{price}' in guide.price_history[0])
        self.assertTrue(f'{new_price}' in guide.price_history[1])

    # TODO: Add image to test
    def test_has_thumbnail(self):
        guide = create_guide(title="Some Title", guide_pdf=self.pdf)
        self.assertFalse(guide.has_thumbnail())
        delete_file(self.pdf_file_name)
        guide.delete()
        img_name = "test_img.png"
        img = SimpleUploadedFile(
            name=img_name,
            content=b'Test Image',
            content_type='image/png',
        )

        guide = Guide.objects.create(title="Some Guide", slug="some_slug",
                                     description="", current_price=12, pages=1,
                                     price_history=[[]],
                                     author=User.objects.first(),
                                     guide_pdf=self.pdf,
                                     tags="",
                                     thumbnail=img,
                                     )
        self.assertTrue(guide.has_thumbnail())
        file = settings.MEDIA_ROOT / "img" / img_name
        os.system(f"test -f {file} && rm {file}")

    def test_amount_orders(self):
        guide = create_guide(title="Some Title", guide_pdf=self.pdf)

        self.assertEqual(guide.amount_orders(), 0)

        username = "User"
        password = "Foo"
        user = User.objects.create_user(username=username, password=password)

        Order.create_order(guide, guide.current_price, user, "asdas1324412")
        self.assertEqual(guide.amount_orders(), 1)

        username = "Resu"
        password = "Foo"
        user = User.objects.create_user(username=username, password=password)

        Order.create_order(guide, guide.current_price, user, "as13asd12")
        self.assertEqual(guide.amount_orders(), 2)

    # TODO: Test correct api requests
    def test_active(self):
        guide = create_guide(title="Some Title", guide_pdf=self.pdf)
        self.assertFalse(guide.is_active)

        activated = guide.activate()
        self.assertTrue(guide.is_active)
        self.assertTrue(activated)

        activated = guide.activate()
        self.assertTrue(guide.is_active)
        self.assertFalse(activated)


class IndexPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('guide:index')

    def test_index_page_returns_correct_response(self):
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'guide/index.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_returns_corrent_content(self):
        response = self.client.get(self.index_url)
        self.assertContains(response, "<title>Guides")


class DetailPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="text/pdf")

        delete_file(self.pdf_file_name)

        self.guide = create_guide(title="Some Guide", guide_pdf=self.pdf)
        self.detail_url = reverse('guide:detail', kwargs={
                                  'slug': self.guide.slug})

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_index_page_returns_correct_response(self):
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, 'guide/detail.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)


class DownloadPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="text/pdf")

        delete_file(self.pdf_file_name)

        self.guide = create_guide(title="Some Guide", guide_pdf=self.pdf)
        self.download_url = reverse('guide:download', kwargs={
                                    'slug': self.guide.slug})

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_download_page_correct_response(self):
        username = "User"
        password = "Foo"
        user = User.objects.create_user(username=username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('landing:index'))

        self.guide.add_owner(user)

        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
        self.assertEqual(
            response.headers['Content-Disposition'], 'attachment; filename="test_guide.pdf"')

        logged_in = self.client.logout()
        self.assertFalse(logged_in)

        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('landing:index'))
