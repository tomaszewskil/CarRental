# Generated by Django 4.1.5 on 2023-01-09 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="rental",
            name="open_hours",
            field=models.TextField(
                blank=True, default="Open hours coming soon... ", null=True
            ),
        ),
        migrations.AlterField(
            model_name="rental",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
