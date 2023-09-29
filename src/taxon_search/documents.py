import os

from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter
from django.forms.models import model_to_dict

from .models import EnsemblMetadata, NCBITaxonFlat
from .utils import load_synonym_file


autophrase_syn_filter = token_filter(
    name_or_instance="autophrase_syn_filter",  # Name for the filter
    type="synonym",  # Synonym filter type
    synonyms=load_synonym_file(os.path.join(os.path.dirname(__file__), "taxon-elastic-search.ph")),
)

synonym_token_filter = token_filter(
    name_or_instance="synonym_token_filter",  # Name for the filter
    lenient=False,
    type="synonym",  # Synonym filter type
    tokenizer="keyword",
    synonyms=load_synonym_file(os.path.join(os.path.dirname(__file__), "taxon-elastic-search.syn")),
)

index_analyzer = analyzer(
    "index_analyzer",
    tokenizer="standard",
    filter=["lowercase", "stop", autophrase_syn_filter, synonym_token_filter],
)

#### Ensembl Taxonomy Flat
taxon_flat_index = Index("ncbi_taxon_flat")

taxon_flat_index.settings(number_of_shards=1, number_of_replicas=0)


@taxon_flat_index.document
class TaxonFlatDocument(Document):
    taxon_id = fields.IntegerField(attr="taxon_id")
    parent_id = fields.IntegerField(attr="parent_id")
    left_index = fields.IntegerField(attr="left_index")
    right_index = fields.IntegerField(attr="right_index")

    rank = fields.KeywordField(attr="rank")
    name = fields.KeywordField(attr="name")
    name_class = fields.KeywordField(attr="name_class")

    species_taxon_id = fields.IntegerField(attr="species_taxon_id")
    name_index = fields.KeywordField(attr="name_index")

    class Django:
        ####
        model = NCBITaxonFlat  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = []
        related_models = []

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Configure how the index should be refreshed after an update.
        # See Elasticsearch documentation for supported options:
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
        # This per-Document setting overrides settings.ELASTICSEARCH_DSL_AUTO_REFRESH.
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""

        result = super(TaxonFlatDocument, self).get_queryset().all()

        return result

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """

        pass
