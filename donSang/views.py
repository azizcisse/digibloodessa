from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donateur import models as dmodels
from patient import models as pmodels
from donateur import forms as dforms
from patient import forms as pforms



def home_view(request):
    x = models.StockSang.objects.all()
    print(x)
    if len(x) == 0:
        sang1 = models.StockSang()
        sang1.groupesanguin = "A+"
        sang1.save()

        sang2 = models.StockSang()
        sang2.groupesanguin = "A-"
        sang2.save()

        sang3 = models.StockSang()
        sang3.groupesanguin = "B+"
        sang3.save()

        sang4 = models.StockSang()
        sang4.groupesanguin = "B-"
        sang4.save()

        sang5 = models.StockSang()
        sang5.groupesanguin = "AB+"
        sang5.save()

        sang6 = models.StockSang()
        sang6.groupesanguin = "AB-"
        sang6.save()

        sang7 = models.StockSang()
        sang7.groupesanguin = "O+"
        sang7.save()

        sang8 = models.StockSang()
        sang8.groupesanguin = "O-"
        sang8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "donSang/index.html")


def is_donateur(user):
    return user.groups.filter(name="DONATEUR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


def afterlogin_view(request):
    if is_donateur(request.user):
        return redirect("donateur/donateur-dashboard")

    elif is_patient(request.user):
        return redirect("patient/patient-dashboard")
    else:
        return redirect("admin-dashboard")


@login_required(login_url="adminlogin")
def admin_dashboard_view(request):
    totalunite = models.StockSang.objects.aggregate(Sum("unite"))
    dict = {
        "A1": models.StockSang.objects.get(groupesanguin="A+"),
        "A2": models.StockSang.objects.get(groupesanguin="A-"),
        "B1": models.StockSang.objects.get(groupesanguin="B+"),
        "B2": models.StockSang.objects.get(groupesanguin="B-"),
        "AB1": models.StockSang.objects.get(groupesanguin="AB+"),
        "AB2": models.StockSang.objects.get(groupesanguin="AB-"),
        "O1": models.StockSang.objects.get(groupesanguin="O+"),
        "O2": models.StockSang.objects.get(groupesanguin="O-"),
        "totaldonateurs": dmodels.Donateur.objects.all().count(),
        "totalunitesang": totalunite["unite__sum"],
        "totaldemande": models.DemandedeSang.objects.all().count(),
        "totaldemandeapprouve": models.DemandedeSang.objects.all()
        .filter(status="Approuve")
        .count(),
    }
    return render(request, "donSang/admin_dashboard.html", context=dict)


@login_required(login_url="adminlogin")
def admin_sang_view(request):
    dict = {
        "SangForm": forms.SangForm(),
        "A1": models.StockSang.objects.get(groupesanguin="A+"),
        "A2": models.StockSang.objects.get(groupesanguin="A-"),
        "B1": models.StockSang.objects.get(groupesanguin="B+"),
        "B2": models.StockSang.objects.get(groupesanguin="B-"),
        "AB1": models.StockSang.objects.get(groupesanguin="AB+"),
        "AB2": models.StockSang.objects.get(groupesanguin="AB-"),
        "O1": models.StockSang.objects.get(groupesanguin="O+"),
        "O2": models.StockSang.objects.get(groupesanguin="O-"),
    }
    if request.method == "POST":
        sangForm = forms.SangForm(request.POST)
        if sangForm.is_valid():
            groupesanguin = sangForm.cleaned_data["groupesanguin"]
            StockSang = models.StockSang.objects.get(groupesanguin=groupesanguin)
            StockSang.unite = sangForm.cleaned_data["unite"]
            StockSang.save()
        return HttpResponseRedirect("admin-sang")
    return render(request, "donSang/admin_sang.html", context=dict)


@login_required(login_url="adminlogin")
def admin_donateur_view(request):
    donateurs = dmodels.Donateur.objects.all()
    return render(request, "donSang/admin_donateur.html", {"donateurs": donateurs})


@login_required(login_url="adminlogin")
def modifier_donateur_view(request, pk):
    donateur = dmodels.Donateur.objects.get(id=pk)
    user = dmodels.User.objects.get(id=donateur.user_id)
    userForm = dforms.DonateurUserForm(instance=user)
    donateurForm = dforms.DonateurForm(request.FILES, instance=donateur)
    mondict = {"userForm": userForm, "donateurForm": donateurForm}
    if request.method == "POST":
        userForm = dforms.DonateurUserForm(request.POST, instance=user)
        donateurForm = dforms.DonateurForm(
            request.POST, request.FILES, instance=donateur
        )
        if userForm.is_valid() and donateurForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            donateur = donateurForm.save(commit=False)
            donateur.user = user
            donateur.groupesanguin = donateurForm.cleaned_data["groupesanguin"]
            donateur.save()
            return redirect("admin-donateur")
    return render(request, "donSang/modifier_donateur.html", context=mondict)


@login_required(login_url="adminlogin")
def supprimer_donateur_view(request, pk):
    donateur = dmodels.Donateur.objects.get(id=pk)
    user = User.objects.get(id=donateur.user_id)
    user.delete()
    donateur.delete()
    return HttpResponseRedirect("/admin-donateur")


@login_required(login_url="adminlogin")
def admin_patient_view(request):
    patients = pmodels.Patient.objects.all()
    return render(request, "donSang/admin_patient.html", {"patients": patients})


@login_required(login_url="adminlogin")
def modifier_patient_view(request, pk):
    patient = pmodels.Patient.objects.get(id=pk)
    user = pmodels.User.objects.get(id=patient.user_id)
    userForm = pforms.PatientUserForm(instance=user)
    patientForm = pforms.PatientForm(request.FILES, instance=patient)
    mondict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = pforms.PatientUserForm(request.POST, instance=user)
        patientForm = pforms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.groupesanguin = patientForm.cleaned_data["groupesanguin"]
            patient.save()
            return redirect("admin-patient")
    return render(request, "donSang/modifier_patient.html", context=mondict)


@login_required(login_url="adminlogin")
def supprimer_patient_view(request, pk):
    patient = pmodels.Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect("/admin-patient")


@login_required(login_url="adminlogin")
def admin_demande_view(request):
    requests = models.DemandedeSang.objects.all().filter(status="En-Attente")
    return render(request, "donSang/admin_demande.html", {"requests": requests})


@login_required(login_url="adminlogin")
def admin_historique_demande_view(request):
    requests = models.DemandedeSang.objects.all().exclude(status="En-Attente")
    return render(
        request, "donSang/admin_historique_demande.html", {"requests": requests}
    )


@login_required(login_url="adminlogin")
def admin_donation_view(request):
    donations = dmodels.SangDonne.objects.all()
    return render(request, "donSang/admin_donation.html", {"donations": donations})


@login_required(login_url="adminlogin")
def modifier_status_approuve_view(request, pk):
    req = models.DemandedeSang.objects.get(id=pk)
    message = None
    groupesanguin = req.groupesanguin
    unite = req.unite
    StockSang = models.StockSang.objects.get(groupesanguin=groupesanguin)
    if StockSang.unite > unite:
        StockSang.unite = StockSang.unite - unite
        StockSang.save()
        req.status = "Approuve"

    else:
        message = (
            "La Quantité de Stock de Sang n'est pas assez pour approuver cette demande, Seulement"
            + str(StockSang.unite)
            + " Unité Disponible"
        )
    req.save()

    requests = models.DemandedeSang.objects.all().filter(status="En-Attente")
    return render(
        request,
        "donSang/admin_demande.html",
        {"requests": requests, "message": message},
    )


@login_required(login_url="adminlogin")
def modifier_status_rejete_view(request, pk):
    req = models.DemandedeSang.objects.get(id=pk)
    req.status = "Rejete"
    req.save()
    return HttpResponseRedirect("/admin-demande")


@login_required(login_url="adminlogin")
def donation_approuve_view(request, pk):
    donation = dmodels.SangDonne.objects.get(id=pk)
    donation_sang_groupe = donation.groupesanguin
    donation_sang_unite = donation.unite

    stock = models.StockSang.objects.get(groupesanguin=donation_sang_groupe)
    stock.unite = stock.unite + donation_sang_unite
    stock.save()

    donation.status = "Approuve"
    donation.save()
    return HttpResponseRedirect("/admin-donation")


@login_required(login_url="adminlogin")
def donation_rejete_view(request, pk):
    donation = dmodels.SangDonne.objects.get(id=pk)
    donation.status = "Rejete"
    donation.save()
    return HttpResponseRedirect("/admin-donation")
