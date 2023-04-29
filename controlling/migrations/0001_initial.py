# Generated by Django 4.2 on 2023-04-29 17:39

import datetime
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
            name="Employee",
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
                ("firstName", models.CharField(max_length=20)),
                ("lastName", models.CharField(max_length=30)),
                (
                    "workStatus",
                    models.CharField(
                        choices=[
                            ("open", "Otwarta"),
                            ("paused", "Wstrzymana"),
                            ("closed", "Zakończona"),
                        ],
                        default="open",
                        max_length=20,
                    ),
                ),
                ("jobtitle", models.CharField(max_length=30)),
                (
                    "joblevel",
                    models.CharField(
                        choices=[
                            ("junior", "Asystent / Technik / Stażysta"),
                            ("mid", "Inżynier / Kordynator"),
                            ("senior", "Projektant / Project Manager"),
                            ("expert", "Kierownik / Ekspert"),
                        ],
                        default="junior",
                        max_length=30,
                    ),
                ),
                ("workStart", models.DateField(default=datetime.date(2023, 4, 29))),
                ("workEnd", models.DateField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
