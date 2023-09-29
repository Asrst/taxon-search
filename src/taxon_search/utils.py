from sqlalchemy import create_engine, text as sql_text
from .models import EnsemblMetadata, NCBITaxonFlat

TREE_TRAVERSAL_LIMIT = 5

def load_synonym_file(path):
    """
    Utility function to load 
    Elastic search synonym files.

    Parameters:
    path (str): Path to the file.

    Returns:
    return_type (List[str]): List of string for elastic search server 
    to retrieve synonyms/phrases.
    
    """
    syn_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            syn_list.append(line)

    print(f"{path} file loaded...")

    return syn_list
    

def run_custom_sql(engine, query):
    """
    Utility function to execute 
    custom sql directly on Django models.

    Parameters:
    engine (sqlalchemy.create_engine): A sqlalchemy engine.
    query (str): A SQL in multi-lined string format.

    Returns:
    return_type (List[List]): List of Lists containing the 
    retrieved query results.
    
    """
    with engine.connect() as cursor:
        rows = cursor.execute(sql_text(query))

    return [row for row in rows]


def get_relevant_species(species_dict):
    """
    Given a species dictonary with taxonomy id, the function
    retrieves species from its parent id's and matches them 
    with ensembl database.

    Parameters:
    species_dict (Dict): A dictonary with species details like 
    taxonomy id, parent id, name, etc.

    Returns:
    species_dict (List[Dict]): List of Dictonaries containing the 
            matched relevant species.

    parent_name (str): Name of parent taxonomy under 
    which species match is found.


    """
    # for a given taxonomy id, get all parent ids from the tree.
    taxon_id = species_dict["species_taxon_id"]
    all_parent_ids = get_all_parents(taxon_id)[::-1]

    # start from last, iterate through each parent id
    parent_id = all_parent_ids[0][0]
    parent_name = all_parent_ids[0][1]
    parent_species = get_species_from_parent(parent_id)
    ensembl_matches = EnsemblMetadata.objects.filter(taxonomy_id__in=parent_species)

    # try to get get species from that parent id & match with ensembl database.
    # stop when match is found
    count = 1
    while count <= TREE_TRAVERSAL_LIMIT and len(ensembl_matches) < 1:
        parent_id = all_parent_ids[count][0]
        parent_name = all_parent_ids[count][1]
        parent_species = get_species_from_parent(parent_id)
        ensembl_matches = EnsemblMetadata.objects.filter(taxonomy_id__in=parent_species)
        count += 1

    species_dict = [ensembl_matches[i].__dict__ for i in range(0, len(ensembl_matches))]

    return species_dict, parent_name


def get_all_parents(taxon_id):
    """
    The function is called inside the `get_relevant_species`
    function to get all parents given a taxonomy id.

    Parameters:
    taxon_id (str): Taxonomy Id

    Returns:
    return_type (List[List]): List of List containing all
    parent ids and names of given taxonomy id.

    """

    ncbi_engine = create_engine("mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109")

    query = f"""SELECT n2.parent_id, na.name
                FROM ncbi_taxa_node n1 
                JOIN (ncbi_taxa_node n2
                    LEFT JOIN ncbi_taxa_name na 
                    ON n2.parent_id = na.taxon_id AND na.name_class = "scientific name")  
                ON n2.left_index <= n1.left_index 
                AND n2.right_index >= n1.right_index 
                WHERE n1.taxon_id = {taxon_id}
                ORDER BY n2.left_index
                """
    with ncbi_engine.connect() as cursor:
        rows = cursor.execute(sql_text(query))

    return [row for row in rows]


def get_species_from_parent(parent_id):
    """
    The function is called inside the `get_relevant_species`
    function to get all species childs present under given a parent taxonomy id.

    Parameters:
    parent_id (str): Parent Taxonomy Id

    Returns:
    return_type (List): List containing all species ids present under 
    given parent id tree.
    
    """

    ncbi_engine = create_engine("mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109")

    query = f"""SELECT distinct ntn.taxon_id
                FROM ncbi_taxa_node AS Parents, ncbi_taxa_node AS Children
                left join ncbi_taxa_name ntn 
                ON Children.taxon_id = ntn.taxon_id AND ntn.name_class = "scientific name"
                WHERE Children.left_index > Parents.left_index
                AND Children.left_index < Parents.right_index
                AND Parents.taxon_id = {parent_id} AND Children.rank = 'species'
                order by name
        """

    with ncbi_engine.connect() as cursor:
        rows = cursor.execute(sql_text(query))

    return [r[0] for r in rows]