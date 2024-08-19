from django.test import TestCase
from .models import Guide
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from django.utils import timezone

User = get_user_model()


def create_guide(title, slug="slug", description="description", price=0, pages=1, author="", guide_pdf="", tags=""):
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


class GuideModelTest(TestCase):
    def setUp(self):
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="text/pdf")
        file = f"{
            settings.BASE_DIR}/guide/doc/{self.pdf_file_name}"
        os.system(f"test -f {file} && rm {file}")

    def tearDown(self):
        file = f"{
            settings.BASE_DIR}/guide/doc/{self.pdf_file_name}"
        os.system(f"test -f {file} && rm {file}")

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
        su1 = User.objects.create_superuser(username="su1", password="Foo")
        su2 = User.objects.create_superuser(username="su2", password="Foo")
        user = User.objects.create_user(username="Normal User", password="Foo")
        guide = Guide.create_guide(title=title, slug=slug, description=description,
                                   pages=pages, current_price=price, author=author, guide_pdf=self.pdf, tags=tags)

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
        self.assertEqual(guide.guide_pdf.name, f"guide/doc/{self.pdf.name}")
        self.assertNotEqual(guide.guide_pdf.size, 0)
        self.assertEqual(guide.tags, tags)

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
