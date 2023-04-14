"""module containing the different authentication forms"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):

    """"class to register"""

    email = forms.EmailField(label="Email", max_length=150)
    username = forms.CharField(label="Username", max_length=150)
    first_name = forms.CharField(label="First name", max_length=150)
    last_name = forms.CharField(label="Last name", max_length=150)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    """class to connect"""

    username = forms.CharField(label='Email', max_length=150)
