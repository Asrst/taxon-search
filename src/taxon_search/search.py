from .documents import TaxonFlatDocument

def search_species(query):
    """
    The function calls the Elastic Search Document Model using 
    a query string and returns the results of the elastic search. 

    Parameters:
    query (str): Query string provided by the user as Input

    Returns:
    return_type (List[Dict]): List of Dictonaries containing the 
            search results from the elastic search server.

    """
    if not query:
        return

    # default: 10 results are returned
    hits = TaxonFlatDocument.search().query("term", name_index=query.lower().strip())
    query_results = []

    for hit in hits:
        # print(hit.name, hit.name_class, hit.taxon_id, hit.species_taxon_id, hit.meta.score)
        # print(hit.parent_id)

        data = {
            "taxon_id": hit.taxon_id,
            "name": hit.name,
            "name_class": hit.name_class,
            "species_taxon_id": hit.species_taxon_id,
            "rank": hit.rank,
            "parent_id": hit.parent_id,
        }
        query_results.append(data)

    return query_results
