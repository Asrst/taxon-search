# Generated by Django 4.2.1 on 2023-07-28 05:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("taxon_search", "0008_ncbitaxaflat"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="NCBITaxaFlat",
            new_name="EnsemblTaxonFlat",
        ),
        migrations.AlterModelTable(
            name="ensembltaxonflat",
            table="ensembl_taxon_flat",
        ),
    ]
