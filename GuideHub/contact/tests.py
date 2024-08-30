from django.test import TestCase, Client
from .models import Inquiry
from .forms import CreateInquiryForm
from django.urls import reverse
from unittest import skip


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


class CreateInquiryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact:index')
        self.success_url = reverse('landing:index')

    def test_create_inquiry_page_returns_correct_response(self):
        response = self.client.get(self.contact_url)
        self.assertTemplateUsed(response, 'contact/index.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_create_inquiry_page_returns_correct_response_POST(self):
        inquiry_count = Inquiry.objects.count()
        self.assertEqual(inquiry_count, 0)

        response = self.client.post(self.contact_url, {
            'email': 'some@mail.de',
            'subject': 'Subject',
            'text': 'text',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

        inquiry_count = Inquiry.objects.count()
        self.assertEqual(inquiry_count, 1)

    def test_create_inquiry_page_correct_content(self):
        response = self.client.get(self.contact_url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')
        self.assertContains(response, '<input type="submit"')
        self.assertContains(response, "<title>Kontakt")

        self.assertContains(response, "E-Mail-Adresse:</label>")
        self.assertContains(response, "Betreff:</label>")
        self.assertContains(response, "Anfragentext:</label>")
