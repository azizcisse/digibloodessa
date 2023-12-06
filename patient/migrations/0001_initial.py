# Generated by Django 4.2.4 on 2023-09-17 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profil",
                    models.ImageField(
                        blank=True, null=True, upload_to="profil/Patient/"
                    ),
                ),
                ("age", models.PositiveIntegerField()),
                ("groupesanguin", models.CharField(max_length=10)),
                ("maladie", models.CharField(max_length=100)),
                ("medecin", models.CharField(max_length=50)),
                ("adresse", models.CharField(max_length=40)),
                ("telephone", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]