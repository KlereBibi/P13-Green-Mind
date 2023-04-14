from django.db import models
from authentification.models import User
import datetime

class Plante(models.Model):

    """"class to creat plante"""

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=30)
    resume = models.TextField(max_length=500)
    exposition = models.CharField(max_length=50)
    entretien = models.CharField(max_length=10)
    arrosage = models.IntegerField()
    picture = models.URLField(max_length=200)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class UserPlante (models.Model):

    name = models.CharField(max_length=100, unique=True)
    rappel = models.BooleanField()
    date_futur = models.DateField(null=True)
    plante = models.ForeignKey(Plante, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rappel (models.Model):

    emailDate = models.DateField(default=datetime.date.today)
    userplante = models.ForeignKey(UserPlante, on_delete=models.CASCADE, related_name='SaveUserPlante')

    def __str__(self):
        return self.emailDate
