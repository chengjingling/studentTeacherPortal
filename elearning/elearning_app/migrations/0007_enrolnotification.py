# Generated by Django 4.2.7 on 2024-02-13 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("elearning_app", "0006_chat"),
    ]

    operations = [
        migrations.CreateModel(
            name="EnrolNotification",
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
                ("read", models.BooleanField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning_app.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning_app.appuser",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teacher",
                        to="elearning_app.appuser",
                    ),
                ),
            ],
        ),
    ]