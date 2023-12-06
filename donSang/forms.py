from django import forms

from . import models


class SangForm(forms.ModelForm):
    class Meta:
        model = models.StockSang
        fields = ["groupesanguin", "unite"]


class DemandeForm(forms.ModelForm):
    class Meta:
        model = models.DemandedeSang
        fields = ["nomPatient", "agePatient", "raison", "groupesanguin", "unite"]