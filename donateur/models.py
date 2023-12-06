from django.db import models
from django.contrib.auth.models import User


class Donateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil = models.ImageField(
        upload_to="profil/Donateur/", null=True, blank=True
    )

    groupesanguin = models.CharField(max_length=10)
    adresse = models.CharField(max_length=40)
    telephone = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class SangDonne(models.Model):
    donateur = models.ForeignKey(Donateur, on_delete=models.CASCADE)
    maladie = models.CharField(max_length=100, default="Aucune")
    age = models.PositiveIntegerField()
    groupesanguin = models.CharField(max_length=10)
    unite = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="En-Attente")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.donateur

