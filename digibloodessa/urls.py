from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from donSang import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("donateur/", include("donateur.urls")),
    path("patient/", include("patient.urls")),
    path("", views.home_view, name=""),
    path(
        "logout", LogoutView.as_view(template_name="donSang/logout.html"), name="logout"
    ),
    path("afterlogin", views.afterlogin_view, name="afterlogin"),
    path(
        "adminlogin",
        LoginView.as_view(template_name="donSang/adminlogin.html"),
        name="adminlogin",
    ),
    path("admin-dashboard", views.admin_dashboard_view, name="admin-dashboard"),
    path("admin-sang", views.admin_sang_view, name="admin-sang"),
    path("admin-donateur", views.admin_donateur_view, name="admin-donateur"),
    path("admin-patient", views.admin_patient_view, name="admin-patient"),
    path("modifier-donateur/<int:pk>", views.modifier_donateur_view, name="modifier-donateur"),
    path("supprimer-donateur/<int:pk>", views.supprimer_donateur_view, name="supprimer-donateur"),
    path("admin-demande", views.admin_demande_view, name="admin-request"),
    path("modifier-patient/<int:pk>", views.modifier_patient_view, name="modifier-patient"),
    path("supprimer-patient/<int:pk>", views.supprimer_patient_view, name="supprimer-patient"),
    path("admin-donation", views.admin_donation_view, name="admin-donation"),
    path(
        "donation-approuve/<int:pk>",
        views.donation_approuve_view,
        name="donation-approuve",
    ),
    path(
        "donation-rejete/<int:pk>", views.donation_rejete_view, name="donation-rejete"
    ),
    path(
        "admin-historique-demande",
        views.admin_historique_demande_view,
        name="admin-historique-demande",
    ),
    path(
        "modifier-status-approuve/<int:pk>",
        views.modifier_status_approuve_view,
        name="modifier-status-approuve",
    ),
    path(
        "modifier-status-rejete/<int:pk>",
        views.modifier_status_rejete_view,
        name="modifier-status-rejete",
    ),
]
