from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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

admin.site.register(models.Livre, LivreAdmin)
# permet de manipuler des objets Livre dans la base de données à partir de l'administration
# et lie la classe Livre a une représentation dans l'administration, LivreAdmin

class UserProfileInline(admin.StackedInline):
    """Classe indiquant l'affichage et les opérations possibles sur les 
    objets Membre dans l'administration
    """
    model = models.UserProfile # nécessaire lorsqu'on utilise les inlines
    
    
admin.site.unregister(User) # nécessaire car User a déjà un modelAdmin enregistré par défaut
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    
    # on utilise add_fieldsets au lieu de fields tout seul car User a déjà une classe admin (?)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None,
            {'fields':('email','first_name','last_name')}),   
    )
    

    ordering = ('username',)
    inlines = [UserProfileInline,] 

    # dans la list_display il est possible de mettre le nom d'une méthode de la classe
    # attention à la gestion des manyToManyField, voir  la doc sur list_display de ModelAdmin
    list_display = ('username','slug_username','email','first_name','last_name','imageProfil',
        'is_active','is_staff','is_superuser')
    search_fields = ('username', 'last_name', 'first_name','email')
    

    def slug_username(self,obj):
        """Retourne le champ slug_username de UserProfile """
        # Pour récuperer le champ d'un OneToOneField (dans les 2 sens), 
        # on fait: obj.nomclasseEnMinuscule.nomChamp
        return obj.userprofile.slug_username

    def imageProfil(self,obj):
        """ Retourne l'image de profil du UserProfile """
        return obj.userprofile.imageProfil








