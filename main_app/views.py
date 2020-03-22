from django.shortcuts import render
from .models import Livre, UserProfile
from .forms import UserProfileForm, UserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
    pageDeRetour = "main_app/signin.html"
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
        username = formMember.cleaned_data["user.username"]
        first_name = formMember.cleaned_data["user.first_name"]
        last_name = formMember.cleaned_data["user.last_name"]
        imageProfil = formMember.cleaned_data["imageProfil"]
        slug_username = slugify(username)
        email = formMember.cleaned_data["user.email"]
        #password = formMember.cleaned_data["password"]
        user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        newMember = Membre(user=user,imageProfil=imageProfil,slug_username=slug_username)
        
        newMember.save() # sauvegarde du nouveau membre dans la base de données
        # important : regarder fonctionnement des signaux pre_save et post_save car à priori
        # nécessaire pour que l'attribut user de Membre se sauvegarde automatiquement lors de 
        # de la sauvegarde de l'objet Membre
        """
        
        pageDeRetour = "main_app/accueil.html"
        # attention: la redirection ne change pas l'url. Voir comment procéder pour les redirections
        
    # on reste sur la page d'inscription dans tous les cas
    return render(request,pageDeRetour,locals()) 
    # il faudra programmer une redirection automatique vers l'accueil si l'enregistrement est réussi
    # avec au préalable un message indiquant que l'enregistrement est réussi


def to_about(request):
    return render(request, 'main_app/about_us.html')

def to_contact(request):
    return render(request, 'main_app/contact.html')

def to_profile(request,pseudoSlug):
    membre = UserProfil.objects.filter(slug_username = pseudoSlug)
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

