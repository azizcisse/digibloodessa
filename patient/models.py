from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profil = models.ImageField(upload_to="profil/Patient/", null=True, blank=True)
    age = models.PositiveIntegerField()
    groupesanguin = models.CharField(max_length=10)
    maladie = models.CharField(max_length=100)
    medecin = models.CharField(max_length=50)
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

