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
            name="Donateur",
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
                        blank=True, null=True, upload_to="profil/Donateur/"
                    ),
                ),
                ("groupesanguin", models.CharField(max_length=10)),
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
        migrations.CreateModel(
            name="SangDonne",
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
                ("maladie", models.CharField(default="Aucune", max_length=100)),
                ("age", models.PositiveIntegerField()),
                ("groupesanguin", models.CharField(max_length=10)),
                ("unite", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(default="En-Attente", max_length=20)),
                ("date", models.DateField(auto_now=True)),
                (
                    "donateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="donateur.donateur",
                    ),
                ),
            ],
        ),
    ]