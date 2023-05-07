# P13 Green Mind : prenez soin de vos plantes

*L'application permet aux utilisateurs de trouver et d'enregistrer des plantes afin d'avoir des informations et des rappels d'arrosage par courriel concernant les plantes sélectionnées.*

## Pour commencer

### Pré-requis

Ce qu'il est requis pour commencer...

* Python 3 *https://www.python.org/downloads/*
* PostgreSQL *https://www.postgresql.org/*
* Git *https://git-scm.com/downloads*
* GitHub *https://github.com/*
* Un éditeur de code (ici PyCharm est utilisé *https://www.jetbrains.com/pycharm/download/download-thanks.html*)

### Installation 
Dans un terminal:
Connectez vous au serveur
Clonez le package avec git sur votre dépôt local (ordinateur) comme ceci:
 - Etape 1 : initialisation de git dans le dossier correspondant avec: *`git init`*
 - Etape 2: *`git remote add <nom du fichier> https://github.com/KlereBibi/P13-Green-Mind.git`* 
 - Etape 3: *`git clone https://github.com/KlereBibi/P13-Green-Mind.git`*
 
Initialisez votre environnement virtuel:
 - Etape 1: installation de pipenv avec la commande: *`pip install pipenv`*
 - Etape 2: initialisation de l'environnement virtuel dans le package: *`pipenv shell`* 
 - Etape 3: installer les modules nécessaires grâce au fichier requierements.txt: *`pipenv install -r requirements.txt`*

## Démarrage
* Créez un fichier .env avec vos propre variable d'environnement local à la racine du projet
* Exécutez *python manage.py migrate*
* Exécutez *python manage.py makemigration*
* Exécutez *python manage.py collectstatic*
* Exécutez *python manage.py plantesdb*
* Exécutez *python manage.py runserver* pour lancer l'application
* Consultez votre application sur votre adresse ip
* La commande personnalisée pour envoyer les rappels est: *python manage.py reminder*

## Fabriqué avec
* PyCharm - Editeur de texte

## Versions
* python 3.9.1
* Django 4.0.6

## Auteur
Claire Biedermann
