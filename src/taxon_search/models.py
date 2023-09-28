from datetime import date

from django.db import models


class EnsemblMetadata(models.Model):
    
    taxonomy_id = models.IntegerField()
    url_name = models.CharField(max_length=1000)
    display_name = models.CharField(max_length=1000)
    scientific_name = models.CharField(max_length=1000)
    strain = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'ensembl_metadata'
        unique_together = (('taxonomy_id', 'display_name'),)


class NCBITaxonFlat(models.Model):

    taxon_id = models.IntegerField(null=False)
    parent_id = models.IntegerField(null=False)
    left_index = models.IntegerField(null=False, default=0)
    right_index = models.IntegerField(null=False, default=0)
    rank = models.CharField(max_length=32, null=False, db_index=True)
    name = models.CharField(max_length=500, db_index=True)
    name_class = models.CharField(max_length=50, null=False, db_index=True)
    species_taxon_id = models.IntegerField(null=False)
    name_index = models.CharField(max_length=500, null=False, db_index=True)

    class Meta:
        db_table = 'ncbi_taxon_flat'
        unique_together = (('taxon_id', 'name', 'name_class', 'species_taxon_id'),)
