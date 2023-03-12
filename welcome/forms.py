from django import forms


class SearchPlante(forms.Form):

    """"class to initialize the search form"""

    plantes = forms.CharField(max_length=100)
