from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from plantes.models import UserPlante, Rappel
from datetime import date, timedelta
from django.core.mail import EmailMessage


class Command(BaseCommand):

    def handle(self, *args, **options):

        plante_user = UserPlante.objects.all()
        email_send = []
        for element in plante_user:
            date_reminder = element.plante
            if element.rappel is True and date.today() >= element.date_futur:
                 mail_subject = "Rappel d'arrosage pour "f"{element.name}."
                 message = render_to_string('reminder.txt', {
                    'user': element.user.username,
                    'contact': "Contact",
                    'planteName': element.name,
                    'planteType': element.plante.type,
                 })
                 email = EmailMessage(
                     mail_subject, message, to=[element.user.email]
                 )
                 email.send()
                 email_send.append(Rappel(userplante=element))
                 element.date_futur=date.today() + timedelta(days=date_reminder.arrosage)
                 element.save()

        Rappel.objects.bulk_create(email_send)
