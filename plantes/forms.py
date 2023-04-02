""""module to initialize the search form"""

from django import forms


class SearchPlante(forms.Form):

    """"class to initialize the search form"""

    plante = forms.CharField(label="", max_length=20, required=True, strip=False)


class SavePlante(forms.Form):

    """"class to initialize the search form"""

    name_plante_user = forms.CharField(label="Nom de votre plante", max_length=20, required=True, strip=False)
    reminder = forms.BooleanField(label="Rappel d'arrosage", initial=True, required=False)

