"""module containing the different authentication forms"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):

    """"class to register"""

    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    """class to connect"""

    username = forms.CharField(label='Email')
