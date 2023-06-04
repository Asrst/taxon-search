from django.db import models

# Create your models here.

class NCBITaxaNode(models.Model):

    taxon_id = models.IntegerField(primary_key=True)
    parent_id = models.ForeignKey('self', nullable=False, db_index=True)
    rank = models.CharField(max_length=32, nullable=False, db_index=True)
    genbank_hidden_flag = models.SmallIntegerField(nullable=False, default=0)
    left_index = models.IntegerField(nullable=False, default=0, db_index=True)
    right_index = models.IntegerField(nullable=False, default=0, db_index=True)
    root_id = models.IntegerField(nullable=False, default=1)

    class Meta:
        db_table = 'ncbi_taxa_node'



class NCBITaxaName(models.Model):

    taxon_id = models.ForeignKey(NCBITaxaNode, on_delete=models.CASCADE, primary_key=True, db_index=True)
    name = models.CharField(max_length=500, db_index=True, primary_key=True)
    name_class = models.CharField(50, nullable=False, db_index=True)

    class Meta:
        db_table = 'ncbi_taxa_name'

