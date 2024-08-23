# Generated by Django 5.0.6 on 2024-08-21 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lookups", "0004_alter_city_latitude_alter_city_longitude"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobTitle",
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
                ("name", models.CharField(max_length=200)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_titles",
                        to="lookups.department",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["id"], name="lookups_job_id_ebe7b1_idx")
                ],
            },
        ),
    ]
