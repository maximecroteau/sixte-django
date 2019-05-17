from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad


class CreateAd(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ('sixte_name', 'sixte_location', 'sixte_prix', 'sixte_date', 'sixte_limit', 'sixte_link')