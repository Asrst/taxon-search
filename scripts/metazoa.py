import pymysql
pymysql.install_as_MySQLdb()

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


species_url = "https://metazoa.ensembl.org/species.html"
response = requests.get(species_url)
soup = BeautifulSoup(response.text, "lxml")

table = soup.find("table") # {"class":"data_table exportable ss autocenter"}
taxon_dfs = pd.read_html(str(table))
metazoa_tids = taxon_dfs[0]['Taxon ID'].values
print("extracted metazoa tax ids:", len(metazoa_tids))

ncbi_engine = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109')

metazoa_df = pd.DataFrame()
for i in range(len(metazoa_tids[:])):
    taxonid = metazoa_tids[i]
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

    df = pd.read_sql_query(query, ncbi_engine)
    df['query_taxon_id'] = taxonid
    metazoa_df = pd.concat([metazoa_df, df])
    

metazoa_df.to_csv("metazoa_taxon.csv", index=False)