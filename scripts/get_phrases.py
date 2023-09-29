import re

from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import requests
from sqlalchemy import create_engine


pymysql.install_as_MySQLdb()


def get_taxon_ids(url):
    """
    The function scrapes the metazoa taxonomy ids data
    from a fixed url: https://metazoa.ensembl.org/species.html

    Returns:
    return_type (List): List containing the taxonomy ids
    that belong to metazoa.

    """
        
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    table = soup.find("table")  # {"class": "data_table exportable ss autocenter"}
    taxon_dfs = pd.read_html(str(table))
    taxon_ids = taxon_dfs[0]["Taxon ID"].unique()
    print("extracted taxonomy ids:", len(taxon_ids))

    return taxon_ids


def preprocess_name(text):
    """
    Does some basic text preprocessing like 
    removing special characters, extra spaces, etc.
    """
    name = text["name"]
    if text["name_class"] != "scientific name":
        name = re.sub(r"[,.;@#?!&$\(\)]+\ *", " ", name)
        name = re.sub(" +", " ", name)

    out = name.lower().replace(" ", "_").strip("_")

    if len(out.split("_")) > 1:
        style = "{} => {}"
        return style.format(text["name"], out)

    return pd.NA


def get_taxon_names(taxon_ids, db_conn):
    """
    The function connects with ensembl My sql database
    and runs a sql query to retrieve taxon names like synonyms, common names, 
    scientif names and converts into elastic search synonym file format. 

    Parameters:
    taxon_ids (List): list of taxonomy ids for which entire tree structures
    needs to be queried
    db_conn (sqlalchemy.create_engine): A sqlalchemy engine.

    Returns:
    pandas dataframe (pd.DataFrame): tabluar data.

    """

    query_df = pd.DataFrame()
    for i in range(len(taxon_ids[:])):
        taxon_id = taxon_ids[i]
        query = f"""SELECT n2.* , na.name, na.name_class
                    FROM ncbi_taxa_node n1 
                    JOIN (ncbi_taxa_node n2
                        LEFT JOIN ncbi_taxa_name na 
                        ON n2.taxon_id = na.taxon_id)  
                    ON n2.left_index <= n1.left_index 
                    AND n2.right_index >= n1.right_index 
                    WHERE n1.taxon_id = {taxon_id}
                    ORDER BY left_index"""
        df = pd.read_sql_query(query, db_conn)
        df["query_taxon_id"] = taxon_id

        query_df = pd.concat([query_df, df])

    query_df = query_df.drop_duplicates()

    syn_df = query_df[
        (query_df["name_class"].isin(["scientific name", "synonym", "equivalent name"]))
        & (~query_df["rank"].isin(["no rank"]))
    ].reset_index(drop=1)

    syn_df["phrase"] = syn_df.apply(lambda r: preprocess_name(r), axis=1)

    return syn_df


if __name__ == "__main__":
    species_url = "https://metazoa.ensembl.org/species.html"
    ncbi_engine = create_engine("mysql://anonymous@ensembldb.ensembl.org:3306/ncbi_taxonomy_109")
    db_conn = ncbi_engine.connect()

    metazoa_ids = get_taxon_ids(species_url)
    taxon_syns = get_taxon_names(metazoa_ids, db_conn)

    # count the synonyms
    taxon_syns["len"] = taxon_syns["name"].str.split(",").str.len()

    # get phrases
    phrases = taxon_syns["phrase"].dropna().unique()

    # save the phrases into a text file to load into elastic search
    pd.Series(phrases).to_csv("taxon-elastic-search.ph", header=None, index=None, sep=",")
