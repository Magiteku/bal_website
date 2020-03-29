from django.shortcuts import render, redirect
from .models import Livre, UserProfile
from .forms import UserProfileForm, UserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
import operator
from functools import reduce
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
    
    query_term = ""
    livres,membres = Livre.objects.none(),UserProfile.objects.none()
    availableResult = False # devient True si on trouve au moins 1 résultat
    pageDeRetour='main_app/accueil.html'
    if 'query' in request.GET:
        query_term = str(request.GET['query'])
        # q est le nom (attribut name) de la barre de recheche (cf base.html)

    if query_term != "":
        for key, value in get_queryset(query_term).items():
          
            if key == "livres":
                livres = value
            elif key == "membres":
                membres = value
            else:
                continue
        pageDeRetour = 'main_app/recherches.html'
    
    # s'il y a au moins 1 résultat:
    if any([subquery.exists() for subquery in [livres,membres]]):
        availableResult = True 
 
    return render(request, pageDeRetour,locals())

def to_forum(request):
    return render(request, 'main_app/forum.html')

def subscription(request):
    """Inscription d'un membre """

    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    profile_form = UserProfileForm(request.POST or None, request.FILES or None)
    """
    request.POST ne contient que des données textuelles, tous les fichiers sélectionnés sont envoyés 
    depuis une autre méthode, et sont finalement recueillis par Django dans le dictionnaire request.FILES. 
    Si vous ne passez pas cette variable au constructeur, celui-ci considérera que le champ imageProfil est vide 
    et n’a donc pas été complété par l’utilisateur ; le formulaire sera donc invalide.
    """
    user_form = UserForm(request.POST or None)
    pageDeRetour = redirect('home')
    if all([profile_form.is_valid(),user_form.is_valid()]):

        user = user_form.save()
        username = user_form.cleaned_data.get('username')
        password = user_form.cleaned_data.get('password1')
        
        newMember = profile_form.save(commit=False) 
        # on ne sauvegarde pas le nouveau membre dans la base de donnée tout de suite car il faut
        # màj la valeur de son slug ainsi que son attribut user
        newMember.user = user
        slug_username = slugify(username)
        newMember.slug_username = slug_username
        newMember.imageProfil = profile_form.cleaned_data["imageProfil"]
        # NB: form.cleaned_data["attribut"] = form.cleaned_data.get("attribut")
        newMember.save()
        # Identification du membre 
        user = authenticate(username=username,password=password)
        
        
        #login(request,user)


        """
        
        newMember.save() # sauvegarde du nouveau membre dans la base de données
        # important : regarder fonctionnement des signaux pre_save et post_save car à priori
        # nécessaire pour que l'attribut user de Membre se sauvegarde automatiquement lors de 
        # de la sauvegarde de l'objet Membre
        """
    
    else:
        pageDeRetour = render(request,pageDeRetour,locals()) 
    
    return pageDeRetour
    # il faudra programmer une redirection automatique vers l'accueil si l'enregistrement est réussi
    # avec au préalable un message indiquant que l'enregistrement est réussi


def to_about(request):
    return render(request, 'main_app/about_us.html')

def to_contact(request):
    return render(request, 'main_app/contact.html')

def to_profile(request,pseudoSlug):
    membre = UserProfile.objects.filter(slug_username = pseudoSlug)
    """ Vérifier que le membre est connecté"""
    return render(request, 'main_app/profile.html',locals())

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

def to_login(request):
    """Redirige vers la page de connexion """

    return render(request,"main_app/login.html")


def get_queryset(query=None):
    """ Effectue une recherche dans la base de données du site
    en fonction des termes de entrées dans la barre de recherche
    -> dictionnaire de queryset, vide si aucun résultat trouvé """

    queryset = {
        "livres": Livre.objects.none(), # query_set vide
        "membres": UserProfile.objects.none()}
    # Il faudra rajouter les villes et les les boîtes à livres une fois les classes
    # créées
    queries = query.split(" ")

    for q in queries:
      
        livres = Livre.objects.filter(
            Q(titre__icontains=q) | Q(auteur__icontains=q) | 
            Q(resume__icontains=q) | Q(note__icontains=q) | Q(isbn__icontains=q)
            | Q(edition__icontains=q))
      
        membres = UserProfile.objects.filter(
            Q(user__username__icontains=q) | Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)
        )
        
        # queryset["livres"].union(livres) ne marche pas avec des query set vides pour des raisons inconnues
        queryset["livres"]|=livres # alternative qui fonctionne mais pourrait peut-être problématique à l'avenir
        queryset["membres"]|=membres
   

    return queryset









    