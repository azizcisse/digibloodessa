from django.urls import path
from django.contrib.auth.views import LoginView
from . import views



urlpatterns = [
    path(
        "patientlogin",
        LoginView.as_view(template_name="patient/patientlogin.html"),
        name="patientlogin",
    ),
    path("patientsignup", views.patient_signup_view, name="patientsignup"),
    path("patient-dashboard", views.patient_dashboard_view, name="patient-dashboard"),
    path("faire-demande", views.faire_demande_view, name="faire-demande"),
    path("mes-demandes", views.mes_demandes_view, name="mes-demandes"),
    path("pdf-patient/<int:pk>", views.render_pdf_view, name="pdf-patient"),
]
