"""module to initialize the search form the plante package"""

from django import forms


class SearchPlante(forms.Form):

    """"class to initialize the search form to find plante"""

    plante = forms.CharField(label="Ex: sansevieria", max_length=20, required=True, strip=False)


class SavePlante(forms.Form):

    """"class to initialize the save form to save plante"""

    reminder = forms.BooleanField(label="Rappel d'arrosage", initial=True, required=False)
    name_plante_user = forms.CharField(label="Nom de votre plante", max_length=20, required=False, strip=False)


