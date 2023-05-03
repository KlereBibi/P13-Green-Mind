"""module returning the different views of the home page and contact"""

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from authentification.models import User
from welcome.forms import ContactForm


def home(request):

    """function that returns the home page view"""

    return render(request, "welcome/home.html")


def legal_mention(request):

    """function that returns the mention legal"""

    return render(request, "welcome/legalMention.html")


def contact(request):

    """function that returns the form of contact"""

    form = ContactForm()
    return render(request, "welcome/contact.html", {'form': form})


@login_required
def answer_contact(request, user_id):

    """function that sends the email containing the information returned by the contact form"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data
            user = User.objects.get(id=user_id)
            mail_subject = "Un utilisateur a une question."
            message = render_to_string('welcome/contact.txt', {
                'prenom':user.first_name,
                'nom': user.last_name,
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
    else:
        form = ContactForm()
        return render(request, "welcome/contact.html", {'form': form})
