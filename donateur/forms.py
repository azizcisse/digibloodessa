from django import forms
from django.contrib.auth.models import User
from . import models


class DonateurUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {"password": forms.PasswordInput()}


class DonateurForm(forms.ModelForm):
    class Meta:
        model = models.Donateur
        fields = ["groupesanguin", "adresse", "telephone", "profil"]


class DonationForm(forms.ModelForm):
    class Meta:
        model = models.SangDonne
        fields = ["age", "groupesanguin", "maladie", "unite"]
