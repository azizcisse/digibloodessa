from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
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


def render_pdf_demande_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    demande_donateur = get_object_or_404(bmodels.DemandedeSang, pk=pk)    
    template_path = 'donateur/pdf_demande_donateur.html'
    context = {
        'demande_donateur': demande_donateur,
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


def render_pdf_don_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    don_donateur = get_object_or_404(models.SangDonne, pk=pk)
    
    template_path = 'donateur/pdf_don_donateur.html'
    context = {
        'don_donateur': don_donateur,
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="don_donateur.pdf"'
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



def donateur_signup_view(request):
    userForm = forms.DonateurUserForm()
    donateurForm = forms.DonateurForm()
    mondict = {"userForm": userForm, "donateurForm": donateurForm}
    if request.method == "POST":
        userForm = forms.DonateurUserForm(request.POST)
        donateurForm = forms.DonateurForm(request.POST, request.FILES)
        if userForm.is_valid() and donateurForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            donateur = donateurForm.save(commit=False)
            donateur.user = user
            donateur.groupesanguin = donateurForm.cleaned_data["groupesanguin"]
            donateur.save()
            mon_groupe_de_don = Group.objects.get_or_create(name="DONATEUR")
            mon_groupe_de_don[0].user_set.add(user)
        return HttpResponseRedirect("donateurlogin")
    return render(request, "donateur/donateursignup.html", context=mondict)


def donateur_dashboard_view(request):
    donateur = models.Donateur.objects.get(user_id=request.user.id)
    dict = {
        "demandeEnAttente": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_donateur=donateur)
        .filter(status="En-Attente")
        .count(),
        "demandeApprouvee": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_donateur=donateur)
        .filter(status="Approuve")
        .count(),
        "demadeEffectuee": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_donateur=donateur)
        .count(),
        "demandeRejetee": bmodels.DemandedeSang.objects.all()
        .filter(demande_du_donateur=donateur)
        .filter(status="Rejete")
        .count(),
    }
    return render(request, "donateur/donateur_dashboard.html", context=dict)


def sang_donne_view(request):
    donation_form = forms.DonationForm()
    if request.method == "POST":
        donation_form = forms.DonationForm(request.POST)
        if donation_form.is_valid():
            sang_donne = donation_form.save(commit=False)
            sang_donne.groupesanguin = donation_form.cleaned_data["groupesanguin"]
            donateur = models.Donateur.objects.get(user_id=request.user.id)
            sang_donne.donateur = donateur
            sang_donne.save()
            return HttpResponseRedirect("historique-donation")
    return render(request, "donateur/sang_donne.html", {"donation_form": donation_form})


def historique_donation_view(request):
    donateur = models.Donateur.objects.get(user_id=request.user.id)
    donations = models.SangDonne.objects.all().filter(donateur=donateur)
    return render(request, "donateur/historique_donation.html", {"donations": donations})


def demande_effectuee_view(request):
    demandeform = bforms.DemandeForm()
    if request.method == "POST":
        demandeform = bforms.DemandeForm(request.POST)
        if demandeform.is_valid():
            demande_de_sang = demandeform.save(commit=False)
            demande_de_sang.groupesanguin = demandeform.cleaned_data["groupesanguin"]
            donateur = models.Donateur.objects.get(user_id=request.user.id)
            demande_de_sang.demande_du_donateur = donateur
            demande_de_sang.save()
            return HttpResponseRedirect("historique-demande")
    return render(request, "donateur/demande_effectuee.html", {"demandeform": demandeform})


def historique_demande_view(request):
    donateur = models.Donateur.objects.get(user_id=request.user.id)
    demande_de_sang = bmodels.DemandedeSang.objects.all().filter(demande_du_donateur=donateur)
    return render(
        request, "donateur/historique_demande.html", {"demande_de_sang": demande_de_sang}
    )
