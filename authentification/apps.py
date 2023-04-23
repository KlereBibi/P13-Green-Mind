"""Module for configuring the authentification package"""

from django.apps import AppConfig


class AuthentificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentification'
