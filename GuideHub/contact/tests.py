from django.test import TestCase
from .models import Inquiry


class InquiryModelTest(TestCase):
    def test_inquiry_model_exists(self):
        inquiry_count = Inquiry.objects.count()

        self.assertEqual(inquiry_count, 0)

    def test_create_inquiry(self):
        email = "some@email.com"
        subject = "Very Important Topic"
        text = "This is an very important inquiry. Please read it!"

        inquiry = Inquiry.create_inquiry(
            email=email, subject=subject, text=text)

        inquiry_count = Inquiry.objects.count()
        self.assertTrue(isinstance(inquiry, Inquiry))
        self.assertEqual(inquiry_count, 1)
        self.assertEqual(inquiry, Inquiry.objects.first())

        self.assertEqual(inquiry.email, email)
        self.assertEqual(inquiry.subject, subject)
        self.assertEqual(inquiry.text, text)
