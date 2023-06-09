# Generated by Django 4.1.5 on 2023-01-06 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
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
            ],
        ),
        migrations.CreateModel(
            name="CarTypes",
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
                ("producer", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=100)),
                ("year", models.PositiveIntegerField()),
                (
                    "fuel",
                    models.CharField(
                        choices=[
                            ("Petrol", "Petrol"),
                            ("Gas", "Gas"),
                            ("Diesel", "Diesel"),
                        ],
                        max_length=10,
                    ),
                ),
                ("seats", models.PositiveIntegerField()),
                (
                    "gearbox",
                    models.CharField(
                        choices=[("Automatic", "Automatic"), ("Manual", "Manual")],
                        max_length=10,
                    ),
                ),
                (
                    "drive",
                    models.CharField(
                        choices=[
                            ("FWD", "Front Wheel Drive"),
                            ("AWD", "All Wheel Drive"),
                            ("RWD", "Rear Wheel Drive"),
                        ],
                        max_length=3,
                    ),
                ),
                ("price", models.PositiveIntegerField()),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.CreateModel(
            name="RentHistory",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("add_fuel", models.BooleanField(default=False)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
            ],
        ),
    ]
