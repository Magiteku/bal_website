from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    """Formulaire pour le OneToOneField User de la classe Membre """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50,required=False)
    last_name = forms.CharField(max_length=50,required=False)

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2")
        labels = {
            "password1": "Mot de passe",
            "password2": "Confirmer mot de passe",
        } # ne marche pas

    def save(self,commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        
        return user
    


class UserProfileForm(forms.ModelForm):
    """Formulaire d'inscription d'un membre"""

    class Meta:
        model = UserProfile
        fields = ("imageProfil",)
        labels = {
            "imageProfil": "Image de profil", 
        }
        



    """
    Remarque: Les ModelForm vérifie déjà l'unicité des champs ayant un keyword unique=True ou autre keyword 
    équivalent en True. Le but de clean_pseudo est de personalisé le message que lit l'utilisateur afin
    qu'il comprenne le refus de la validation du formulaire
    """
    def clean_pseudo(self):
        """ Vérifie que le pseudo n'a pas déjà été utilisé """

        pseudo = self.cleaned_data["pseudo"]
        occurences = UserProfile.objects.filter(pseudo=pseudo).count()
        if occurences > 0:
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")

        return pseudo
        # les méthodes clean doivent toujours renvoyer le champ qu'elles nettoient


class LoginForm(forms.Form):
    """Formulaire de connexion d'un membre """
    pass