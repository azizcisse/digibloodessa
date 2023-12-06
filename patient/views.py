from django.shortcuts import get_object_or_404, render, redirect, reverse
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donSang import forms as bforms
from donSang import models as bmodels

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    demande_patient = get_object_or_404(bmodels.DemandedeSang, pk=pk)    
    template_path = 'patient/pdf_demande_patient.html'
    context = {
        'demande_patient': demande_patient,
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="demande_de_sang.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mondict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.groupesanguin = patientForm.cleaned_data["groupesanguin"]
            patient.save()
            mon_groupe_patient = Group.objects.get_or_create(name="PATIENT")
            mon_groupe_patient[0].user_set.add(user)
        return HttpResponseRedirect("patientlogin")
    return render(request, "patient/patientsignup.html", context=mondict)


def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    dict = {
        "demandeEnAttente": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_patient=patient)
        .filter(status="En-Attente")
        .count(),
        "demandeApprouve": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_patient=patient)
        .filter(status="Approuve")
        .count(),
        "effectueDemande": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_patient=patient)
        .count(),
        "demandeRejete": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_patient=patient)
        .filter(status="Rejete")
        .count(),
    }

    return render(request, "patient/patient_dashboard.html", context=dict)


def faire_demande_view(request):
    demande_form = bforms.DemandeForm()
    if request.method == "POST":
        demande_form = bforms.DemandeForm(request.POST)
        if demande_form.is_valid():
            demande_de_sang = demande_form.save(commit=False)
            demande_de_sang.groupesanguin = demande_form.cleaned_data["groupesanguin"]
            patient = models.Patient.objects.get(user_id=request.user.id)
            demande_de_sang.demande_du_patient = patient
            demande_de_sang.save()
            return HttpResponseRedirect("mes-demandes")
    return render(request, "patient/faire_demande.html", {"demande_form": demande_form})


def mes_demandes_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    demande_de_sang = bmodels.DemandedeSang.objects.all().filter(
        demande_du_patient=patient
    )
    return render(request, "patient/mes_demandes.html", {"demande_de_sang": demande_de_sang})
