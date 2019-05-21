from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad
from .models import Team


class CreateAd(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ('creator', 'sixte_name', 'sixte_location', 'sixte_prix', 'sixte_date', 'sixte_limit', 'sixte_link')


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CreateTeam(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('ad', 'team_name', 'captain', 'player1', 'player2', 'player3', 'player4', 'player5', 'player6')
