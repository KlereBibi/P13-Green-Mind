"""plant app test"""

from datetime import date, timedelta
from django.core.management import call_command
from django.test import TestCase
from django.test import Client
from authentification.models import User
from plantes.models import UserPlante, Plante
from plantes.views import UserTexte


class TestViews(TestCase):

    """class to test the different feature about plante"""

    def setUp(self):

        """user settings initialization for test"""

        user = User(username='test', email='test@gmail.com', is_active=True)
        user.set_password('test@.test')
        user.save()

    def test_user_texte(self):

        """test to test the initialisation class of Usertext"""

        UserTexte('Claire', 'extrait', 'http://test.com', 'http://picture.com')

    def test_search_plante_wikipedia_success(self):

        """test to find with wikipedia api what user asked"""

        c = Client()
        response = c.post("/plantes/SearchPlante/", data={'plante': 'rose'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plantes/find_plante.html')

    def test_search_plante_db_success(self):

        """test to find in database what user asked with data initializ"""

        c = Client()
        Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                        entretien="facile", arrosage="3", picture="http://soleil.com",
                                        url="http://soleil.com")
        response = c.post("/plantes/Plantesdb/", data={'plante': 'yucca'})
        self.assertTemplateUsed(response, 'plantes/find_plante_db.html')
        self.assertContains(response, 'yucca', status_code=200)

    def test_plante(self):

        """test that the function returns a page with the data initialized in the database"""

        c = Client()
        Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                        entretien="facile", arrosage="3", picture="http://soleil.com",
                                        url="http://soleil.com")
        response = c.post("/plantes/Plantes/")
        self.assertTemplateUsed(response, 'plantes/plante.html')
        self.assertContains(response, 'yucca', status_code=200)

    def test_plante_error(self):

        """error test when no plant is in the database"""

        c = Client()
        response = c.post("/plantes/Plantes/")
        self.assertTemplateUsed(response, 'plantes/plante.html')
        self.assertContains(response, 'Aucun produit ne correspond à votre recherche', status_code=200)

    def test_plante_explain(self):

        """test to confirm that the function returns the correct plant when clicking on 'learn more'"""

        plante = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                              entretien="facile", arrosage="3", picture="http://soleil.com",
                              url="http://soleil.com")
        c = Client()
        response = c.post("/plantes/PlanteExplain/"f"{plante.id}")
        self.assertTemplateUsed(response, 'plantes/planteExplain.html')
        self.assertContains(response, 'yucca', status_code=200)

    def test_plante_user_save(self):

        """test to find out if the function saves the plant that the user has selected in the database"""

        plante = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                       entretien="facile", arrosage="3", picture="http://soleil.com",
                                       url="http://soleil.com")
        User.objects.create(username='Claire', first_name='TheBest', last_name='OfTheWorld',
                                       email='claire@gmail.com')
        c = Client()
        c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
        response = c.post("/plantes/PlanteUser/"f"{plante.id}", data={'reminder': True, 'name_plante_user':'mimine'})
        self.assertTemplateUsed(response, 'plantes/planteSave.html')
        self.assertContains(response, 'Votre plante a bien été sauvegardé', status_code=200)

    def test_all_plante_user(self):

        """test returns all the plants that the user has registered"""

        plante1 = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                       entretien="facile", arrosage="3", picture="http://soleil.com",
                                       url="http://soleil.com")
        plante2 = Plante.objects.create(name="rose", type="arbuste", resume="une autre plante", exposition="ombre",
                                       entretien="facile", arrosage="7", picture="http://soleil.com",
                                       url="http://soleil.com")
        user_name = User.objects.create(username='Claire', first_name='TheBest', last_name='OfTheWorld',
                                       email='claire@gmail.com')
        date_futur = (date.today() + timedelta(days=4))
        UserPlante.objects.create(name="mimine", rappel=True, date_futur=date_futur, plante=plante1,
                                                user=user_name)
        UserPlante.objects.create(name="loulou", rappel=True, date_futur=date_futur, plante=plante2,
                                  user=user_name)
        c = Client()
        c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
        response = c.post("/plantes/MyPlante/")
        self.assertTemplateUsed(response, 'plantes/myPlantes.html')
        self.assertContains(response, 'loulou', status_code=200)
        self.assertContains(response, 'mimine', status_code=200)

    def test_delete(self):

        """test confirming the deletion of a user plant"""

        plante1 = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                       entretien="facile", arrosage="3", picture="http://soleil.com",
                                       url="http://soleil.com")
        user_name = User.objects.create(username='Claire', first_name='TheBest', last_name='OfTheWorld',
                                       email='claire@gmail.com')
        date_futur = (date.today() + timedelta(days=4))
        user_plante = UserPlante.objects.create(name="mimine", rappel=True, date_futur=date_futur, plante=plante1,
                                                user=user_name)
        c = Client()
        c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
        response = c.post("/plantes/Delete/"f"{user_plante.id}")
        self.assertEqual(response.status_code, 302)

    def test_reminder(self):

        """test ensuring that automated reminders are sent"""

        plante1 = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                       entretien="facile", arrosage="3", picture="http://soleil.com",
                                       url="http://soleil.com")
        user_name = User.objects.create(username='Claire', first_name='TheBest', last_name='OfTheWorld',
                                       email='claire@gmail.com')
        date_futur = (date.today() + timedelta(days=4))
        user_plante = UserPlante.objects.create(name="mimine", rappel=True, date_futur=date_futur, plante=plante1,
                                                user=user_name)
        c = Client()
        c.post('/auth/login/', {'username': 'test', 'password': 'test@.test'})
        response = c.post("/plantes/Delete/"f"{user_plante.id}")
        self.assertEqual(response.status_code, 302)


class CommandsTestCase(TestCase):

    def test_command_plante(self):

        """Test my custom command plantedb, to save in database the plante"""

        args = []
        opts = {}
        call_command('plantesdb', *args, **opts)

    def test_command_reminder(self):

        """Test my custom command reminder to send the reminder mail"""

        plante1 = Plante.objects.create(name="yucca", type="plante", resume="une plante", exposition="lumière",
                                        entretien="facile", arrosage="3", picture="http://soleil.com",
                                        url="http://soleil.com")
        user_name = User.objects.create(username='Claire', first_name='TheBest', last_name='OfTheWorld',
                                        email='claire@gmail.com')
        date_futur = date.today()
        user_plante = UserPlante.objects.create(name="mimine", rappel=True, date_futur=date_futur, plante=plante1,
                                                user=user_name)
        " Test my custom command."
        args = []
        opts = {}
        call_command('reminder', *args, **opts)
