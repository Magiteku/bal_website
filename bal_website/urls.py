"""bal_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include

# imports nécessaire pour la gestion des images et fichiers
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookinner/', include('main_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# MEDIA_ROOT est le dossier dans lequel est stocké tous les fichiers
# MEDIA_URL est l'url à partir de laquel on peut accéder au fichiers stocké dans le dossier précisé par MEDIA_ROOT
# Par défault MEDIA_URL = '' . MEDIA_ROOT est précisé dans le fichier settings.py
""" La ligne de code ci-dessus est nécessaire si l'on souhaite acceder aux fichiers stockés dans le MEDIA_ROOT
à partir d'une URL. Par conséquent il faut toujours la préciser dès qu'au moins un modèle utilise un fichier.
Par ailleurs, il faut aussi précisé MEDIA_ROOT. Précisé MEDIA_URL n'est pas obligatoire
Pour des raisons de sécurité, gérer les fichiers de cette façon ne se fait qu'en développement. En production, il
faut employer une autre méthode (cf la doc officiel et/ou le chapitre déployer votre application de openclassroom)
"""
