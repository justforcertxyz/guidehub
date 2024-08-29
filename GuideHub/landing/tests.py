from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegisterUserForm
from guide.models import Guide
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os

User = get_user_model()


def create_guide(title, slug="some_slug", description="description", price=0, pages=1, author="", guide_pdf="", tags=""):
    if author == "":
        author = User.objects.create_user(username="Name", password="Foo")

    if guide_pdf == "":
        guide_pdf = SimpleUploadedFile(
            name="test_guide.pdf", content=b'Test guide', content_type="text/pdf")

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


class DashboardPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        username = "User"
        password = "foo"
        self.user = User.objects.create_user(
            username=username, password=password)
        self.logged_in = self.client.login(
            username=username, password=password)
        self.dashboard_url = reverse('landing:dashboard')
        self.login_url = reverse('landing:login')
        self.pdf_file_name = "test_guide.pdf"

        delete_file(self.pdf_file_name)

    def tearDown(self):
        delete_file(self.pdf_file_name)

    def test_register_page_returns_correct_response(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(self.dashboard_url)
        self.assertTemplateUsed(response, 'landing/dashboard.html')
        self.assertTemplateUsed(response, 'landing/base.html')
        self.assertEqual(response.status_code, 200)

        self.logged_in = self.client.logout()
        self.assertFalse(self.logged_in)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next=/dashboard/")

    def test_page_return_correct_content(self):
        name1 = "some_guide.pdf"
        pdf1 = SimpleUploadedFile(
            name=name1, content=b'Test guide', content_type="text/pdf")
        guide1 = create_guide(title="Some Guide",
                              author=self.user, price=10, guide_pdf=pdf1)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context['guides_owned'][0], guide1)
        self.assertEqual(response.context['guides_written'][0], guide1)

        name2 = "another_guide.pdf"
        pdf2 = SimpleUploadedFile(
            name=name2, content=b'Test guide', content_type="text/pdf")
        guide2 = create_guide(title="Another Guide",
                              slug="another_guide", author=self.user, price=5, guide_pdf=pdf2)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context['guides_owned'][0], guide2)
        self.assertEqual(response.context['guides_written'][0], guide2)
        self.assertEqual(response.context['guides_owned'][1], guide1)
        self.assertEqual(response.context['guides_written'][1], guide1)

        name3 = "another_other_guide.pdf"
        pdf3 = SimpleUploadedFile(
            name=name3, content=b'Test guide', content_type="text/pdf")
        guide3 = create_guide(title="Another other Guide",
                              slug="another_other_guide", author=self.user, price=15, guide_pdf=pdf3)
        name4 = "cheaper_guide.pdf"
        pdf4 = SimpleUploadedFile(
            name=name4, content=b'Test guide', content_type="text/pdf")
        guide4 = create_guide(title="Cheaper Guide",
                              slug="cheaper_guide", author=self.user, price=9.5, guide_pdf=pdf4)

        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context['guides_owned'][0], guide2)
        self.assertEqual(response.context['guides_written'][0], guide2)
        self.assertEqual(response.context['guides_owned'][1], guide4)
        self.assertEqual(response.context['guides_written'][1], guide4)
        self.assertEqual(response.context['guides_owned'][2], guide1)
        self.assertEqual(response.context['guides_written'][2], guide1)

        delete_file(name1)
        delete_file(name2)
        delete_file(name3)
        delete_file(name4)
