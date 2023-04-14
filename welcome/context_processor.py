"""module calling the form to search a product"""

from welcome.forms import ContactForm


def contact_form(request):

    """calls the search method of product
    returns the search form"""

    return {"contact_form":  ContactForm()}
