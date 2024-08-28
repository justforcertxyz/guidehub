from django.test import TestCase, Client
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import Order
from django.contrib.auth import get_user_model
from guide.models import Guide
from django.urls import reverse
from unittest import skip

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


class CheckoutPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        username = "User"
        password = "foo"
        self.user = User.objects.create_user(
            username=username, password=password)
        self.logged_in = self.client.login(
            username=username, password=password)
        self.dashboard_url = reverse('landing:dashboard')
        self.checkout_url = reverse('payment:checkout')
        self.pdf_file_name = "test_guide.pdf"
        self.pdf = SimpleUploadedFile(
            name=self.pdf_file_name, content=b'Test guide', content_type="text/pdf")

        delete_file(self.pdf_file_name)

        self.guide = create_guide(title="Some Guide", guide_pdf=self.pdf)
        self.query_string = f"?guide={self.guide.slug}"

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_checkout_page_returns_correct_response(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(self.checkout_url + self.query_string)
        self.assertTemplateUsed(response, 'payment/checkout.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            self.checkout_url + "?guide=this_should_fail")
        self.assertEqual(response.status_code, 404)

        self.logged_in = self.client.logout()
        self.assertFalse(self.logged_in)
        response = self.client.get(self.checkout_url + self.query_string)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "landing:login") + "?next=" + self.checkout_url + self.query_string)

    def test_checkout_page_returns_corrent_content(self):
        response = self.client.get(self.checkout_url + self.query_string)
        self.assertContains(response, "<title>Checkout")
        self.assertContains(response, '<form')
        self.assertContains(response, '<button')
        self.assertContains(response,
                            f' href="{self.checkout_url + self.query_string}"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_checkout_page_returns_correct_response_POST(self):
        self.assertFalse(self.guide.is_active)

        response = self.client.post(self.checkout_url + self.query_string)
        self.assertEqual(response.status_code, 404)

        self.guide.activate()
        self.assertTrue(self.guide.is_active)

        response = self.client.post(self.checkout_url + self.query_string)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('checkout.stripe.com' in response.url)
