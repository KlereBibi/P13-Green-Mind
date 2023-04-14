""""module to initialize the search form"""

from django import forms


class ContactForm(forms.Form):

    """"class to initialize the search form"""

    subject = forms.CharField(label="Sujet", max_length=50, required=True, strip=False)
    text = forms.CharField(label="Une question?", max_length=300, required=True, strip=False)


