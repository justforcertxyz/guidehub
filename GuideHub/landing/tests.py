from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegisterUserForm

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


class LogoutPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        username = "User"
        password = "foo"
        User.objects.create_user(username=username, password=password)
        self.logged_in = self.client.login(
            username=username, password=password)
        self.logout_url = reverse('landing:logout')
        self.success_url = reverse('landing:index')

    def test_logout_page_returns_correct_response(self):
        self.assertTrue(self.logged_in)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

        self.logged_in = self.client.logout()
        self.assertFalse(self.logged_in)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'{reverse('landing:login')}?next=/abmelden')


class RegisterUserFormTest(TestCase):
    def setUp(self):
        self.form = RegisterUserForm

    def test_form_valid(self):
        self.assertTrue(issubclass(self.form, RegisterUserForm))

        self.assertTrue('username' in self.form.Meta.fields)
        self.assertTrue('email' in self.form.Meta.fields)
        self.assertTrue('password1' in self.form.Meta.fields)
        self.assertTrue('password2' in self.form.Meta.fields)

        form = self.form({
            'username': 'username',
            'email': 'test@test.com',
            'password1': 'SomeStrongPassword123!xy',
            'password2': 'SomeStrongPassword123!xy',
        })

        self.assertTrue(form.is_valid())

    def test_save(self):
        self.assertEqual(User.objects.count(), 0)

        form = self.form({
            'username': 'username',
            'email': 'test@test.com',
            'password1': 'SomeStrongPassword123!xy',
            'password2': 'SomeStrongPassword123!xy',
        })

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(User.objects.count(), 1)


class RegisterUserPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('landing:register')
        self.success_url = reverse('landing:login')

    def test_register_page_returns_correct_response(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'landing/register.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_correct_response_POST(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(self.register_url,
                                    {
                                        'username': 'username',
                                        'email': 'ok@ok.com',
                                        'password1': "OKPassword123",
                                        'password2': "OKPassword123"
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

        self.assertEqual(User.objects.count(), 1)

    def test_register_page_correct_content(self):
        response = self.client.get(self.register_url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')
        self.assertContains(response, '<input type="submit"')
        self.assertContains(response, "<title>Registrieren")

        username = "User"
        password = "foo"
        User.objects.create_user(username=username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
        response = self.client.get(self.register_url)
        self.assertContains(response, 'bereits angemeldet')
