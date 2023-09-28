# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Assembly(models.Model):
    assembly_id = models.AutoField(primary_key=True)
    assembly_accession = models.CharField(max_length=16, blank=True, null=True)
    assembly_name = models.CharField(max_length=200)
    assembly_default = models.CharField(max_length=200)
    assembly_ucsc = models.CharField(max_length=16, blank=True, null=True)
    assembly_level = models.CharField(max_length=50)
    base_count = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = "assembly"
        unique_together = (("assembly_accession", "assembly_default", "base_count"),)


class AssemblySequence(models.Model):
    assembly_sequence_id = models.AutoField(primary_key=True)
    assembly_id = models.PositiveIntegerField()
    name = models.CharField(max_length=40)
    acc = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "assembly_sequence"
        unique_together = (("assembly_id", "name", "acc"),)


class ComparaAnalysis(models.Model):
    compara_analysis_id = models.AutoField(primary_key=True)
    data_release_id = models.PositiveIntegerField()
    division_id = models.PositiveIntegerField()
    method = models.CharField(max_length=50)
    set_name = models.CharField(max_length=128, blank=True, null=True)
    dbname = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = "compara_analysis"
        unique_together = (("division_id", "method", "set_name", "dbname"),)


class ComparaAnalysisEvent(models.Model):
    compara_analysis_event_id = models.AutoField(primary_key=True)
    compara_analysis_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    source = models.CharField(max_length=128, blank=True, null=True)
    creation_time = models.DateTimeField()
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "compara_analysis_event"


class DataRelease(models.Model):
    data_release_id = models.AutoField(primary_key=True)
    ensembl_version = models.PositiveIntegerField()
    ensembl_genomes_version = models.PositiveIntegerField(blank=True, null=True)
    release_date = models.DateField()
    is_current = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "data_release"
        unique_together = (("ensembl_version", "ensembl_genomes_version"),)


class DataReleaseDatabase(models.Model):
    data_release_database_id = models.AutoField(primary_key=True)
    data_release_id = models.PositiveIntegerField()
    dbname = models.CharField(max_length=64)
    type = models.CharField(max_length=8, blank=True, null=True)
    division_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "data_release_database"
        unique_together = (("data_release_id", "dbname"),)


class DataReleaseDatabaseEvent(models.Model):
    data_release_database_event_id = models.AutoField(primary_key=True)
    data_release_database_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    source = models.CharField(max_length=128, blank=True, null=True)
    creation_time = models.DateTimeField()
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "data_release_database_event"


class Division(models.Model):
    division_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32)
    short_name = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = "division"


class Genome(models.Model):
    genome_id = models.AutoField(primary_key=True)
    data_release_id = models.PositiveIntegerField()
    assembly_id = models.PositiveIntegerField()
    organism_id = models.PositiveIntegerField()
    genebuild = models.CharField(max_length=255)
    division_id = models.PositiveIntegerField()
    has_pan_compara = models.PositiveIntegerField()
    has_variations = models.PositiveIntegerField()
    has_peptide_compara = models.PositiveIntegerField()
    has_genome_alignments = models.PositiveIntegerField()
    has_synteny = models.PositiveIntegerField()
    has_other_alignments = models.PositiveIntegerField()
    has_microarray = models.PositiveIntegerField()
    website_packed = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome"
        unique_together = (("data_release_id", "genome_id", "division_id"),)


class GenomeAlignment(models.Model):
    genome_alignment_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    count = models.PositiveIntegerField()
    genome_database_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome_alignment"
        unique_together = (("genome_id", "type", "name", "genome_database_id"),)


class GenomeAnnotation(models.Model):
    genome_annotation_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    value = models.CharField(max_length=128)
    genome_database_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome_annotation"
        unique_together = (("genome_id", "type", "genome_database_id"),)


class GenomeComparaAnalysis(models.Model):
    genome_compara_analysis_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    compara_analysis_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome_compara_analysis"
        unique_together = (("genome_id", "compara_analysis_id"),)


class GenomeDatabase(models.Model):
    genome_database_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    dbname = models.CharField(max_length=64)
    species_id = models.PositiveIntegerField()
    type = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "genome_database"
        unique_together = (("genome_id", "dbname", "species_id"),)


class GenomeEvent(models.Model):
    genome_event_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    source = models.CharField(max_length=128, blank=True, null=True)
    creation_time = models.DateTimeField()
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "genome_event"


class GenomeFeature(models.Model):
    genome_feature_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    analysis = models.CharField(max_length=128)
    count = models.PositiveIntegerField()
    genome_database_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome_feature"
        unique_together = (("genome_id", "type", "analysis", "genome_database_id"),)


class GenomeVariation(models.Model):
    genome_variation_id = models.AutoField(primary_key=True)
    genome_id = models.PositiveIntegerField()
    type = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    count = models.PositiveIntegerField()
    genome_database_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "genome_variation"
        unique_together = (("genome_id", "type", "name", "genome_database_id"),)


class Organism(models.Model):
    organism_id = models.AutoField(primary_key=True)
    taxonomy_id = models.PositiveIntegerField()
    reference = models.CharField(max_length=128, blank=True, null=True)
    species_taxonomy_id = models.PositiveIntegerField()
    name = models.CharField(unique=True, max_length=128)
    url_name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    scientific_name = models.CharField(max_length=128)
    strain = models.CharField(max_length=128, blank=True, null=True)
    serotype = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "organism"


class OrganismAlias(models.Model):
    organism_alias_id = models.AutoField(primary_key=True)
    organism_id = models.PositiveIntegerField()
    alias = models.CharField(max_length=255, db_collation="latin1_bin", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "organism_alias"
        unique_together = (("organism_id", "alias"),)


class OrganismPublication(models.Model):
    organism_publication_id = models.AutoField(primary_key=True)
    organism_id = models.PositiveIntegerField()
    publication = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "organism_publication"
        unique_together = (("organism_id", "publication"),)
