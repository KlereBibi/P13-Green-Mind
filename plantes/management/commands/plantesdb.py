from django.core.management.base import BaseCommand
from plantes.models import Plante
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):

        plantes = []
        with open("/Users/klere/Documents/open_classroom/P13/GreenMind/plantes/management/commands/Plantes.csv", 'r', encoding='utf-8') as file:
            plantes_list = csv.reader(file)

            for row in plantes_list:
                plantes.append(row)

        plante_obj = []
        for element in plantes:
            try:
                new_plante = Plante(name=element[0],
                     type= element[1],
                     resume=element[2],
                     exposition=element[3],
                     entretien=element[4],
                     arrosage=element[5],
                     url=element[6],
                     picture=element[7],
                    )
                plante_obj.append(new_plante)
            except KeyError:
                continue

        Plante.objects.bulk_create(plante_obj, ignore_conflicts=True)

