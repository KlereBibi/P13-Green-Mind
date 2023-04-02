"""module calling the form to search a product"""

from plantes.forms import SearchPlante
from plantes.forms import SavePlante

def search_form(request):

    """calls the search method of product
    returns the search form"""

    return {"search_form":  SearchPlante()}

def save_form(request):

    """calls the search method of product
    returns the search form"""

    return {"save_form":  SavePlante()}
