"""module containing the Authentication application tests"""
from django.test import TestCase
from django.test import Client
from authentification.models import User
from django.core import mail
import re


class TestViews(TestCase):

    """class to test the different feature about authentification"""

    def setUp(self):

        """user settings initialization for test"""

        user = User(username='test', email='test@gmail.com', is_active=True)
        user.set_password('test@.test')
        user.save()

    def test_login_page(self):

        """page login test """

        c = Client()
        response = c.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentification/login.html')

    def test_login_succes(self):

        """login success test with identifiant"""

        c = Client()
        response = c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
        self.assertRedirects(response, '/')

    def test_login_error(self):

        """login success test with identifiant"""

        c = Client()
        response = c.post('/auth/login/', {'username': 'false', 'password': 'false'})
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):

        """register success test with identifiant"""

        c = Client()
        response = c.post('/auth/register/', {'email': 'claire@gmail.com', 'username': 'Claire',
                                              'first_name': 'TheBest', 'last_name': 'OfTheWorld',
                                              'password1': 'test@.test', 'password2': 'test@.test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmation/confirm_mail.html')
        self.assertEqual(len(mail.outbox), 1)

    def test_register_error(self):
        """register success test with identifiant"""

        c = Client()
        response = c.post('/auth/register/', {'email': '', 'username': '',
                                              'first_name': '', 'last_name': '',
                                              'password1': '', 'password2': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTemplateUsed(response, 'authentification/register.html')

    def test_register_invalid(self):
        """register success test with identifiant"""

        c = Client()
        response = c.get('/auth/register/', {'email': '', 'username': '',
                                              'first_name': '', 'last_name': '',
                                              'password1': '', 'password2': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTemplateUsed(response, 'authentification/register.html')

    def test_account_page(self):

        """page account test """

        c = Client()
        response = c.get('/auth/account/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentification/account.html')


class PasswordResetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
                    username="user",
                    email="test@gmail.com",
                    password="pwd")

        self.c = Client()

    def test_send_mail(self):
        self.c.post('/auth/reset_password/', {'email': 'test@gmail.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation du mot de passe.')
        assert mail.outbox[0].to == ['test@gmail.com']

    def test_send_no_mail(self):
        self.c.post('/auth/reset_password/', {'email': 'gg@gmail.com'})
        self.assertEqual(len(mail.outbox), 0)

    def test_url_mail_password_reset(self):

        #Send the email
        self.c.post('/auth/reset_password/', {'email': 'test@gmail.com'})

        #Search the email adress to redirect
        body = mail.outbox[0].body
        link_regex = re.compile(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, body)
        for element in links:
            self.url = element[0]

        #Test the template use redirection
        response = self.c.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/password_reset_confirm.html')

