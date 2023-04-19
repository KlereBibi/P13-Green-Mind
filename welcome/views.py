from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from welcome.forms import ContactForm
from authentification.models import User


def home(request):
    return render(request, "welcome/home.html")


def legal_mention(request):

    return render(request, "welcome/legalMention.html")


def contact(request):

    return render(request, "welcome/contact.html")


@login_required
def answer_contact(request, user_id):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data
            user = User.objects.get(id=user_id)
            mail_subject = "Un utilisateur a une question."
            message = render_to_string('welcome/contact.txt', {
                'prenom':user.first_name,
                'nom' : user.last_name,
                'email': user.email,
                'sujet': contact['subject'],
                'texte': contact['text'],
            })
            mail_contact="biedermannclaire153@gmail.com"
            email = EmailMessage(
                mail_subject, message, to=[mail_contact]
            )
            email.send()
            return render(request, "welcome/contactEnvoye.html")
