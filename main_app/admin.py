from django.contrib import admin
from . import models
# Register your models here.

class LivreAdmin(admin.ModelAdmin):
    """ Classe indiquant l'affichage et les opérations possibles sur les
    objets Livre dans l'administration 
    """
    list_display = ('titre','auteur','slug_title','couverture','note') # ce qui est afficher dans la liste des Livres, 
                                                          # et l'ordre d'affichage
    list_filter = ('titre','auteur','note') # champs permettant de filtrer les livres
    ordering = ('titre',) # champs à partir desquels les livres sont ordonnées
    search_fields = ('titre', 'auteur', 'note', 'isbn') # champs utilisés pour rechercher les livres
    fields = ('titre','slug_title','auteur','couverture','resume',
            'edition','note','codeBarre','isbn')
    prepopulated_fields = {'slug_title':('titre',),}
    # important: les champs dans prepopulated_field doivent faire partie des champs dans fields


class MembreAdmin(admin.ModelAdmin):
    """Classe indiquant l'affichage et les opérations possibles sur les 
    objets Membre dans l'administration
    """

    list_display = ('pseudo','slug_pseudo','imageProfil','nom','prenom')
    ordering = ('pseudo',)
    search_fields = ('pseudo', 'nom', 'prenom')
    fields = ('pseudo','slug_pseudo','nom','prenom','imageProfil')
    prepopulated_fields = {'slug_pseudo':('pseudo',),}





admin.site.register(models.Livre, LivreAdmin)
# permet de manipuler des objets Livre dans la base de données à partir de l'administration
# et lie la classe Livre a une représentation dans l'administration, LivreAdmin
admin.site.register(models.Membre, MembreAdmin)