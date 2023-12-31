# Generated by Django 4.2.1 on 2023-07-06 11:08

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OnePieceCapituloManga",
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
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("capitulo", models.IntegerField()),
                ("volumen", models.IntegerField()),
                ("titulo", models.CharField(max_length=255)),
                ("titulo_romanizado", models.CharField(max_length=255)),
                ("titulo_viz", models.CharField(max_length=255)),
                ("paginas", models.IntegerField()),
                ("fecha_publicacion", models.DateField()),
                ("episodios", models.CharField(max_length=100)),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
