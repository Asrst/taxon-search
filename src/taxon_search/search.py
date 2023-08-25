from .documents import TaxanomyDocument, TaxonFlatDocument


def search_species(query):

    if not query:
        return

    # s = TaxanomyDocument.search().filter("term", color="red")
    # hits = TaxanomyDocument.search().query("match", name=query)

    # q_results = []

    # for hit in hits:
    #     print(hit, hit.meta.score)

    #     data = {
    #         "name": hit.name,
    #         "name_class": hit.name_class,
    #         "taxon_id": hit.taxon_id,
    #     }
    #     q_results.append(data)

    # default: 10 results are returned
    # hits = EnsemblTaxonDocument.search().query("match", scientific_name=query)
    # q_results = []

    # for hit in hits:
    #     print(hit.taxonomy_id, hit.scientific_name, hit.meta.score)
    #     print(hit.display_name, hit.strain, hit.url_name)

    #     data = {
    #         "name": hit.display_name,
    #         "strain": hit.strain,
    #         "taxon_id": hit.taxonomy_id,
    #         "ensembl_url": "http://metazoa.ensembl.org/" + str(hit.url_name)
    #     }
    #     q_results.append(data)

    hits = TaxonFlatDocument.search().query("term", name_index=query.lower().strip())
    q_results = []

    for hit in hits:
        print(hit.name, hit.name_class, hit.taxon_id, hit.species_taxon_id, hit.meta.score)
        print(hit.parent_id)
        # print(hit.display_name, hit.strain, hit.url_name)

        data = {
            "taxon_id":hit.taxon_id,
            "name": hit.name,
            "name_class": hit.name_class,
            "species_taxon_id": hit.species_taxon_id,
            "rank": hit.rank,
            "parent_id":hit.parent_id
        }
        q_results.append(data)


    return q_results
