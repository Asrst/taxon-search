# Generated by Django 4.2.1 on 2023-06-04 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NCBITaxaNode",
            fields=[
                ("taxon_id", models.IntegerField(primary_key=True, serialize=False)),
                ("rank", models.CharField(db_index=True, max_length=32)),
                ("genbank_hidden_flag", models.SmallIntegerField(default=0)),
                ("left_index", models.IntegerField(db_index=True, default=0)),
                ("right_index", models.IntegerField(db_index=True, default=0)),
                ("root_id", models.IntegerField(default=1)),
                (
                    "parent_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taxon_search.ncbitaxanode",
                    ),
                ),
            ],
            options={
                "db_table": "ncbi_taxa_node",
            },
        ),
        migrations.CreateModel(
            name="NCBITaxaName",
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
                ("name", models.CharField(db_index=True, max_length=500)),
                ("name_class", models.CharField(db_index=True, max_length=50)),
                (
                    "taxaname_taxon_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="taxaname_taxon_id",
                        to="taxon_search.ncbitaxanode",
                    ),
                ),
            ],
            options={
                "db_table": "ncbi_taxa_name",
                "unique_together": {("taxaname_taxon_id", "name")},
            },
        ),
    ]
