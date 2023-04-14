"""module calling the form to search a product"""

from authentification.forms import RegisterForm
from authentification.forms import LoginForm


def register_form(request):

    """calls the search method of product
    returns the search form"""

    return {"register_form":  RegisterForm()}


def login_form(request):

    """calls the search method of product
    returns the search form"""

    return {"login_form":  LoginForm()}
