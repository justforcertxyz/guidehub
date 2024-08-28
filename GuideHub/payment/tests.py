from django.test import TestCase
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import Order
from django.contrib.auth import get_user_model
from guide.models import Guide

User = get_user_model()


def create_guide(title, slug="some_slug", description="description", price=5, pages=1, author="", guide_pdf="", tags=""):
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


class OrderModelTest(TestCase):
    def setUp(self):
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="text/pdf")
        delete_file(self.pdf_file_name)

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_order_model_exists(self):
        order_count = Order.objects.count()

        self.assertEqual(order_count, 0)

    def test_create_order(self):
        username = "User"
        password = "Foo"
        user = User.objects.create_user(username=username, password=password)

        price = 5
        guide = create_guide(title="Some Guide",
                             price=price, guide_pdf=self.pdf)

        checkout_id = "912i34qkwhrASdj09aufd"
        order = Order.create_order(
            guide=guide, price=guide.current_price, user=user, stripe_checkout_id=checkout_id)

        order_count = Order.objects.count()
        self.assertTrue(isinstance(order, Order))
        self.assertEqual(order_count, 1)
        self.assertEqual(order, Order.objects.first())

        self.assertEqual(order.guide, guide)
        self.assertEqual(order.price, price)
        self.assertEqual(order.user, user)
        self.assertEqual(order.stripe_checkout_id, checkout_id)
