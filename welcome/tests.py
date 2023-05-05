from http import HTTPStatus
from django.test import TestCase
from django.test import Client
from authentification.models import User
from django.core import mail


class TestViews(TestCase):

    """class to test the different feature about products"""

    def setUp(self):

        """user settings initialization for test"""

        user = User(username='test', email='test@gmail.com', is_active=True)
        user.set_password('test@.test')
        user.save()

    def test_home_page(self):

        """test about template home page and connect home page """

        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome/home.html')

    def test_legal_mention(self):
        """test about template home page and connect home page """

        c = Client()
        response = c.get('/mentionLegal/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome/legalMention.html')

    def test_contact(self):

         """test about template home page and connect home page """
    
         c = Client()
         c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
         response = c.get('/contact/')
         self.assertEqual(response.status_code, 200)

    def test_contact_send(self):

          c = Client()
          c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
          response = c.post("/contact/confirm", data={'subject': 'something', 'text': 'something'})
          self.assertEqual(response.status_code, 200)
          self.assertEqual(len(mail.outbox), 1)
          self.assertTemplateUsed(response, 'welcome/contactEnvoye.html')
