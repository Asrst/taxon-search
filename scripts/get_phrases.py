import pymysql
pymysql.install_as_MySQLdb()

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

def get_taxon_ids(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find("table") # {"class":"data_table exportable ss autocenter"}
    taxon_dfs = pd.read_html(str(table))
    taxon_tids = taxon_dfs[0]['Taxon ID'].unique()
    print("extracted taxanomy ids:", len(taxon_tids))

    return taxon_tids

def get_taxon_names(taxon_ids, db_conn):
    
    query_df = pd.DataFrame()
    for i in range(len(taxon_ids[:])):
        taxonid = taxon_ids[i]
        query = f"""SELECT n2.* , na.name, na.name_class
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id AND na.name_class = "scientific name")  
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxonid}
                    ORDER BY left_index"""
        df = pd.read_sql_query(query, db_conn)
        df['query_taxon_id'] = taxonid

        query_df = pd.concat([query_df, df])
    
    query_df = query_df.drop_duplicates()
    # syn_df = (query_df.sort_values(by=['taxon_id', 'name_class'])
    #           .groupby(["taxon_id"])['name'].apply(", ".join).reset_index())
    
    syn_df = query_df[(~query_df['rank'].isin(['no rank'])) & 
                      (query_df['name_class'].isin(['scientific name']))]

    return syn_df



if __name__ == "__main__":
    species_url = "https://metazoa.ensembl.org/species.html"
    ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')
    db_conn = ncbi_engine.connect()

    metazoa_ids = get_taxon_ids(species_url)
    taxon_syns = get_taxon_names(metazoa_ids, db_conn)

    # count the synonyms
    taxon_syns['len'] = taxon_syns['name'].str.split(",").str.len()

    # replace spaces with _
    phrases = []
    for name in taxon_syns['name'].values:
        if len(name.split()) > 1:
            style = "{} => {}"
            ph = name.lower().replace(" ", "_")
            phrases.append(style.format(name, ph))

    # save the phrases into a text file to load into elastic search
    pd.Series(phrases).to_csv("taxon-elastic-search.ph", header=None, index=None, sep=',')