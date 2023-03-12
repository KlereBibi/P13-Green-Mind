from django.shortcuts import render

# Create your views here.

from welcome.forms import SearchPlante


def home(request):
    return render(request, "welcome/home.html")


def search_plante(request):

    """method to search the product requested by the user and returns the corresponding information
    return a list of object product or nothing"""

    form = SearchPlante()
    return render(request, "main.html", context={'form': form})
