"""module initializing the user table in the database"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser, PermissionsMixin):

    """class initializing the user table in the database"""

    email = models.EmailField(unique=True)

