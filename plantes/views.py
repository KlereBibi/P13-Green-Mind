"""module returning the different views of plantes"""

import requests
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from plantes.forms import SearchPlante, SavePlante
from plantes.models import Plante, UserPlante, Rappel


class UserTexte:

    """class to initialize user text"""

    def __init__(self, name, extrait, url=None, picture=None):
        self.name = name
        self.extrait = extrait
        self.url = url
        self.picture = picture


def apiwikipicture(title, page_id):

    """class to return the wikipedia image of the article"""

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


@require_http_methods(['POST'])
def find_plante(request):

    """class allowing to find and find information in wikipedia"""

    if request.method == 'POST':
        form = SearchPlante(request.POST)
        if form.is_valid():
            plante_user = form.cleaned_data
            plante_lower = plante_user['plante'].lower()
            res = requests.get(
                "http://fr.wikipedia.org/w/api.php?action=query&prop=extracts|inf&inprop=url&explaintext=true&exsentences=2&exlimit=1&format=json&titles="f"{plante_lower}")
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
                    text = UserTexte(article['title'], article['extract'],
                                      "https://fr.wikipedia.org/?curid="f"{pageid_selected}", image['picture'])
                except AttributeError:
                    text = UserTexte("Nous n'avons pas trouvé en lien avec la recherche "f"{plante_lower}.",
                                      "Merci de reformuler votre demande.",
                                      "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal",
                                      "https://thumbs.dreamstime.com/b/eagle-portrait-1649198.jpg", )
                return render(request, "plantes/find_plante.html", context={"texte": text})
            else:
                error_form()
                
    else:
        search_form = SearchPlante()
        return render(request, "plantes/plante.html", context={"search_form": search_form})


def error_form(request):

    """class allowing to return a server error"""

    title = "Erreur serveur"
    content = "La requête ne peut aboutir, veuillez essayer ultérieurement"
    image = "https://thumbs.dreamstime.com/b/eagle-portrait-1649198.jpg"
    wikipedia = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
    erreur_text = UserTexte(title, content, wikipedia, image)
    return render(request, "plantes/find_plante.html", context={"texte": erreur_text})


def plante(request):

    """class to return the plants available in the database"""

    plante_db = Plante.objects.all()
    search_form = SearchPlante()
    return render(request, "plantes/plante.html", context={"all_plantes_db": plante_db, "search_form":search_form})


def explain_plante(request, plante_id):

    """class to return a specific plant"""

    plante_explain = Plante.objects.get(pk=plante_id)
    save_form=SavePlante()
    search_form=SearchPlante()
    return render(request, "plantes/planteExplain.html",
                  context={"plante": plante_explain, "save_form":save_form, "search_form":search_form})


def my_plante(request):

    """class to return a plant of the logged in user"""

    plante_user_db = UserPlante.objects.all()
    search_form = SearchPlante()
    return render(request, "plantes/myPlantes.html",
                  context={"all_plantes_db": plante_user_db, "search_form":search_form})


@login_required
def user_plante(request, plante_id):

    """class allowing to register a plant, its name and reminder"""

    if request.method == 'POST':
        form = SavePlante(request.POST)
        search_form = SearchPlante()
        save_form = SavePlante()
        if form.is_valid():
            name_plante = form.cleaned_data
            plante_save = []
            try:
                plante = Plante.objects.get(pk=plante_id)
                if name_plante['reminder'] is True:
                    endate = date.today() + timedelta(days=plante.arrosage)
                    plante_save.append(UserPlante(name=name_plante['name_plante_user'],
                                                    rappel=name_plante['reminder'], date_futur=endate,
                                                    plante=plante, user=request.user))
                    UserPlante.objects.bulk_create(plante_save)
                else:
                    plante_save.append(UserPlante(name=name_plante['name_plante_user'],
                                                  rappel=name_plante['reminder'],
                                                  plante=plante, user=request.user))
                    UserPlante.objects.bulk_create(plante_save)
                return render(request, "plantes/planteSave.html",
                              context={"plante": plante, "save_form":save_form, "search_form": search_form})
            except IntegrityError:
                plante = Plante.objects.get(pk=plante_id)
                return render(request, "plantes/planteSave.html",
                              context={"plante": False, "plante_i":plante, "save_form":save_form, "search_form": search_form})
        else:
            error_form(request)
    else:
        form = SavePlante()
        return render(request, 'plantes/planteSave.html', {'form': form})


@require_http_methods(['POST'])
def search_plante_db(request):

    """class to search for a plant in the database"""

    if request.method == 'POST':
        form = SearchPlante(request.POST)
        if form.is_valid():
            plante_user = form.cleaned_data
            plante_wanted = plante_user['plante'].lower()
            try:
                plante_db = Plante.objects.get(name=plante_wanted)
            except Plante.DoesNotExist:
                plante_db = None
            return render(request, "plantes/find_plante_db.html", context={"plante": plante_db})
        else: 
            error_form(request)
    else:
        search_form = SearchPlante()
        return render(request, "plantes/plante.html", context={"search_form": search_form})


def delete(request, plante_user_id):

    """class for deleting a plant from the database"""

    UserPlante.objects.filter(id=plante_user_id).delete()
    return redirect("plantes:myPlante")


def reminder_change(request, plante_user_id):

    """class to enable/disable the reminder"""

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
