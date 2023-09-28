from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import requests
from sqlalchemy import create_engine, text as sql_text


pymysql.install_as_MySQLdb()


def get_taxon_ids(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find("table")  # {"class": "data_table exportable ss autocenter"}
    taxon_dfs = pd.read_html(str(table))
    taxon_ids = taxon_dfs[0]['Taxon ID'].unique().tolist()
    print("extracted taxonomy ids:", len(taxon_ids))

    return taxon_ids


def get_taxon_tree(taxon_ids, db_conn):

    unique_taxons = list(set(taxon_ids))
    
    tree_df = pd.DataFrame()
    for i in range(len(unique_taxons[:])):
        taxon_id = unique_taxons[i]
        query = f"""SELECT n2.taxon_id ,n2.parent_id ,na.name
                    ,n2.rank ,na.name_class
                    ,n2.left_index, n2.right_index
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id) 
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxon_id}
                    ORDER BY left_index"""
    
        df = pd.read_sql_query(sql_text(query), db_conn)
        df['species_taxon_id'] = taxon_id
        tree_df = pd.concat([tree_df, df])
    
    # filter on required rank & name class
    syn_df = tree_df[(tree_df['name_class'].isin(['scientific name', 'synonym', 
                                                'equivalent name']))
                & (~tree_df['rank'].isin(['no rank']))].reset_index(drop=1)
    syn_df['name_index'] = syn_df['name'].apply(lambda r: r.lower().strip())

    return syn_df


if __name__ == "__main__":
    species_url = "https://metazoa.ensembl.org/species.html"
    ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')
    db_conn = ncbi_engine.connect()
    
    metazoa_ids = get_taxon_ids(species_url)
    add_ids = [707708, 549330, 365367, 10235, 2816133]
    all_ids = metazoa_ids + add_ids
    metazoa_df = get_taxon_tree(all_ids, db_conn)

    # get data json for taxon_search.EnsemblTaxonFlat model
    pk_col = []
    field_col = ['taxon_id', 'parent_id', 'name', 'rank', 'name_class', 'left_index',
       'right_index', 'species_taxon_id', 'name_index']
    unique_key = ['taxon_id', 'name', 'name_class', 'species_taxon_id']
    m2_df = metazoa_df[pk_col+field_col].drop_duplicates()
    m2_df = m2_df.drop_duplicates(subset=unique_key)

    m2_df.to_csv("ncbi_taxon_flat.csv", index=False)
    m2_df['model'] = 'taxon_search.NCBITaxonFlat' 
    m2_df['fields'] = m2_df[field_col].to_dict(orient="records")
    json_str = m2_df[['model', 'fields']].to_json(orient='records')
    
    OUT_FOLDER = f"src/taxon_search/fixtures"
    with open(f"{OUT_FOLDER}/ncbi_taxon_flat.json", "w") as outfile:
        outfile.write(json_str)

