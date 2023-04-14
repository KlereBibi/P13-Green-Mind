import requests
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from plantes.forms import SearchPlante, SavePlante
from plantes.models import Plante, UserPlante, Rappel
from datetime import date, timedelta


def apiwiki(plantesearch):

    url = "http://fr.wikipedia.org/w/api.php?"
    parameters = {
        "action": "query",
        "prop": "extracts|info",
        "inprop": "url",
        "explaintext": True,
        "generator": "geosearch",
        "exsentences": 2,
        "exlimit": 1,
        "titles": f"{plantesearch}"
    }

    res = requests.get(url, params=parameters)

    if res.status_code == 200:
        content = res.json()

        try:
            content.get("query").get("pages")
        except AttributeError:
            return False

        places = content.get("query").get("pages")
        places_list = []

        for place in places:
            places_list.append(
                (
                    places.get(place).get("index"),
                    places.get(place).get("pageid"),
                )
            )
        if not places_list:
            return False

        place_selected = min(places_list)
        pageid_selected = str(place_selected[1])

        article = {
            "title": content.get("query")
                .get("pages")
                .get(pageid_selected)
                .get("title", ""),
            "extract": content.get("query")
                .get("pages")
                .get(pageid_selected)
                .get("extract", ""),
            "fullurl": content.get("query")
                .get("pages")
                .get(pageid_selected)
                .get("fullurl", ""),
        }
        return article

    else:
        return False


class UserTexte:

    def __init__(self, name, extrait, url=None, picture=None):
        self.name = name
        self.extrait = extrait
        self.url = url
        self.picture = picture


def apiwikipicture(title, page_id):

    img = requests.get("http://fr.wikipedia.org/w/api.php?action=query&prop=extracts|inf&inprop=url&explaintext=true&exsentences=2&exlimit=1&format=json&titles="f"{title}&prop=pageimages")

    if img.status_code == 200:
        content = img.json()

        picture = content.get("query").get("pages")

        try:
            picture = {
                "picture": content.get("query")
                    .get("pages")
                    .get(page_id)
                    .get("thumbnail")
                    .get("source",  "")}
        except AttributeError:
            picture = {"picture":"https://thumbs.dreamstime.com/b/dog-reading-newspaper-cool-funny-jack-russell-magazine-125398832.jpg"}
        return picture


def apiwiki(form):
    if form.is_valid():
        plante_user = form.cleaned_data
        plante_lower = plante_user['plante'].lower()
        res = requests.get("http://fr.wikipedia.org/w/api.php?action=query&prop=extracts|inf&inprop=url&explaintext=true&exsentences=2&exlimit=1&format=json&titles="f"{plante_lower}")
    else:
        title = "Erreur Formulaire"
        error = "Le formulaire n'est pas valide, merci de recommencer"
        erreur_texte = UserTexte(title, error)
        return erreur_texte

    if res.status_code == 200:
        content = res.json()
        plantes = content.get("query").get("pages")

        plantes_list = []
        for place in plantes:
            plantes_list.append(
                (
                    plantes.get(place).get("index"),
                    plantes.get(place).get("pageid"),
                )
            )

        place_selected = min(plantes_list)
        pageid_selected = str(place_selected[1])

        try:
            article = {
                "title": content.get("query")
                    .get("pages")
                    .get(pageid_selected)
                    .get("title", ""),
                "extract": content.get("query")
                    .get("pages")
                    .get(pageid_selected)
                    .get("extract", ""),
            }

            image = apiwikipicture(article['title'], pageid_selected)
            texte = UserTexte(article['title'], article['extract'], "https://fr.wikipedia.org/?curid="f"{pageid_selected}", image['picture'])
        except AttributeError:
            texte = UserTexte("Nous n'avons pas trouvé en lien avec la recherche "f"{plante_lower}.", "Merci de reformuler votre demande.", "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal", "https://thumbs.dreamstime.com/b/eagle-portrait-1649198.jpg", )
        return texte

    else:
        title = "Erreur serveur"
        content = "La requête ne peut aboutir, veuillez essayer ultérieurement"
        image ="https://thumbs.dreamstime.com/b/eagle-portrait-1649198.jpg"
        wikipedia = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
        erreur_texte = UserTexte(title, content, wikipedia, image)
        return erreur_texte


@require_http_methods(['POST'])
def find_plante(request):
    form = SearchPlante(request.POST)
    response = apiwiki(form)
    return render(request, "plantes/find_plante.html", context={"texte": response})


def plante(request):
    plante_db = Plante.objects.all()
    return render(request, "plantes/plante.html", context={"all_plantes_db": plante_db})


def explain_plante(request, plante_id):
    plante_explain = Plante.objects.get(pk=plante_id)
    return render(request, "plantes/planteExplain.html", context={"plante": plante_explain})


def my_plante(request):
    plante_user_db = UserPlante.objects.all()
    return render(request, "plantes/myPlantes.html", context={"all_plantes_db": plante_user_db})


@login_required
def user_plante(request, plante_id):
    form = SavePlante(request.POST)
    if form.is_valid():
        name_plante = form.cleaned_data
        plante_save = []
        try:
            plante = Plante.objects.get(pk=plante_id)
            plante_save.append(UserPlante(name=name_plante['name_plante_user'], rappel=name_plante['reminder'], plante=plante, user=request.user))
            UserPlante.objects.bulk_create(plante_save)
            plante_user = UserPlante.objects.get(name=name_plante['name_plante_user'])
            if name_plante['reminder'] is True:
                endate= date.today() + timedelta(days=plante.arrosage)
                plante_user.date_futur = endate
                plante_user.save()
            return render(request, "plantes/planteSave.html", context={"plante": plante})
        except IntegrityError:
            plante = Plante.objects.get(pk=plante_id)
            return render(request, "plantes/planteSave.html", context={"plante": False, "plante_i":plante})
    else:
        return redirect("welcome:homePage")


@require_http_methods(['POST'])
def search_plante_db(request):
    form = SearchPlante(request.POST)
    if form.is_valid():
        plante_user = form.cleaned_data
        plante_wanted = plante_user['plante']
        try:
            plante_db = Plante.objects.get(name=plante_wanted)
        except Plante.DoesNotExist:
            plante_db = None
        return render(request, "plantes/find_plante_db.html", context={"plante": plante_db})


def delete(request, plante_user_id):
    UserPlante.objects.filter(id=plante_user_id).delete()
    return redirect("plantes:myPlante")


def reminder_change(request, plante_user_id):
    plante_user = UserPlante.objects.get(id=plante_user_id)
    if plante_user.rappel is False:
        plante_user.rappel = True
        plante_user.save()
        endate = date.today() + timedelta(days=plante_user.plante.arrosage)
        plante_user.date_futur = endate
        plante_user.save()
    else:
        plante_user.rappel=False
        plante_user.save()
    return redirect("plantes:myPlante")
