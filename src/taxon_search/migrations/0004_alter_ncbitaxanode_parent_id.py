# Generated by Django 4.2.1 on 2023-06-10 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("taxon_search", "0003_alter_ncbitaxanode_parent_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ncbitaxanode",
            name="parent_id",
            field=models.ForeignKey(
                default=0,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="taxon_search.ncbitaxanode",
            ),
        ),
    ]
