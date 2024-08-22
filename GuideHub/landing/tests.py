from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('landing:index')

    def test_index_page_returns_correct_response(self):
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'landing/index.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_returns_corrent_content(self):
        response = self.client.get(self.index_url)
        self.assertContains(response, "<title>Home")


class PrivacyPolicyPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.privacy_policy_url = reverse('landing:privacy-policy')

    def test_privacy_policy_page_returns_correct_response(self):
        response = self.client.get(self.privacy_policy_url)
        self.assertTemplateUsed(response, 'landing/privacy_policy.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_page_returns_corrent_content(self):
        response = self.client.get(self.privacy_policy_url)
        self.assertContains(response, "<title>Datenschutzerklärung")


class ImprintPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.imprint_url = reverse('landing:imprint')

    def test_imprint_page_returns_correct_response(self):
        response = self.client.get(self.imprint_url)
        self.assertTemplateUsed(response, 'landing/imprint.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_imprint_page_returns_corrent_content(self):
        response = self.client.get(self.imprint_url)
        self.assertContains(response, "<title>Impressum")


class LoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('landing:login')
        self.success_url = reverse('landing:index')

    def test_login_page_returns_correct_response(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'landing/login.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_login_page_returns_correct_response_POST(self):
        username = "User"
        password = "foo"
        User.objects.create_user(username=username, password=password)

        response = self.client.post(
            self.login_url, {'username': username, 'password': password, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_login_page_correct_content(self):
        response = self.client.get(self.login_url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

        username = "User"
        password = "foo"
        User.objects.create_user(username=username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        response = self.client.get(self.login_url)
        self.assertContains(response, 'bereits angemeldet')
