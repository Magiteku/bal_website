from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Livre(models.Model):
    titre = models.CharField(max_length = 50)
    slug_title = models.SlugField(default = "")
    auteur = models.CharField(max_length = 50)
    resume = models.TextField(max_length = 500)
    couverture = models.ImageField(upload_to="couvertures/")
    # les couvertures seront enregistrés dans le dossier MEDIA_ROOT/couvertures/
    note = models.PositiveSmallIntegerField()
    codeBarre = models.CharField(max_length = 50)
    isbn = models.CharField(max_length = 50)
    edition = models.CharField(max_length = 50)
    """
    A rajouter (foreignKey, OneToManyField, ManyToManyField ?):
        * avis sur le livre
        * membres ayant lu le livre
        * boîte à livre où on peut trouver le livre
        * recommendations (autres oeuvres liées)
        * date de parution
        * nombres de livre dispo
        * boîtes à livre contenant le livre
        * date et position du dernier dépôt
    """

    class Meta:
        # verbose_name = "superlivre" 
        # verbose_name indique quel titre prennent les objets dans l'administration. S'il n'est pas précisé,
        # il s'agit juste du nom de la classe
        ordering = ['titre'] # indique que les livres sont classés par rapport à leur titre, ordre croissant
        
    def __str__(self):
        """
        C'est avec la méthode __str__ que l'administration représente 
        les livres dans la liste des livres
        """
        return self.titre

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.titre)

        super(Livre,self).save(*args, **kwargs)

    def getUrl(self):
        """Retourne l'url permettant d'acceder à la description du livre """

        return reverse('main_app.views.to_bookList').replace('list',self.slug_title)


class UserProfile(models.Model):
    """ Profil d'un membre de la communauté Bookinner """

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    imageProfil = models.ImageField(upload_to = "imagesDeProfil/",blank=True,verbose_name = "Image de Profil")
    # le verbose_name de imageProfil précisé dans le modèle est celui utilisé dans l'administration
    slug_username = models.SlugField(default = "", unique = True, blank=True)
  

    def save(self, *args, **kwargs):
        # Verifier si cette condition est nécessaire
        if not self.id:
            self.slug_username = slugify(self.user.username)

        super(UserProfile,self).save(*args, **kwargs)

    def __str__(self):

        s = "Pseudo du membre: " + self.user.username + \
            "\nIdentité du membre: " + self.user.first_name + " " + self.user.last_name 
        return s

    