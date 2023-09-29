from .documents import TaxonFlatDocument


def search_species(query):
    if not query:
        return

    # default: 10 results are returned
    hits = TaxonFlatDocument.search().query("term", name_index=query.lower().strip())
    q_results = []

    for hit in hits:
        print(hit.name, hit.name_class, hit.taxon_id, hit.species_taxon_id, hit.meta.score)
        print(hit.parent_id)

        data = {
            "taxon_id": hit.taxon_id,
            "name": hit.name,
            "name_class": hit.name_class,
            "species_taxon_id": hit.species_taxon_id,
            "rank": hit.rank,
            "parent_id": hit.parent_id,
        }
        q_results.append(data)

    return q_results
