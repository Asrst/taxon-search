from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from .models import NCBITaxaName, NCBITaxaNode
from elasticsearch_dsl import analyzer, token_filter
from django.forms.models import model_to_dict
from .utils import load_synonym_file
import os


taxon_index = Index('taxon')

taxon_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

autophrase_syn_filter = token_filter(
    name_or_instance='autophrase_syn_filter', # Name for the filter
    type='synonym', # Synonym filter type
    synonyms = load_synonym_file(os.path.join(os.path.dirname(__file__), 'taxon-elastic-search.ph'))
    )


synonym_token_filter = token_filter(
    name_or_instance='synonym_token_filter', # Name for the filter
    type='synonym', # Synonym filter type
    tokenizer = "keyword",
    synonyms = load_synonym_file(os.path.join(os.path.dirname(__file__), 'taxon-elastic-search.syn'))
    # synonyms=[
    #     'reactjs, react',  # <-- important
    # ],
    # synonyms_path = "analysis/wn_s.pl"
    )

index_analyzer = analyzer(
    'index_analyzer',
    tokenizer="standard",
    filter=["lowercase", "stop", autophrase_syn_filter, synonym_token_filter],
)

@registry.register_document
@taxon_index.document
class TaxanomyDocument(Document):

    name = fields.TextField(
        attr='name',
        analyzer=index_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )
    name_class = fields.KeywordField(attr='name_class')
    
    # taxon_id = fields.IntegerField(attr='taxaname_taxon_id')
    # taxa_node = fields.ObjectField(properties={
    #     'taxon_id': fields.IntegerField(), 
    #     'parent_id': fields.IntegerField(),
    #     'rank':fields.KeywordField(),
    # })

    taxon_id = fields.ObjectField(properties={
                'taxon_id': fields.IntegerField(),
                'rank':fields.KeywordField(),
    })

    parent_id = fields.ObjectField(properties={
        'parent_id': fields.IntegerField()
    })


    class Django:
        model = NCBITaxaName # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            # 'name',
            # 'name_class'
            # 'taxon_id'
        ]
        related_models = [NCBITaxaNode]


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
        
        result = super(TaxanomyDocument, self).get_queryset().select_related(
            'taxon_id'
        )

        # for ob in NCBITaxaName.objects.select_related('taxon_id'):
        #     print(ob.taxon_id.ncbitaxanode_set.all()[0].__dict__)

        # print(NCBITaxaName.objects.select_related().all()[67].__dict__)
        # print(NCBITaxaName.objects.ncbitaxanode_set.all()[67].__dict__)
        # print(model_to_dict(result[454]))

        # print(len(result.filter(taxon_id_id__rank='species')))

        return result.filter(name_class="scientific name").filter(taxon_id__rank='species')

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """

        if isinstance(related_instance, NCBITaxaNode):
            # return related_instance.taxaname_taxon_id.all()
            # return NCBITaxaNode.objects.filter(taxon_id=related_instance)
            pass