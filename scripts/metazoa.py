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
    taxon_tids = taxon_dfs[0]['Taxon ID'].values
    print("extracted taxanomy ids:", len(taxon_tids))

    return taxon_tids


def get_taxon_tree(taxon_ids, db_engine):
    
    tree_df = pd.DataFrame()
    for i in range(len(taxon_ids[:])):
        taxonid = taxon_ids[i]
        query = f"""SELECT n2.taxon_id ,n2.parent_id ,na.name
                    ,n2.rank ,na.name_class
                    ,n2.left_index, n2.right_index
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id)  
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxonid}
                    ORDER BY left_index
        """

        df = pd.read_sql_query(query, db_engine)
        df['query_taxon_id'] = taxonid
        tree_df = pd.concat([tree_df, df])
    
    tree_df.to_csv("metazoa_taxon.csv", index=False)

    return tree_df
    
if __name__ == "__main__":
    species_url = "https://metazoa.ensembl.org/species.html"
    ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')
    
    metazoa_ids = get_taxon_ids(species_url)
    metazoa_df = get_taxon_tree(metazoa_ids, ncbi_engine)

