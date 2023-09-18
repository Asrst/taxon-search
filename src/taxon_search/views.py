from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .search import search_species
from .models import TaxonFlat, EnsemblMetadata
from django.db import connection

import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, text as sql_text


def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row


# Create your views here.
def index(request):

    query_params = request.GET
    q = query_params.get('q')

    context = {}
    results = []
    if q is not None and len(q) > 1:
        search_results = search_species(q)

        name_class = [d['name_class'] for d in search_results][0]
        rank = [d['rank'] for d in search_results][0]

        matched_species = set([d['species_taxon_id'] for d in search_results])
        species_names = EnsemblMetadata.objects.filter(taxonomy_id__in=matched_species)
        
        context['query'] = q
        context['match_type'] = "excat"

        # if name_class = scientific name & rank = species is excat match
        # if name_class != scientific name & rank = species is returning synoyms [returning synonym species for]
        # if name_class = scientific name & rank != species is species under provided rank [returning closely related species under given rank]
        # if name_class != scientific name & rank != species is rank synonynms + species under provided rank 
        # if no species found then traverse the tree and return species under common ancestors [returning species under common ancestor].

        if len(species_names) > 0:
            
            if name_class != "scientific name" and rank == 'species':
                context['match_type'] = 'synonym'
            elif rank != "species":
                context['match_type'] = 'related'
                context['rank'] = rank

            species_list = [species_names[i].__dict__ for i in range(0, len(species_names))]
            for d in species_list:
                d['ensembl_url'] = "http://metazoa.ensembl.org/" + str(d["url_name"])
                results.append(d)
        else:
            for sp_dict in search_results:
                species_list, common_ancestor = get_relevant_species(sp_dict)
                for d in species_list:
                    d['ensembl_url'] = "http://metazoa.ensembl.org/" + str(d["url_name"])
                    results.append(d)

                context['match_type'] = "ancestor"
                context['common_ancestor'] = common_ancestor

    context['results'] = results

    return render(request, "index.html", context)


def get_relevant_species(sp_dict):

    taxid = sp_dict["species_taxon_id"]
    all_parent_ids = get_all_parents(taxid)[::-1]
    
    # for a given taxonomy id, get all parent ids from the tree.
    # start from last, iterate through each parent id
    # try to get get species from that parent id & match with ensembl database.
    # stop when match is found

    parent_id = all_parent_ids[0][0]
    parent_name = all_parent_ids[0][1]
    parent_species = get_species_from_parent(parent_id)
    ensembl_matches = EnsemblMetadata.objects.filter(taxonomy_id__in=parent_species)

    count = 1
    while count <= 5 and len(ensembl_matches) < 1:
        parent_id = all_parent_ids[count][0]
        parent_name = all_parent_ids[count][1]
        parent_species = get_species_from_parent(parent_id)
        ensembl_matches = EnsemblMetadata.objects.filter(taxonomy_id__in=parent_species)
        count += 1

    species_dict = [ensembl_matches[i].__dict__ for i in range(0, len(ensembl_matches))]

    return species_dict, parent_name


def get_all_parents(taxon_id):

    ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')

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

    # print([r for r in rows])
    return [r for r in rows]


def get_species_from_parent(parent_id):

    ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')

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

    # print([r for r in rows])
    return [r[0] for r in rows]


def taxon_tree(request, taxon_id):

    # print(taxon_id)

    query = f"""SELECT n2.taxon_id , n2.parent_id_id ,na.name
                    ,n2.rank ,na.name_class
                    ,n2.left_index, n2.right_index
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id_id AND na.name_class = "scientific name")  
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxon_id}
                    ORDER BY n2.left_index
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    results = []
    for row in rows:
        d = {}
        d['taxon_id'] = row[0]
        d['parent_id'] = row[1]
        d['name'] = row[2]
        d['rank'] = row[3]
        d['name_class'] = row[4]
        results.append(d)

    context = {}
    context['results'] = results
    context['query'] = taxon_id


    #return HttpResponse("Hello, world. You're at the Tax on search index.")
    return render(request, "tree.html", context)


def redirect_to_ensembl(request, taxon_id):

    # print(taxon_id)

    query = f"""SELECT n2.taxon_id , n2.parent_id_id ,na.name
                    ,n2.rank ,na.name_class
                    ,n2.left_index, n2.right_index
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id_id AND na.name_class = "scientific name")  
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxon_id}
                    ORDER BY n2.left_index
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    results = []
    for row in rows:
        d = {}
        d['taxon_id'] = row[0]
        d['parent_id'] = row[1]
        d['name'] = row[2]
        d['rank'] = row[3]
        d['name_class'] = row[4]
        results.append(d)

    context = {}
    context['results'] = results
    context['query'] = taxon_id


    #return HttpResponse("Hello, world. You're at the Tax on search index.")
    return render(request, "tree.html", context)



