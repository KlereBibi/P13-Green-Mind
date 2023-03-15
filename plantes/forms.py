""""module to initialize the search form"""

from django import forms


class SearchPlante(forms.Form):

    """"class to initialize the search form"""

    plante = forms.CharField(label="", max_length=10, required=True, strip=False)
