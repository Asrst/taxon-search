from .documents import TaxanomyDocument


def search_species(query):

    if not query:
        return

    # s = TaxanomyDocument.search().filter("term", color="red")
    hits = TaxanomyDocument.search().query("match", name=query)

    q_results = []

    for hit in hits:
        # print(hit, hit.taxon_id)

        data = {
            "name": hit.name,
            "name_class": hit.name_class,
            "taxon_id": hit.taxon_id,
        }
        q_results.append(data)

    return q_results
