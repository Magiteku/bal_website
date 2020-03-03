from django.shortcuts import render
from .models import Livre
# Create your views here.

EMPLACEMENT_LIVRE = "book"
# Comme le choix de l'url n'est pas encore décidé, c'est une variable pour l'instant

def home(request):
    """ Page d'accueil du site
    Contient:
     * Une barre de recherche
     * Un accès au forum
     * Un moyen de s'inscrire/se connecter/ voir son profil
     * Une carte avec les localisations des boîtes à livre
     * Les tendances/ flux personalisés si connecté
     * Des pubs

     """

    return render(request, 'main_app/accueil.html')

def to_forum(request):
    return render(request, 'main_app/forum.html')

def to_subscription(request):
    pass

def to_about(request):
    return render(request, 'main_app/about_us.html')

def to_contact(request):
    pass

def to_profile(request):
    return render(request, 'main_app/profile.html')

def to_bookList(request):
    """ Redirige vers une page contenant l'ensemble des livres disponibles
        ou bien vers la page du livre dont le titre a été précisé """
    
    context = {"livres": Livre.objects.all()}
    return render(request,"main_app/listeDesLivres.html",context)

def to_book(request,bookSlug):
    """Redirige vers la page du livre dont le titre a été précisé """

    livre = Livre.objects.filter(slug_title = bookSlug).first()
    # Important: il est tout à fait possible qu'un livre puisse être plusieurs fois dans une BàL ou même dans
    # différentes BàL en même temps. Par conséquent le titre d'un livre ne constitue pas une clé idéale pour 
    # l'identifier individuellement. Ici cependant, ce n'est pas un problème
    return render(request,"main_app/descriptionLivre.html",locals())

# A faire : les templates et les routages urls