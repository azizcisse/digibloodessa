from django.urls import path
from django.contrib.auth.views import LoginView
from . import views



urlpatterns = [
    path(
        "donateurlogin",
        LoginView.as_view(template_name="donateur/donateurlogin.html"),
        name="donateurlogin",
    ),
    path("donateursignup", views.donateur_signup_view, name="donateursignup"),
    path("donateur-dashboard", views.donateur_dashboard_view, name="donateur-dashboard"),
    path("sang-donne", views.sang_donne_view, name="sang-donne"),
    path("historique-donation", views.historique_donation_view, name="historique-donation"),
    path("demande-effectuee", views.demande_effectuee_view, name="demande-effectuee"),
    path("historique-demande", views.historique_demande_view, name="historique-demande"),    
    # path("historique-demande", views.SangDonneListView.as_view(), name="historique-demande"),  
    path("pdf-demande/<int:pk>", views.render_pdf_demande_view, name="pdf-demande"), 
    path("pdf-don/<int:pk>", views.render_pdf_don_view, name="pdf-don"), 
]
