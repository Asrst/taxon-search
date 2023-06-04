from django.db import models

class NCBITaxaNode(models.Model):

    taxon_id = models.IntegerField(primary_key=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=False, db_index=True)
    rank = models.CharField(max_length=32, null=False, db_index=True)
    genbank_hidden_flag = models.SmallIntegerField(null=False, default=0)
    left_index = models.IntegerField(null=False, default=0, db_index=True)
    right_index = models.IntegerField(null=False, default=0, db_index=True)
    root_id = models.IntegerField(null=False, default=1)

    class Meta:
        db_table = 'ncbi_taxa_node'



class NCBITaxaName(models.Model):

    taxon_id = models.ForeignKey(NCBITaxaNode, on_delete=models.CASCADE, db_index=True, 
                                 related_name='taxaname_taxon_id')
    name = models.CharField(max_length=500, db_index=True)
    name_class = models.CharField(max_length=50, null=False, db_index=True)

    class Meta:
        db_table = 'ncbi_taxa_name'
        unique_together = (('taxon_id', 'name'),)


