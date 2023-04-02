"""GreenMind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from plantes import views
from django.urls import path, re_path

app_name = "plantes"

urlpatterns = [
    path('SearchPlante/', views.find_plante, name='searchPlante'),
    path('Plantesdb/', views.search_plante_db, name='dbPlante'),
    path('Plantes/', views.plante, name='allPlante'),
    path('PlanteExplain/<int:plante_id>', views.explain_plante, name='explainPlante'),
    path('PlanteUser/<int:plante_id>', views.user_plante, name='userPlante'),
    path('MyPlante/', views.my_plante, name='myPlante'),
    path('Delete/<int:plante_user_id>', views.delete, name='delete'),
    path('Reminder/<int:plante_user_id>', views.reminder_change, name='reminder'),
]

