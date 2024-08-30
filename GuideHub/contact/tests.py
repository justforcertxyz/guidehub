from django.test import TestCase
from .models import Inquiry
from .forms import CreateInquiryForm


def create_inquiry(subject, email="some@email.com", text="Some inquiry text"):
    return Inquiry.create_inquiry(subject=subject, email=email, text=text)


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
        self.assertFalse(inquiry.processed)

    def test___str__(self):
        subject = "Very Important Inquiry"
        inquiry = create_inquiry(subject=subject)
        self.assertEqual(str(inquiry), subject)

    def test_finish_processing(self):
        inquiry = create_inquiry("Very Important")
        self.assertFalse(inquiry.processed)

        inquiry.finish_processing()

        self.assertTrue(Inquiry.objects.first().processed)

class CreateInquiryFormTest(TestCase):
    def setUp(self):
        self.form = CreateInquiryForm

    def test_form_valid(self):
        self.assertTrue(issubclass(self.form, CreateInquiryForm))

        self.assertTrue('email' in self.form.Meta.fields)
        self.assertTrue('subject' in self.form.Meta.fields)
        self.assertTrue('text' in self.form.Meta.fields)

        form = self.form({
            'email': "some@mail.de",
            "subject": "subject",
            "text": "Text",
        })

        self.assertTrue(form.is_valid())