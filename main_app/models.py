from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
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


class Membre(models.Model):
    """ Membre de la communauté Bookinner """

    pseudo = models.CharField(max_length = 50, unique=True)
    nom = models.CharField(max_length = 50)
    prenom = models.CharField(max_length = 50)
    imageProfil = models.ImageField(upload_to = "imagesDeProfil/")
    slug_pseudo = models.SlugField(default = "", unique = True)

    """Rajouté un booléan pour vérifier la connection """
    class Meta:
        ordering = ['pseudo']
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_pseudo = slugify(self.pseudo)

        super(Membre,self).save(*args, **kwargs)

    def __str__(self):

        s = "Pseudo du membre: " + self.pseudo + \
            "\nIdentité du membre: " + self.prenom + " " + self.nom 
        return s

    