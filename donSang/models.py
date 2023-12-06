from django.db import models
from patient import models as pmodels
from donateur import models as dmodels


class StockSang(models.Model):
    groupesanguin = models.CharField(max_length=10)
    unite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.groupesanguin


class DemandedeSang(models.Model):
    demande_du_patient = models.ForeignKey(pmodels.Patient, null=True, on_delete=models.CASCADE)
    demande_du_donateur = models.ForeignKey(dmodels.Donateur, null=True, on_delete=models.CASCADE)
    nomPatient = models.CharField(max_length=30)
    agePatient = models.PositiveIntegerField()
    raison = models.CharField(max_length=500)
    groupesanguin = models.CharField(max_length=10)
    unite = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="En-Attente")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.groupesanguin
