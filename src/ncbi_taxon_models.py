# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NcbiTaxaName(models.Model):
    taxon_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    name_class = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ncbi_taxa_name'


class NcbiTaxaNode(models.Model):
    taxon_id = models.PositiveIntegerField(primary_key=True)
    parent_id = models.PositiveIntegerField()
    rank = models.CharField(max_length=32)
    genbank_hidden_flag = models.IntegerField()
    left_index = models.IntegerField()
    right_index = models.IntegerField()
    root_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ncbi_taxa_node'
