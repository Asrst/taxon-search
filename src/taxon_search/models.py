from datetime import date

from django.db import models


class EnsemblMetadata(models.Model):
    """
    EnsemblMetadata Django model class.

    All fields defined are self explainatory and 
    picked up from the ensembl MySQL database
    aftering joining 'organism' , 'genome', 'division'
    and 'data_release' tables present 
    in the 'ensmebl_metadata_109' schema/database.

    refer the scripts/get_ensembl_metadata.py for SQL query used.

    """

    taxonomy_id = models.IntegerField()
    url_name = models.CharField(max_length=1000)
    display_name = models.CharField(max_length=1000)
    scientific_name = models.CharField(max_length=1000)
    strain = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "ensembl_metadata"
        unique_together = (("taxonomy_id", "display_name"),)


class NCBITaxonFlat(models.Model):
    """
    NCBI Taxonomy Django model class.

    All fields defined are self explainatory and 
    picked up from the ensembl MySQL database
    aftering joining 'ncbi_taxa_node' and 'ncbi_taxa_name'
    tables present in the 'ncbi_taxonomy_109' schema/database.
    
    refer the scripts/get_taxon_flat.py for SQL query used.

    """

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
        db_table = "ncbi_taxon_flat"
        unique_together = (("taxon_id", "name", "name_class", "species_taxon_id"),)
