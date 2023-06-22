from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .search import search_species
from django.db import connection


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

    if q is not None:
        results = search_species(q)
        context['results'] = results
        context['query'] = q

    #return HttpResponse("Hello, world. You're at the Tax on search index.")
    return render(request, "index.html", context)


def taxon_tree(request, taxon_id):

    print(taxon_id)

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

