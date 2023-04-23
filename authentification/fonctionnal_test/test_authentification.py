"""Test fonctionnal about user authentification and login"""

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from authentification.models import User


class TestAuthentification(StaticLiveServerTestCase):

    """class to initialize tests with selenium"""

    def test_reset_password(self):

        """Function testing the form in order to receive an email to change the password"""

        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("authentification:reset_password"))

        password1 = self.browser.find_element(By.ID, "id_email")
        password1.send_keys("test@gmail.com")

        signup = self.browser.find_element(By.ID, "Envoyer")
        signup.click()

        self.assertEqual(self.browser.find_element(By.ID, 'text').text,
                         "La réinitialisation du mot de passe a été envoyé")
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse("authentification:password_reset_done"))

        self.browser.close()

    def test_register_success(self):

        """Function testing the form for registering on the application"""

        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("authentification:register"))

        email = self.browser.find_element(By.ID, "id_email")
        email.send_keys(By.ID, "test@test.com")
        fname = self.browser.find_element(By.ID, "id_first_name")
        fname.send_keys("Claire")
        lname = self.browser.find_element(By.ID, "id_last_name")
        lname.send_keys("Etudiante")
        username = self.browser.find_element(By.CLASS_NAME, "usernameRegister")
        username.send_keys("cEtudiante")
        password1 = self.browser.find_element(By.ID, "id_password1")
        password1.send_keys("password@10")
        password2 = self.browser.find_element(By.ID, "id_password2")
        password2.send_keys("password@10")
        signup = self.browser.find_element(By.ID, "sub")
        signup.send_keys()
        sleep(5)
        signup.click()

        self.assertEqual(self.browser.find_element(By.ID, 'confirmation_text').text,
                         "Un courriel vous a été envoyé.")
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse("authentification:register"))

        self.browser.close()

    def test_login_success(self):

        """Function testing the login form"""

        user = User(username='test', first_name="Claire", email='test@gmail.com', is_active=True)
        user.set_password('test@.test')
        user.save()

        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.maximize_window()
        self.browser.get(self.live_server_url + reverse("authentification:login"))

        username = self.browser.find_element(By.CLASS_NAME, "usernameLogin")
        username.send_keys("test")
        password1 = self.browser.find_element(By.ID, "id_password")
        password1.send_keys("test@.test")
        signup = self.browser.find_element(By.ID, "submit")
        signup.click()

        self.assertEqual(self.browser.find_element(By.ID, 'textConfirSel').text, "Bonjour "f"{user.first_name},")
        self.assertEqual(self.browser.current_url,self.live_server_url + reverse("authentification:account"))

        self.browser.close()

    def test_login_error(self):

        """Function testing the login form error when the user isn't register"""

        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.maximize_window()
        self.browser.get(self.live_server_url + reverse("authentification:login"))

        username = self.browser.find_element(By.CLASS_NAME, "usernameLogin")
        username.send_keys("test")
        password1 = self.browser.find_element(By.ID, "id_password")
        password1.send_keys("test@.test")
        signup = self.browser.find_element(By.ID, "submit")
        signup.click()
        text_error = "Saisissez un nom d’utilisateur et un mot de passe valides. " \
                     "Remarquez que chacun de ces champs est sensible à la casse " \
                     "(différenciation des majuscules/minuscules)."
        self.assertEqual(self.browser.find_element(By.CLASS_NAME, 'text-danger').text, text_error)
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse("authentification:login"))

        self.browser.close()
